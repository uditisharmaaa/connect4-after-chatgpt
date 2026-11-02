import random
import os
import string

ROWS = 6
COLS = 7
MAX_COLS = 26
TOKENS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2

if COLS > MAX_COLS:
    COLS = MAX_COLS
if NUM_PLAYERS < 2:
    NUM_PLAYERS = 2
if NUM_PLAYERS > 5:
    NUM_PLAYERS = 5

players = TOKENS[:NUM_PLAYERS]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(board):
    os.system('clear')
    letters = list(string.ascii_uppercase[:len(board[0])])
    print("  " + "   ".join(letters))
    sep = "+" + "+".join(["---"] * len(board[0])) + "+"
    for r in range(len(board)):
        print(sep)
        row_str = "|"
        for c in range(len(board[0])):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(sep)

def drop_piece(board, col, token):
    for r in range(len(board)-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
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
            ok = True
            for k in range(4):
                if not in_bounds(r, c+k, rows, cols) or board[r][c+k] != token:
                    ok = False
                    break
            if ok:
                return True
            # down
            ok = True
            for k in range(4):
                if not in_bounds(r+k, c, rows, cols) or board[r+k][c] != token:
                    ok = False
                    break
            if ok:
                return True
            # diag down-right
            ok = True
            for k in range(4):
                if not in_bounds(r+k, c+k, rows, cols) or board[r+k][c+k] != token:
                    ok = False
                    break
            if ok:
                return True
            # diag down-left
            ok = True
            for k in range(4):
                if not in_bounds(r+k, c-k, rows, cols) or board[r+k][c-k] != token:
                    ok = False
                    break
            if ok:
                return True
    return False

def board_full(board):
    for r in board:
        for v in r:
            if v == " ":
                return False
    return True

def main():
    board = make_board(ROWS, COLS)
    current = random.randrange(NUM_PLAYERS)
    print_board(board)
    while True:
        token = players[current]
        print(f"Player {token}, please enter a column:")
        col_letter = input().strip()
        while True:
            if len(col_letter) != 1:
                print("Invalid input. Please enter a single letter for the column:")
                col_letter = input().strip()
                continue
            col_letter = col_letter.upper()
            letters = string.ascii_uppercase[:COLS]
            if col_letter not in letters:
                print("Invalid column. Please enter a valid column letter:")
                col_letter = input().strip()
                continue
            break
        col_idx = ord(col_letter) - ord('A')
        placed = drop_piece(board, col_idx, token)
        print_board(board)
        if not placed:
            print("Column is full. Turn lost.")
        else:
            if check_win(board, token):
                print(f"Player {token} won!")
                break
            if board_full(board):
                print("It's a draw!")
                break
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
