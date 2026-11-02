#!/usr/bin/env python3
import os
import random
import sys

# -------------------- Configuration --------------------
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
EMPTY = '.'

# Set number of players between 2 and 5 inclusive
NUM_PLAYERS = 2  # change to 3, 4, or 5 to allow more players
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # in order of turn rotation

# -------------------- Helpers --------------------
def clear_screen():
    # Uses 'clear' as requested
    os.system('clear')

def make_board():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print('  ' + ' '.join(COLUMN_LABELS))
    for r in range(ROWS):
        print(str(ROWS - r) + ' ' + ' '.join(board[r]))
    print()

def col_from_input(s):
    s = s.strip().upper()
    if len(s) != 1:
        return None
    if s in COLUMN_LABELS:
        return COLUMN_LABELS.index(s)
    return None

def get_lowest_empty_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            return r
    return None

def drop_piece(board, col, symbol):
    r = get_lowest_empty_row(board, col)
    if r is None:
        return None
    board[r][col] = symbol
    return r

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def count_direction(board, r, c, dr, dc, symbol):
    count = 0
    rr, cc = r, c
    while in_bounds(rr, cc) and board[rr][cc] == symbol:
        count += 1
        rr += dr
        cc += dc
    return count

def check_win_from(board, r, c, symbol):
    # Check all four directions (combine forward and backward, subtract 1 to avoid double count of origin)
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        total = (
            count_direction(board, r, c, dr, dc, symbol) +
            count_direction(board, r, c, -dr, -dc, symbol) - 1
        )
        if total >= 4:
            return True
    return False

def is_draw(board):
    for c in range(COLS):
        if board[0][c] == EMPTY:
            return False
    return True

def validate_setup():
    n = NUM_PLAYERS
    if not (2 <= n <= 5):
        print(f"NUM_PLAYERS must be between 2 and 5, got {n}.")
        sys.exit(1)
    if len(PLAYER_SYMBOLS) < n:
        print("PLAYER_SYMBOLS does not have enough entries.")
        sys.exit(1)
    # Ensure symbols are single non-empty and unique among first n
    used = PLAYER_SYMBOLS[:n]
    if len(set(used)) != len(used) or any(len(s) != 1 or s == EMPTY for s in used):
        print("PLAYER_SYMBOLS must contain unique single-character symbols not equal to EMPTY.")
        sys.exit(1)

# -------------------- Game Loop --------------------
def main():
    validate_setup()
    board = make_board()

    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_index = random.randrange(len(players))  # random first player

    print_board(board)
    print(f"Starting player (random): {players[current_index]}")
    input("Press Enter to begin...")

    while True:
        symbol = players[current_index]
        while True:
            print_board(board)
            print(f"Player {symbol}'s turn.")
            choice = input("Choose column (A-G): ").strip()
            col = col_from_input(choice)
            if col is None:
                print("Invalid input. Enter a single letter A-G. Press Enter to try again.")
                input()
                continue
            row = get_lowest_empty_row(board, col)
            if row is None:
                print(f"Column {COLUMN_LABELS[col]} is full. Press Enter to choose another column.")
                input()
                continue
            # Valid move
            drop_row = drop_piece(board, col, symbol)
            break

        print_board(board)

        # Check win
        if check_win_from(board, drop_row, col, symbol):
            print(f"Player {symbol} wins!")
            break

        # Check draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player
        current_index = (current_index + 1) % len(players)

    print("Game over.")

if __name__ == "__main__":
    main()
