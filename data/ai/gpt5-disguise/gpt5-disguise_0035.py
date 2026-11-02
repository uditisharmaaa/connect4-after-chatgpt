import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2

SYMS = ["X", "O", "V", "H", "M"]

if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    NUM_PLAYERS = 2
if COLS > 26:
    COLS = 26

players = SYMS[:NUM_PLAYERS]

board = [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board():
    os.system('clear')
    letters = string.ascii_uppercase[:COLS]
    print("  " + "   ".join(list(letters)))
    print("+---" * COLS + "+")
    for r in range(ROWS):
        row = "|"
        for c in range(COLS):
            row += " " + board[r][c] + " |"
        print(row)
        print("+---" * COLS + "+")

def drop_piece(col, sym):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = sym
            return r, col
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_dir(r, c, dr, dc, sym):
    count = 0
    for i in range(4):
        rr = r + dr * i
        cc = c + dc * i
        if not in_bounds(rr, cc):
            return False
        if board[rr][cc] != sym:
            return False
        count += 1
    return count == 4

def check_win(sym):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != sym:
                continue
            if check_dir(r, c, 0, 1, sym):
                return True
            if check_dir(r, c, 1, 0, sym):
                return True
            if check_dir(r, c, 1, 1, sym):
                return True
            if check_dir(r, c, 1, -1, sym):
                return True
    return False

def is_draw():
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

current = random.randint(0, NUM_PLAYERS - 1)
print_board()

while True:
    sym = players[current]
    letters = string.ascii_uppercase[:COLS]
    col_input = ""
    while True:
        col_input = input(f"Player {sym}, please enter a column: ").strip()
        if len(col_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        col_input = col_input.upper()
        if col_input not in letters:
            print("Invalid column. Please enter a valid column letter.")
            continue
        break

    col_index = letters.index(col_input)
    placed = drop_piece(col_index, sym)
    print_board()

    if placed is None:
        print("Column is full. Turn lost.")
    else:
        if check_win(sym):
            print(f"Player {sym} won!")
            break
        if is_draw():
            print("Draw!")
            break

    current = (current + 1) % NUM_PLAYERS
