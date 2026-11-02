import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2

SYMS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def make_board(r, c):
    return [[' ' for _ in range(c)] for _ in range(r)]

def clear():
    os.system('clear')

def print_board(b):
    clear()
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(COLS))
    print(header)
    sep = "+" + "+".join(["---"] * COLS) + "+"
    for r in range(ROWS):
        print(sep)
        row = "|" + "|".join(f" {b[r][c]} " for c in range(COLS)) + "|"
        print(row)
    print(sep)

def full(b):
    for r in range(ROWS):
        for c in range(COLS):
            if b[r][c] == ' ':
                return False
    return True

def check_win(b, s):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if b[r][c] == s and b[r][c+1] == s and b[r][c+2] == s and b[r][c+3] == s:
                return True
    # vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if b[r][c] == s and b[r+1][c] == s and b[r+2][c] == s and b[r+3][c] == s:
                return True
    # diag down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if b[r][c] == s and b[r+1][c+1] == s and b[r+2][c+2] == s and b[r+3][c+3] == s:
                return True
    # diag up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if b[r][c] == s and b[r-1][c+1] == s and b[r-2][c+2] == s and b[r-3][c+3] == s:
                return True
    return False

def get_col_input(sym):
    while True:
        inp = input(f"Player {sym}, please enter a column: ").strip().upper()
        if len(inp) != 1:
            continue
        ch = inp[0]
        if 'A' <= ch <= chr(ord('A') + COLS - 1):
            return ord(ch) - ord('A')

def main():
    board = make_board(ROWS, COLS)
    current = random.randrange(NUM_PLAYERS)
    print_board(board)
    while True:
        sym = SYMS[current]
        col = get_col_input(sym)
        placed = False
        for r in range(ROWS - 1, -1, -1):
            if board[r][col] == ' ':
                board[r][col] = sym
                placed = True
                break
        if not placed:
            print_board(board)
            print("Column is full. Turn lost.")
            current = (current + 1) % NUM_PLAYERS
            continue
        print_board(board)
        if check_win(board, sym):
            print(f"Player {sym} won!")
            break
        if full(board):
            print("The game is a draw.")
            break
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
