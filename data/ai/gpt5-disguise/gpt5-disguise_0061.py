import os
import random
import sys

ROWS = 6
COLS = 7
NUM_PLAYERS = 2

SYMS = ["X", "O", "V", "H", "M"]

if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    print("Number of players must be between 2 and 5.")
    sys.exit(1)
if COLS < 1 or COLS > 26:
    print("Number of columns must be between 1 and 26.")
    sys.exit(1)

players = SYMS[:NUM_PLAYERS]
board = [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(b):
    os.system('clear')
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    sep = "+" + "+".join(["---"] * COLS) + "+"
    for r in range(ROWS):
        print(sep)
        row = "|" + "|".join([" {} ".format(b[r][c]) for c in range(COLS)]) + "|"
        print(row)
    print(sep)

def place(col, sym):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = sym
            return True
    return False

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(sym):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != sym:
                continue
            # right
            ok = True
            for k in range(4):
                if not in_bounds(r, c + k) or board[r][c + k] != sym:
                    ok = False
                    break
            if ok:
                return True
            # down
            ok = True
            for k in range(4):
                if not in_bounds(r + k, c) or board[r + k][c] != sym:
                    ok = False
                    break
            if ok:
                return True
            # diag down-right
            ok = True
            for k in range(4):
                if not in_bounds(r + k, c + k) or board[r + k][c + k] != sym:
                    ok = False
                    break
            if ok:
                return True
            # diag down-left
            ok = True
            for k in range(4):
                if not in_bounds(r + k, c - k) or board[r + k][c - k] != sym:
                    ok = False
                    break
            if ok:
                return True
    return False

def is_draw():
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

current = random.randint(0, NUM_PLAYERS - 1)

while True:
    print_board(board)
    sym = players[current]
    col_idx = None
    while True:
        s = input(f"Player {sym}, please enter a column: ").strip().upper()
        if len(s) != 1:
            continue
        ch = s[0]
        start = ord('A')
        end = start + COLS
        if ord(ch) < start or ord(ch) >= end:
            continue
        col_idx = ord(ch) - start
        break

    if not place(col_idx, sym):
        current = (current + 1) % NUM_PLAYERS
        continue

    if check_win(sym):
        print_board(board)
        print(f"Player {sym} won!")
        break

    if is_draw():
        print_board(board)
        print("It's a draw.")
        break

    current = (current + 1) % NUM_PLAYERS
