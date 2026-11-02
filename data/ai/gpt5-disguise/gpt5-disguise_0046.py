import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
SYMS = ["X", "O", "V", "H", "M"]

if COLS > 26:
    COLS = 26
if NUM_PLAYERS < 2:
    NUM_PLAYERS = 2
if NUM_PLAYERS > 5:
    NUM_PLAYERS = 5

syms = SYMS[:NUM_PLAYERS]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(b):
    letters = string.ascii_uppercase[:len(b[0])]
    header = "  " + "   ".join(letters)
    sep = "+" + "+".join(["---"] * len(b[0])) + "+"
    print(header)
    print(sep)
    for r in range(len(b)):
        row = "|" + "|".join([" {} ".format(b[r][c]) for c in range(len(b[0]))]) + "|"
        print(row)
        print(sep)

def place(b, col, sym):
    for r in range(len(b)-1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = sym
            return r, col
    return None

def in_bounds(r, c, R, C):
    return 0 <= r < R and 0 <= c < C

def check_win(b, sym):
    R = len(b)
    C = len(b[0])
    for r in range(R):
        for c in range(C):
            if b[r][c] != sym:
                continue
            # right
            if c + 3 < C and all(b[r][c+i] == sym for i in range(4)):
                return True
            # down
            if r + 3 < R and all(b[r+i][c] == sym for i in range(4)):
                return True
            # down-right
            if r + 3 < R and c + 3 < C and all(b[r+i][c+i] == sym for i in range(4)):
                return True
            # down-left
            if r + 3 < R and c - 3 >= 0 and all(b[r+i][c-i] == sym for i in range(4)):
                return True
    return False

def board_full(b):
    for r in b:
        for v in r:
            if v == " ":
                return False
    return True

def get_col_input(valid_cols, sym):
    while True:
        s = input(f"Player {sym}, please enter a column: ").strip().upper()
        if len(s) == 1 and s in valid_cols:
            return s
        # keep asking until valid

def main():
    b = make_board(ROWS, COLS)
    cols_letters = string.ascii_uppercase[:COLS]
    turn = random.randrange(NUM_PLAYERS)
    os.system('clear')
    print_board(b)
    while True:
        sym = syms[turn]
        col_letter = get_col_input(cols_letters, sym)
        col = ord(col_letter) - ord('A')
        placed = place(b, col, sym)
        os.system('clear')
        print_board(b)
        if placed is None:
            # column full, lose turn
            pass
        else:
            if check_win(b, sym):
                print(f"Player {sym} won!")
                break
            if board_full(b):
                print("Draw!")
                break
        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
