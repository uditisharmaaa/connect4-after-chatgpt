import os
import random
import sys

ROWS = 6
COLS = 7
NUM_PLAYERS = 2

CHARS = ["X", "O", "V", "H", "M"]
PLAYERS = CHARS[:NUM_PLAYERS]

def make_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(b):
    os.system('clear')
    letters = [chr(ord('A') + i) for i in range(len(b[0]))]
    print("  " + "   ".join(letters))
    print("+---" * len(b[0]) + "+")
    for r in range(len(b)):
        s = "|"
        for c in range(len(b[0])):
            s += " " + b[r][c] + " |"
        print(s)
        print("+---" * len(b[0]) + "+")

def drop(b, col, ch):
    for r in range(len(b)-1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = ch
            return r, col
    return None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(b, r, c, ch):
    def count_dir(dr, dc):
        cnt = 1
        rr, cc = r + dr, c + dc
        while in_bounds(rr, cc, len(b), len(b[0])) and b[rr][cc] == ch:
            cnt += 1
            rr += dr
            cc += dc
        rr, cc = r - dr, c - dc
        while in_bounds(rr, cc, len(b), len(b[0])) and b[rr][cc] == ch:
            cnt += 1
            rr -= dr
            cc -= dc
        return cnt

    if count_dir(0, 1) >= 4:
        return True
    if count_dir(1, 0) >= 4:
        return True
    if count_dir(1, 1) >= 4:
        return True
    if count_dir(1, -1) >= 4:
        return True
    return False

def board_full(b):
    for r in b:
        for v in r:
            if v == " ":
                return False
    return True

def valid_col_input(s, cols):
    if len(s) != 1:
        return False
    if not ("A" <= s <= chr(ord("A") + cols - 1)):
        return False
    return True

def main():
    if COLS > 26:
        print("Max 26 columns supported.")
        sys.exit(1)
    b = make_board(ROWS, COLS)
    cur = random.randrange(0, NUM_PLAYERS)
    while True:
        print_board(b)
        p = PLAYERS[cur]
        print(f"Player {p}, please enter a column:")
        s = input().strip().upper()
        while not valid_col_input(s, COLS):
            print(f"Player {p}, please enter a column:")
            s = input().strip().upper()
        col = ord(s) - ord("A")
        pos = drop(b, col, p)
        if pos is None:
            print("Column is full. Turn lost.")
            cur = (cur + 1) % NUM_PLAYERS
            continue
        r, c = pos
        if check_win(b, r, c, p):
            print_board(b)
            print(f"Player {p} won!")
            break
        if board_full(b):
            print_board(b)
            print("It's a draw!")
            break
        cur = (cur + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
