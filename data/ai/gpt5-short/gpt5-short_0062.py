# Connect 4 (6x7) for 2–5 players
# Basic Python only (intro CS friendly)
# Players: X, O, V, H, M (use first NUM_PLAYERS of these)
# Random first player, input validation, win/draw checks, clear screen each turn

import os
import random

# ----- Constants you can change -----
NUM_PLAYERS = 2  # set between 2 and 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
ROWS = 6
COLS = 7
EMPTY = '.'
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
# ------------------------------------

def clear_screen():
    os.system('clear')  # per requirement

def make_board():
    board = []
    for _ in range(ROWS):
        row = []
        for _ in range(COLS):
            row.append(EMPTY)
        board.append(row)
    return board

def print_board(board):
    print("Connect 4 — 6 rows x 7 columns")
    print("Players:", " ".join(PLAYER_SYMBOLS[:NUM_PLAYERS]))
    print("Columns:", " ".join(COL_LABELS))
    for r in range(ROWS):
        line = []
        for c in range(COLS):
            line.append(board[r][c])
        print(" " + " ".join(line))
    print()

def column_from_input(text):
    # Accept A-G (case-insensitive)
    if len(text) != 1:
        return -1
    ch = text.upper()
    for i in range(COLS):
        if COL_LABELS[i] == ch:
            return i
    return -1

def column_full(board, col):
    return board[0][col] != EMPTY

def drop_piece(board, col, symbol):
    # Place in lowest empty row; return row index, or -1 if full
    if column_full(board, col):
        return -1
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            board[r][col] = symbol
            return r
    return -1

def in_bounds(r, c):
    return r >= 0 and r < ROWS and c >= 0 and c < COLS

def check_win(board, symbol):
    # Check all directions for 4-in-a-row for the given symbol
    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (1, 1),   # down-right
        (1, -1),  # down-left
    ]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                rr = r
                cc = c
                count = 0
                while count < 4 and in_bounds(rr, cc) and board[rr][cc] == symbol:
                    rr += dr
                    cc += dc
                    count += 1
                if count == 4:
                    return True
    return False

def is_draw(board):
    # Draw if no empty cells in top row (i.e., all columns full)
    for c in range(COLS):
        if board[0][c] == EMPTY:
            return False
    return True

def next_player_index(i):
    return (i + 1) % NUM_PLAYERS

def get_valid_move(board, symbol):
    while True:
        move = input(f"Player {symbol}, choose a column (A-G): ").strip()
        col = column_from_input(move)
        if col == -1:
            print("Invalid input. Enter a single letter A-G.")
            continue
        if column_full(board, col):
            print("That column is full. Choose another.")
            continue
        return col

def main():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5.")
        return
    symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]

    board = make_board()
    current = random.randrange(NUM_PLAYERS)

    while True:
        clear_screen()
        print_board(board)

        symbol = symbols[current]
        col = get_valid_move(board, symbol)

        row = drop_piece(board, col, symbol)
        # row should not be -1 because we validate, but check anyway
        if row == -1:
            print("Unexpected error: could not drop piece.")
            return

        # After move, clear and show updated board
        clear_screen()
        print_board(board)

        if check_win(board, symbol):
            print(f"Player {symbol} wins! Thanks for playing.")
            break
        if is_draw(board):
            print("It's a draw! Board is full.")
            break

        current = next_player_index(current)

if __name__ == "__main__":
    main()
