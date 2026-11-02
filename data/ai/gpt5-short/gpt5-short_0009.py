# Simple Connect 4 (6x7) for 2–5 players
# Columns labeled A-G, players: X O V H M
# Random starting player, input validation, win/draw detection, clears screen each turn

import os
import random

# Constants you can change
ROWS = 6
COLS = 7
COL_LABELS = "ABCDEFG"
EMPTY = "."
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2  # set between 2 and 5

def clear_screen():
    # Clears the terminal screen (Unix/macOS). Ignore errors if not supported.
    try:
        os.system('clear')
    except:
        pass

def make_board():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print("  " + " ".join(COL_LABELS))
    for r in range(ROWS):
        print(str(ROWS - r) + " " + " ".join(board[r]))
    print()

def col_from_input(s):
    s = s.strip().upper()
    if len(s) != 1:
        return -1
    if s not in COL_LABELS:
        return -1
    return COL_LABELS.index(s)

def drop_piece(board, col, symbol):
    # Place piece in the lowest empty spot in the column. Return row or -1 if full.
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            board[r][col] = symbol
            return r
    return -1

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(board, r, c):
    # Check 4-in-a-row including (r,c) in all 4 directions
    sym = board[r][c]
    if sym == EMPTY:
        return False

    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]

    for dr, dc in directions:
        count = 1

        # forward
        rr, cc = r + dr, c + dc
        while in_bounds(rr, cc) and board[rr][cc] == sym:
            count += 1
            rr += dr
            cc += dc

        # backward
        rr, cc = r - dr, c - dc
        while in_bounds(rr, cc) and board[rr][cc] == sym:
            count += 1
            rr -= dr
            cc -= dc

        if count >= 4:
            return True

    return False

def board_full(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == EMPTY:
                return False
    return True

def get_move(board, current_symbol):
    while True:
        move = input(f"Player {current_symbol}, choose a column (A-G): ").strip()
        if move == "":
            print("Please enter a column letter A-G.")
            continue
        col = col_from_input(move)
        if col == -1:
            print("Invalid input. Enter a column letter A-G.")
            continue
        if board[0][col] != EMPTY:
            print("That column is full. Try another one.")
            continue
        return col

def main():
    # Setup
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5.")
        return

    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_index = random.randrange(NUM_PLAYERS)

    board = make_board()
    winner = None

    while True:
        clear_screen()
        print_board(board)
        current_symbol = players[current_index]
        col = get_move(board, current_symbol)
        row = drop_piece(board, col, current_symbol)

        # Safety check (shouldn't happen due to validation)
        if row == -1:
            print("Unexpected error: column is full. Try again.")
            continue

        # Check win
        if check_win(board, row, col):
            clear_screen()
            print_board(board)
            print(f"Player {current_symbol} wins!")
            winner = current_symbol
            break

        # Check draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player
        current_index = (current_index + 1) % NUM_PLAYERS

    # Game over
    print("Game over.")

if __name__ == "__main__":
    main()
