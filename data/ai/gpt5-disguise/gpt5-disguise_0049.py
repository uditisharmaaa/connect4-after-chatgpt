import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def make_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear():
    os.system('clear')

def print_board(board):
    cols = len(board[0])
    letters = string.ascii_uppercase[:cols]
    print("  " + "   ".join(letters))
    line = "+" + "+".join(["---"] * cols) + "+"
    for r in range(len(board)):
        print(line)
        row = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row)
    print(line)

def valid_column_input(s, cols):
    if len(s) != 1:
        return False
    if s < 'A' or s >= chr(ord('A') + cols):
        return False
    return True

def drop_token(board, col, token):
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r
    return None

def check_winner(board, token):
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols - 3):
            if board[r][c] == token and board[r][c+1] == token and board[r][c+2] == token and board[r][c+3] == token:
                return True
    for r in range(rows - 3):
        for c in range(cols):
            if board[r][c] == token and board[r+1][c] == token and board[r+2][c] == token and board[r+3][c] == token:
                return True
    for r in range(rows - 3):
        for c in range(cols - 3):
            if board[r][c] == token and board[r+1][c+1] == token and board[r+2][c+2] == token and board[r+3][c+3] == token:
                return True
    for r in range(3, rows):
        for c in range(cols - 3):
            if board[r][c] == token and board[r-1][c+1] == token and board[r-2][c+2] == token and board[r-3][c+3] == token:
                return True
    return False

def board_full(board):
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = make_board(ROWS, COLS)
    current = random.randint(0, NUM_PLAYERS - 1)
    while True:
        clear()
        print_board(board)
        print(f"Player {TOKENS[current]}, please enter a column:")
        col_input = input().strip().upper()
        while not valid_column_input(col_input, COLS):
            clear()
            print_board(board)
            print(f"Player {TOKENS[current]}, please enter a column:")
            col_input = input().strip().upper()
        col_index = ord(col_input) - ord('A')
        placed_row = drop_token(board, col_index, TOKENS[current])
        if placed_row is None:
            current = (current + 1) % NUM_PLAYERS
            continue
        if check_winner(board, TOKENS[current]):
            clear()
            print_board(board)
            print(f"Player {TOKENS[current]} won!")
            break
        if board_full(board):
            clear()
            print_board(board)
            print("It's a draw!")
            break
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
