#!/usr/bin/env python3
"""
Connect 4 (Intro CS Edition)

- Board: 6 rows x 7 columns, columns labeled A-G
- Players: 2 to 5 players, symbols chosen from constants (X, O, V, H, M)
- Random first player
- Validates input (column letter, non-full column)
- Detects wins (4-in-a-row in any direction) and draws
- Clears screen between turns using os.system('clear') as requested

Adjust NUM_PLAYERS below to choose 2..5 players.
"""

import os
import random
import sys

# -------------------- Configuration Constants --------------------

ROWS = 6
COLS = 7
COLUMN_LABELS = "ABCDEFG"

# Allowed player symbols in turn order. Adjust or extend as needed.
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# Number of players: choose an integer from 2 to 5
NUM_PLAYERS = 2  # <<-- Change this to 2, 3, 4, or 5

# Character for empty cells
EMPTY = ' '

# -------------------- Utility Functions --------------------

def clear_screen():
    """
    Clears the terminal screen using os.system('clear') as required.
    Falls back gracefully if not available.
    """
    try:
        os.system('clear')  # As specified in the assignment
    except Exception:
        # Fallback: print blank lines
        print("\n" * 100)


def make_board(rows=ROWS, cols=COLS):
    """Create an empty game board (list of lists)."""
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Print the board with column labels.
    Top row prints first; bottom row shows the "ground" where tokens fall.
    """
    # Column labels
    print("  " + " ".join(COLUMN_LABELS))
    # Each row
    for r in range(ROWS):
        row_str = []
        for c in range(COLS):
            row_str.append(board[r][c])
        print(f"{ROWS - r} " + " ".join(row_str))
    print()  # Extra spacing


def col_label_to_index(label):
    """
    Convert a column label (A-G) to an index 0..6.
    Returns None for invalid inputs.
    """
    if not label or len(label) != 1:
        return None
    label = label.upper()
    if label in COLUMN_LABELS:
        return ord(label) - ord('A')
    return None


def get_lowest_empty_row(board, col):
    """
    Return the lowest empty row index in the given column, or None if full.
    We index rows 0..ROWS-1 from top to bottom, so search from bottom up.
    """
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            return r
    return None


def place_piece(board, col, symbol):
    """
    Attempt to place 'symbol' in column 'col'.
    Returns (row, col) on success or (None, None) if the column is full.
    """
    r = get_lowest_empty_row(board, col)
    if r is None:
        return None, None
    board[r][col] = symbol
    return r, col


def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS


def check_win(board, last_row, last_col, symbol):
    """
    Check whether placing 'symbol' at (last_row, last_col) creates a 4-in-a-row.
    Checks in all 4 directions: horizontal, vertical, two diagonals.
    """
    directions = [
        (0, 1),   # horizontal (right)
        (1, 0),   # vertical (down)
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # start with the just-placed piece

        # Scan forward
        r, c = last_row + dr, last_col + dc
        while in_bounds(r, c) and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc

        # Scan backward
        r, c = last_row - dr, last_col - dc
        while in_bounds(r, c) and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True

    return False


def board_full(board):
    """Return True if the board has no EMPTY cells in the top row of any column."""
    for c in range(COLS):
        if board[0][c] == EMPTY:
            return False
    return True


def validate_configuration():
    """
    Validate NUM_PLAYERS and PLAYER_SYMBOLS configuration at startup.
    Exits with a helpful message if invalid.
    """
    if not (2 <= NUM_PLAYERS <= 5):
        print(f"Error: NUM_PLAYERS must be between 2 and 5, got {NUM_PLAYERS}.")
        sys.exit(1)
    if len(PLAYER_SYMBOLS) < NUM_PLAYERS:
        print("Error: Not enough PLAYER_SYMBOLS for NUM_PLAYERS.")
        sys.exit(1)
    # Ensure symbols are single non-space characters
    for s in PLAYER_SYMBOLS[:NUM_PLAYERS]:
        if not isinstance(s, str) or len(s) != 1 or s == ' ':
            print("Error: Each player symbol must be a single non-space character.")
            sys.exit(1)


# -------------------- Game Loop --------------------

def prompt_for_column(current_symbol):
    """
    Prompt the current player for a column selection.
    Returns the column index (0..6) or None if input invalid.
    """
    raw = input(f"Player {current_symbol}, choose a column (A-G): ").strip()
    idx = col_label_to_index(raw)
    return idx


def main():
    validate_configuration()

    # Create players list based on NUM_PLAYERS
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]

    # Initialize game
    board = make_board()
    start_index = random.randint(0, len(players) - 1)
    current_index = start_index

    winner = None

    while True:
        clear_screen()
        print("Connect 4")
        print(f"Players: {' '.join(players)}   |   First player (random): {players[start_index]}")
        print_board(board)

        current_symbol = players[current_index]

        # Get and validate input
        try:
            col = prompt_for_column(current_symbol)
        except (EOFError, KeyboardInterrupt):
            print("\nExiting game.")
            return

        if col is None:
            print("Invalid input. Please enter a letter A-G. Press Enter to continue.")
            try:
                input()
            except Exception:
                pass
            continue

        # Attempt to place piece
        row, placed_col = place_piece(board, col, current_symbol)
        if row is None:
            print("That column is full. Press Enter to try another column.")
            try:
                input()
            except Exception:
                pass
            continue

        # Check for win
        if check_win(board, row, placed_col, current_symbol):
            winner = current_symbol
            break

        # Check for draw
        if board_full(board):
            break

        # Next player's turn
        current_index = (current_index + 1) % len(players)

    # Game over
    clear_screen()
    print("Connect 4 - Game Over")
    print_board(board)
    if winner:
        print(f"Player {winner} wins! Congratulations!")
    else:
        print("It's a draw! Well played by all.")


if __name__ == "__main__":
    main()
