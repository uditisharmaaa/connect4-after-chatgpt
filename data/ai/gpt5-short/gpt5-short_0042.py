#!/usr/bin/env python3
"""
Connect 4 (6 rows x 7 columns) for terminal.

- Columns labeled A-G
- Supports 2 to 5 players (symbols: X, O, V, H, M) set by constants
- Random first player
- Validates input
- Checks wins and draws
- Clears screen with os.system('clear')
"""

import os
import random
import sys

# ----------------------------
# Configuration (edit these)
# ----------------------------
NUM_PLAYERS = 2          # Set between 2 and 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Available symbols for up to 5 players
EMPTY = ' '              # Character used for empty board cells

# ----------------------------
# Constants
# ----------------------------
ROWS = 6
COLS = 7
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
LABEL_TO_COL = {label: idx for idx, label in enumerate(COL_LABELS)}

# ----------------------------
# Utility functions
# ----------------------------

def clear_screen():
    """Clear the terminal screen (Unix/macOS)."""
    os.system('clear')


def create_board(rows=ROWS, cols=COLS):
    """Create an empty board represented as a list of lists."""
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]


def print_board(board, active_players):
    """Print the board with column headers and current players."""
    # Column header
    print("   " + "   ".join(COL_LABELS))
    print(" +" + "---+" * COLS)

    # Each row
    for r in range(ROWS):
        row_cells = []
        for c in range(COLS):
            row_cells.append(board[r][c])
        print(" | " + " | ".join(row_cells) + " |")
        print(" +" + "---+" * COLS)

    # Show which symbols are in play
    print("Players:", " ".join(active_players))


def get_column_input(prompt):
    """
    Read and validate a column input from user.
    Accepts A-G (case-insensitive). Re-prompts until valid.
    """
    while True:
        choice = input(prompt).strip().upper()
        if choice in LABEL_TO_COL:
            return LABEL_TO_COL[choice]
        print("Invalid input. Please enter a column letter A-G.")


def find_drop_row(board, col):
    """
    Find the lowest available row in a given column.
    Returns the row index if available, otherwise returns None if the column is full.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            return row
    return None


def drop_piece(board, col, symbol):
    """
    Drop a piece with 'symbol' into the given column.
    Returns the (row, col) position where the piece landed, or None if column is full.
    """
    row = find_drop_row(board, col)
    if row is None:
        return None
    board[row][col] = symbol
    return (row, col)


def in_bounds(r, c):
    """Check if (r, c) is within the board boundaries."""
    return 0 <= r < ROWS and 0 <= c < COLS


def check_win(board, r, c, sym):
    """
    Check if placing 'sym' at (r, c) creates a connect-4.
    We check 4 directions: horizontal, vertical, and two diagonals.
    """
    # Directions: (dr, dc)
    directions = [
        (0, 1),   # horizontal (right)
        (1, 0),   # vertical (down)
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # include the placed piece

        # Count forward direction
        rr, cc = r + dr, c + dc
        while in_bounds(rr, cc) and board[rr][cc] == sym:
            count += 1
            rr += dr
            cc += dc

        # Count backward direction
        rr, cc = r - dr, c - dc
        while in_bounds(rr, cc) and board[rr][cc] == sym:
            count += 1
            rr -= dr
            cc -= dc

        if count >= 4:
            return True

    return False


def is_draw(board):
    """The game is a draw if the top row has no empty cells."""
    return all(board[0][c] != EMPTY for c in range(COLS))


def next_player_index(current, total):
    """Get the next player's index, wrapping around."""
    return (current + 1) % total


# ----------------------------
# Main game loop
# ----------------------------

def main():
    # Validate configuration
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if NUM_PLAYERS > len(PLAYER_SYMBOLS):
        print("Error: Not enough PLAYER_SYMBOLS for the number of players.")
        sys.exit(1)

    active_players = PLAYER_SYMBOLS[:NUM_PLAYERS]  # Use the first N symbols
    board = create_board()

    # Pick a random starting player
    current_idx = random.randrange(NUM_PLAYERS)

    # Game loop
    while True:
        clear_screen()
        print_board(board, active_players)
        current_symbol = active_players[current_idx]
        print(f"Player {current_symbol}'s turn.")

        # Get a valid, non-full column
        while True:
            col = get_column_input("Choose a column (A-G): ")
            drop_pos = drop_piece(board, col, current_symbol)
            if drop_pos is not None:
                break
            print("That column is full. Please choose a different column.")

        row, col = drop_pos

        # Check for win
        if check_win(board, row, col, current_symbol):
            clear_screen()
            print_board(board, active_players)
            print(f"Player {current_symbol} wins! Congratulations!")
            break

        # Check for draw
        if is_draw(board):
            clear_screen()
            print_board(board, active_players)
            print("It's a draw!")
            break

        # Next player's turn
        current_idx = next_player_index(current_idx, NUM_PLAYERS)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
