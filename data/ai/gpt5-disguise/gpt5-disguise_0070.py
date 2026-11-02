import os
import random
import sys

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(board):
    os.system('clear')
    letters = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(letters))
    sep = "+" + "+".join(["---"] * len(board[0])) + "+"
    for r in range(len(board)):
        print(sep)
        row = "|"
        for c in range(len(board[0])):
            row += " " + board[r][c] + " |"
        print(row)
    print(sep)

def drop_token(board, col_idx, token):
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = token
            return True
    return False

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, token):
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            # right
            if c + 3 < cols and all(board[r][c + k] == token for k in range(4)):
                return True
            # down
            if r + 3 < rows and all(board[r + k][c] == token for k in range(4)):
                return True
            # down-right
            if r + 3 < rows and c + 3 < cols and all(board[r + k][c + k] == token for k in range(4)):
                return True
            # down-left
            if r + 3 < rows and c - 3 >= 0 and all(board[r + k][c - k] == token for k in range(4)):
                return True
    return False

def board_full(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def valid_col_input(s, cols):
    if len(s) != 1:
        return False
    if not s.isalpha():
        return False
    ch = s.upper()
    idx = ord(ch) - ord('A')
    return 0 <= idx < cols

def main():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5.")
        return
    if COLS > 26:
        print("Max 26 columns supported.")
        return

    players = TOKENS[:NUM_PLAYERS]
    board = make_board(ROWS, COLS)
    current = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)

    while True:
        token = players[current]
        col_input = input(f"Player {token}, please enter a column: ").strip().upper()
        while not valid_col_input(col_input, COLS):
            print_board(board)
            col_input = input(f"Player {token}, please enter a column: ").strip().upper()

        col_idx = ord(col_input) - ord('A')
        placed = drop_token(board, col_idx, token)

        print_board(board)

        if placed:
            if check_win(board, token):
                print(f"Player {token} won!")
                break
            if board_full(board):
                print("It's a draw!")
                break
        # if not placed, turn is lost
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
