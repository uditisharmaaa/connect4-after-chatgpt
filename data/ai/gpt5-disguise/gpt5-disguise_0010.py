import os
import random
import sys

ROWS = 6
COLS = 7
PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]
WIN_LEN = 4

if COLS > 26 or PLAYERS < 2 or PLAYERS > 5:
    print("Invalid settings.")
    sys.exit(1)

TOKENS = TOKENS[:PLAYERS]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear():
    os.system('clear')

def print_board(b):
    letters = [chr(ord('A') + i) for i in range(len(b[0]))]
    print("  " + "   ".join(letters))
    print("+---" * len(b[0]) + "+")
    for r in range(len(b)):
        row = []
        for c in range(len(b[0])):
            row.append(b[r][c])
        print("| " + " | ".join(row) + " |")
        print("+---" * len(b[0]) + "+")

def drop_token(b, col, token):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = token
            return True
    return False

def in_bounds(r, c, rmax, cmax):
    return 0 <= r < rmax and 0 <= c < cmax

def check_win(b, token):
    R = len(b)
    C = len(b[0])
    for r in range(R):
        for c in range(C):
            if b[r][c] != token:
                continue
            # right
            if c + WIN_LEN - 1 < C:
                ok = True
                for k in range(WIN_LEN):
                    if b[r][c + k] != token:
                        ok = False
                        break
                if ok:
                    return True
            # down
            if r + WIN_LEN - 1 < R:
                ok = True
                for k in range(WIN_LEN):
                    if b[r + k][c] != token:
                        ok = False
                        break
                if ok:
                    return True
            # down-right
            if r + WIN_LEN - 1 < R and c + WIN_LEN - 1 < C:
                ok = True
                for k in range(WIN_LEN):
                    if b[r + k][c + k] != token:
                        ok = False
                        break
                if ok:
                    return True
            # down-left
            if r + WIN_LEN - 1 < R and c - (WIN_LEN - 1) >= 0:
                ok = True
                for k in range(WIN_LEN):
                    if b[r + k][c - k] != token:
                        ok = False
                        break
                if ok:
                    return True
    return False

def board_full(b):
    for r in b:
        for v in r:
            if v == " ":
                return False
    return True

def read_column(max_col):
    while True:
        s = input().strip()
        if len(s) != 1:
            print("Invalid input. Enter a single letter.")
            continue
        ch = s.upper()
        if not ('A' <= ch <= 'Z'):
            print("Invalid input. Enter a letter.")
            continue
        idx = ord(ch) - ord('A')
        if idx < 0 or idx >= max_col:
            print("Out of range. Try again.")
            continue
        return idx

def main():
    b = make_board(ROWS, COLS)
    turn = random.randrange(PLAYERS)
    while True:
        clear()
        print_board(b)
        if board_full(b):
            print("It's a draw!")
            break
        token = TOKENS[turn]
        print(f"Player {token}, please enter a column:")
        col = read_column(COLS)
        placed = drop_token(b, col, token)
        if not placed:
            print("Column is full. You lose this turn. Press Enter to continue.")
            input()
            turn = (turn + 1) % PLAYERS
            continue
        if check_win(b, token):
            clear()
            print_board(b)
            print(f"Player {token} won!")
            break
        turn = (turn + 1) % PLAYERS

if __name__ == "__main__":
    main()
