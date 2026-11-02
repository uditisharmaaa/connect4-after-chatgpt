import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]

if COLS > 26:
    COLS = 26
players = TOKENS[:max(2, min(5, NUM_PLAYERS))]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear():
    os.system('clear')

def print_board(b):
    letters = string.ascii_uppercase[:len(b[0])]
    header = "  " + "   ".join(list(letters))
    sep = "+" + "+".join(["---"] * len(b[0])) + "+"
    print(header)
    print(sep)
    for r in range(len(b)):
        row = "|"
        for c in range(len(b[0])):
            row += " " + b[r][c] + " |"
        print(row)
        print(sep)

def col_from_input(s):
    if len(s) != 1:
        return None
    if not s.isalpha():
        return None
    s = s.upper()
    letters = string.ascii_uppercase[:COLS]
    if s not in letters:
        return None
    return letters.index(s)

def drop(b, col, token):
    for r in range(ROWS - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = token
            return r, col
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(b, token):
    for r in range(ROWS):
        for c in range(COLS):
            if b[r][c] != token:
                continue
            # right
            if c + 3 < COLS and all(b[r][c + k] == token for k in range(4)):
                return True
            # down
            if r + 3 < ROWS and all(b[r + k][c] == token for k in range(4)):
                return True
            # diag down-right
            if r + 3 < ROWS and c + 3 < COLS and all(b[r + k][c + k] == token for k in range(4)):
                return True
            # diag down-left
            if r + 3 < ROWS and c - 3 >= 0 and all(b[r + k][c - k] == token for k in range(4)):
                return True
    return False

def board_full(b):
    for r in b:
        for v in r:
            if v == " ":
                return False
    return True

def main():
    b = make_board(ROWS, COLS)
    turn = random.randint(0, len(players) - 1)
    clear()
    print_board(b)

    while True:
        token = players[turn]
        print(f"Player {token}, please enter a column:")
        while True:
            s = input().strip()
            col = col_from_input(s) if s else None
            if col is None:
                print("Invalid input. Please enter a valid column letter:")
                continue
            res = drop(b, col, token)
            if res is None:
                clear()
                print_board(b)
                print("Column full. Turn lost.")
                break
            clear()
            print_board(b)
            if check_win(b, token):
                print(f"Player {token} won!")
                return
            break

        if board_full(b):
            print("Game is a draw.")
            return

        turn = (turn + 1) % len(players)

if __name__ == "__main__":
    main()
