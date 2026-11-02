import random
import os
import sys

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_LEN = 4

alphabet = [chr(ord('A') + i) for i in range(26)]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear():
    os.system('clear')

def print_board(b):
    clear()
    header = "  " + "   ".join(alphabet[:len(b[0])])
    print(header)
    sep = "+" + "+".join(["---"] * len(b[0])) + "+"
    for r in range(len(b)):
        print(sep)
        row_str = "|"
        for c in range(len(b[0])):
            row_str += " " + b[r][c] + " |"
        print(row_str)
    print(sep)

def valid_col_input(s, cols):
    if len(s) != 1:
        return False
    if s not in alphabet[:cols]:
        return False
    return True

def drop(b, col, t):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = t
            return r, col
    return None

def in_bounds(r, c, R, C):
    return 0 <= r < R and 0 <= c < C

def check_win(b, t):
    R = len(b)
    C = len(b[0])
    for r in range(R):
        for c in range(C):
            if b[r][c] != t:
                continue
            # right
            ok = True
            for k in range(WIN_LEN):
                if not in_bounds(r, c + k, R, C) or b[r][c + k] != t:
                    ok = False
                    break
            if ok:
                return True
            # down
            ok = True
            for k in range(WIN_LEN):
                if not in_bounds(r + k, c, R, C) or b[r + k][c] != t:
                    ok = False
                    break
            if ok:
                return True
            # down-right
            ok = True
            for k in range(WIN_LEN):
                if not in_bounds(r + k, c + k, R, C) or b[r + k][c + k] != t:
                    ok = False
                    break
            if ok:
                return True
            # down-left
            ok = True
            for k in range(WIN_LEN):
                if not in_bounds(r + k, c - k, R, C) or b[r + k][c - k] != t:
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

def main():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Number of players must be between 2 and 5.")
        sys.exit(1)
    if COLS > 26:
        print("Max 26 columns supported.")
        sys.exit(1)

    b = make_board(ROWS, COLS)
    turn = random.randrange(NUM_PLAYERS)

    while True:
        print_board(b)
        t = TOKENS[turn]
        print(f"Player {t}, please enter a column:")
        col_input = input().strip().upper()
        while not valid_col_input(col_input, COLS):
            print("Invalid input. Please enter a valid column letter:")
            col_input = input().strip().upper()
        col_idx = alphabet.index(col_input)

        res = drop(b, col_idx, t)
        if res is None:
            print_board(b)
            print("Column is full. Turn lost.")
        else:
            r, c = res
            if check_win(b, t):
                print_board(b)
                print(f"Player {t} won!")
                break
            if board_full(b):
                print_board(b)
                print("It's a draw!")
                break

        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
