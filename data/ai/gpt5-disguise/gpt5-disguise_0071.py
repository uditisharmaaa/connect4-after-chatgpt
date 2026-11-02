import os
import random
import sys

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LEN = 4

SYMS = ["X", "O", "V", "H", "M"]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear():
    os.system('clear')

def print_board(b):
    cols = len(b[0])
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    sep = "+" + "+".join(["---"] * cols) + "+"
    print(header)
    print(sep)
    for r in range(len(b)):
        row = "|"
        for c in range(cols):
            row += " " + b[r][c] + " |"
        print(row)
        print(sep)

def get_col_input(cols):
    while True:
        s = input().strip()
        if len(s) == 0:
            print("Invalid input. Try again:")
            continue
        ch = s[0].upper()
        if not ch.isalpha():
            print("Invalid input. Try again:")
            continue
        idx = ord(ch) - ord('A')
        if idx < 0 or idx >= cols:
            print("Out of range. Try again:")
            continue
        return idx

def drop(b, col, sym):
    for r in range(len(b)-1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = sym
            return r
    return -1

def in_bounds(r, c, R, C):
    return 0 <= r < R and 0 <= c < C

def check_win(b, sym):
    R = len(b)
    C = len(b[0])
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(R):
        for c in range(C):
            if b[r][c] != sym:
                continue
            for dr, dc in dirs:
                cnt = 0
                rr, cc = r, c
                while in_bounds(rr, cc, R, C) and b[rr][cc] == sym:
                    cnt += 1
                    if cnt == WIN_LEN:
                        return True
                    rr += dr
                    cc += dc
    return False

def board_full(b):
    for r in b:
        for x in r:
            if x == " ":
                return False
    return True

def main():
    if COLS > 26:
        print("Max 26 columns supported.")
        sys.exit(1)
    players = SYMS[:NUM_PLAYERS]
    b = make_board(ROWS, COLS)
    turn = random.randint(0, NUM_PLAYERS - 1)

    clear()
    print_board(b)
    while True:
        p = players[turn]
        print(f"Player {p}, please enter a column:")
        col = get_col_input(COLS)
        row = drop(b, col, p)
        if row == -1:
            print("Column is full. Turn lost.")
        clear()
        print_board(b)
        if row != -1:
            if check_win(b, p):
                print(f"Player {p} won!")
                break
            if board_full(b):
                print("It's a draw!")
                break
        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
