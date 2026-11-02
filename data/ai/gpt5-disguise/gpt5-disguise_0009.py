import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2

TOKENS = ["X", "O", "V", "H", "M"]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(b):
    os.system('clear')
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(len(b[0])))
    print(header)
    sep = "+" + "+".join(["---"] * len(b[0])) + "+"
    for row in b:
        print(sep)
        line = "|" + "|".join(" " + row[i] + " " for i in range(len(row))) + "|"
        print(line)
    print(sep)

def drop_token(b, col, t):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = t
            return r
    return None

def in_bounds(r, c, rmax, cmax):
    return 0 <= r < rmax and 0 <= c < cmax

def check_win(b, t):
    rmax = len(b)
    cmax = len(b[0])
    for r in range(rmax):
        for c in range(cmax):
            if b[r][c] != t:
                continue
            # right
            if c + 3 < cmax and all(b[r][c + k] == t for k in range(4)):
                return True
            # down
            if r + 3 < rmax and all(b[r + k][c] == t for k in range(4)):
                return True
            # down-right
            if r + 3 < rmax and c + 3 < cmax and all(b[r + k][c + k] == t for k in range(4)):
                return True
            # down-left
            if r + 3 < rmax and c - 3 >= 0 and all(b[r + k][c - k] == t for k in range(4)):
                return True
    return False

def board_full(b):
    for r in b:
        for v in r:
            if v == " ":
                return False
    return True

def main():
    if COLS > 26:
        print("Maximum 26 columns supported.")
        return
    players = TOKENS[:NUM_PLAYERS]
    b = make_board(ROWS, COLS)
    turn = random.randint(0, NUM_PLAYERS - 1)
    print_board(b)
    while True:
        t = players[turn]
        col_idx = None
        while True:
            s = input(f"Player {t}, please enter a column: ").strip().upper()
            if len(s) != 1 or not s.isalpha():
                continue
            col = ord(s) - ord('A')
            if 0 <= col < COLS:
                col_idx = col
                break
        row_placed = drop_token(b, col_idx, t)
        if row_placed is None:
            print_board(b)
            turn = (turn + 1) % NUM_PLAYERS
            continue
        print_board(b)
        if check_win(b, t):
            print(f"Player {t} won!")
            break
        if board_full(b):
            print("It's a draw!")
            break
        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
