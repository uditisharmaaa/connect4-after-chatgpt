import os
import random
import string

ROWS = 6
COLS = 7
PLAYERS = 2

tokens_all = ["X", "O", "V", "H", "M"]
tokens = tokens_all[:PLAYERS]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear():
    os.system('clear')

def print_board(b):
    letters = [string.ascii_uppercase[i] for i in range(COLS)]
    print("  " + "   ".join(letters))
    sep = "+" + ("---+" * COLS)
    for r in range(ROWS):
        print(sep)
        row = []
        for c in range(COLS):
            row.append(" " + b[r][c] + " ")
        print("|" + "|".join(row) + "|")
    print(sep)

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(b, ch):
    # horizontal, vertical, diag down-right, diag down-left
    for r in range(ROWS):
        for c in range(COLS):
            if b[r][c] != ch:
                continue
            # right
            win = True
            for k in range(4):
                if not in_bounds(r, c+k) or b[r][c+k] != ch:
                    win = False
                    break
            if win:
                return True
            # down
            win = True
            for k in range(4):
                if not in_bounds(r+k, c) or b[r+k][c] != ch:
                    win = False
                    break
            if win:
                return True
            # down-right
            win = True
            for k in range(4):
                if not in_bounds(r+k, c+k) or b[r+k][c+k] != ch:
                    win = False
                    break
            if win:
                return True
            # down-left
            win = True
            for k in range(4):
                if not in_bounds(r+k, c-k) or b[r+k][c-k] != ch:
                    win = False
                    break
            if win:
                return True
    return False

def board_full(b):
    for r in b:
        for v in r:
            if v == " ":
                return False
    return True

def valid_col_input(s):
    if len(s) != 1:
        return False
    if not s.isalpha():
        return False
    s = s.upper()
    idx = ord(s) - ord('A')
    return 0 <= idx < COLS

def first_empty_row(b, col):
    for r in range(ROWS-1, -1, -1):
        if b[r][col] == " ":
            return r
    return -1

def main():
    b = make_board(ROWS, COLS)
    turn = random.randint(0, PLAYERS - 1)
    clear()
    print_board(b)
    while True:
        ch = tokens[turn]
        print(f"Player {ch}, please enter a column:")
        col_input = ""
        while True:
            col_input = input().strip()
            if valid_col_input(col_input):
                break
            print(f"Player {ch}, please enter a column:")
        col = ord(col_input.upper()) - ord('A')
        placed = False
        row = first_empty_row(b, col)
        if row != -1:
            b[row][col] = ch
            placed = True
        clear()
        print_board(b)
        if placed:
            if check_win(b, ch):
                print(f"Player {ch} won!")
                break
            if board_full(b):
                print("It's a draw!")
                break
        else:
            # turn lost
            if board_full(b):
                print("It's a draw!")
                break
        turn = (turn + 1) % PLAYERS

if __name__ == "__main__":
    main()
