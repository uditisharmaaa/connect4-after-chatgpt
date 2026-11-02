import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2

TOKENS_ALL = ["X", "O", "V", "H", "M"]
TOKENS = TOKENS_ALL[:NUM_PLAYERS]

if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    print("NUM_PLAYERS must be between 2 and 5.")
    exit(1)
if COLS > 26 or COLS < 1 or ROWS < 1:
    print("Board size invalid (max 26 columns).")
    exit(1)

def clear():
    os.system('clear')

def print_board(b):
    clear()
    headers = "  " + "   ".join(chr(ord('A') + i) for i in range(COLS))
    line = "+" + "---+" * COLS
    print(headers)
    for r in range(ROWS):
        print(line)
        row = "|"
        for c in range(COLS):
            row += " " + b[r][c] + " |"
        print(row)
    print(line)

def place(b, col, t):
    for r in range(ROWS - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = t
            return True
    return False

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
            if b[r][c] == t and b[r+1][c] == t and b[r+2][c] == t and b[r+3][c] == t:
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

def main():
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    current = random.randrange(NUM_PLAYERS)
    print_board(board)

    while True:
        token = TOKENS[current]
        col_input = ""
        while True:
            col_input = input(f"Player {token}, please enter a column: ").strip().upper()
            if len(col_input) == 1 and 'A' <= col_input <= 'Z':
                col = ord(col_input) - ord('A')
                if 0 <= col < COLS:
                    break
            # keep asking until valid
        placed = place(board, col, token)
        print_board(board)
        if not placed:
            # turn lost
            pass
        else:
            if check_win(board, token):
                print(f"Player {token} won!")
                break
            if board_full(board):
                print("Game is a draw.")
                break
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
