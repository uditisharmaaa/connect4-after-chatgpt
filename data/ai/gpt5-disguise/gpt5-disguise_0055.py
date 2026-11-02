import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2

TOKENS = ["X", "O", "V", "H", "M"]

if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    NUM_PLAYERS = 2
if COLS > 26:
    COLS = 26

players = TOKENS[:NUM_PLAYERS]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(b):
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    sep = "+" + "+".join(["---"] * COLS) + "+"
    for r in range(ROWS):
        print(sep)
        row_str = "|"
        for c in range(COLS):
            row_str += " " + b[r][c] + " |"
        print(row_str)
    print(sep)

def drop(b, col, t):
    for r in range(ROWS - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = t
            return r
    return None

def check_win(b, t):
    for r in range(ROWS):
        for c in range(COLS - 3):
            if b[r][c] == t and b[r][c+1] == t and b[r][c+2] == t and b[r][c+3] == t:
                return True
    for c in range(COLS):
        for r in range(ROWS - 3):
            if b[r][c] == t and b[r+1][c] == t and b[r+2][c] == t and b[r+3][c] == t:
                return True
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if b[r][c] == t and b[r+1][c+1] == t and b[r+2][c+2] == t and b[r+3][c+3] == t:
                return True
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if b[r][c] == t and b[r-1][c+1] == t and b[r-2][c+2] == t and b[r-3][c+3] == t:
                return True
    return False

def board_full(b):
    for r in range(ROWS):
        for c in range(COLS):
            if b[r][c] == " ":
                return False
    return True

board = make_board(ROWS, COLS)
current = random.randrange(NUM_PLAYERS)
winner = None
draw = False

while True:
    os.system('clear')
    print_board(board)
    if winner is not None:
        print(f"Player {winner} won!")
        break
    if draw:
        print("Game is a draw!")
        break

    p = players[current]
    print(f"Player {p}, please enter a column:")
    col_input = input().strip().upper()

    valid = False
    while not valid:
        if len(col_input) == 1 and 'A' <= col_input <= chr(ord('A') + COLS - 1):
            valid = True
        else:
            print(f"Invalid input. Please enter a column between A and {chr(ord('A') + COLS - 1)}:")
            col_input = input().strip().upper()

    col_idx = ord(col_input) - ord('A')
    row_idx = drop(board, col_idx, p)
    if row_idx is None:
        print("Column is full. Turn lost.")
        input("Press Enter to continue...")
        current = (current + 1) % NUM_PLAYERS
        continue

    if check_win(board, p):
        winner = p
    elif board_full(board):
        draw = True
    else:
        current = (current + 1) % NUM_PLAYERS
