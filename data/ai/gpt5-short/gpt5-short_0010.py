# Connect 4 (6x7) for 2–5 players
# - Columns labeled A–G
# - Players use tokens from TOKENS (X, O, V, H, M)
# - Number of active players set by NUM_PLAYERS (2–5)
# - Random first player, input validation, win/draw detection
# - Clears screen with os.system('clear') each turn
#
# Run this file with Python 3.
# You can change NUM_PLAYERS to 2..5 before running.

import os
import random
import sys

# -------------------- Configuration Constants --------------------

ROWS = 6
COLS = 7
COLUMN_LABELS = "ABCDEFG"

# Tokens for up to 5 players (do not use spaces)
TOKENS = ['X', 'O', 'V', 'H', 'M']

# Number of players: set between 2 and 5 (inclusive)
NUM_PLAYERS = 2  # Change to 3, 4, or 5 if you want more players


# -------------------- Utility Functions --------------------

def clear_screen():
    """
    Clear the terminal screen.
    Uses 'clear' as required. If that fails (e.g., non-POSIX),
    attempts 'cls' as a basic fallback.
    """
    # Primary requirement:
    code = os.system('clear')
    # Basic fallback (optional, won't run on some systems):
    if code != 0:
        os.system('cls')


def create_board(rows, cols):
    """Create an empty game board as a list of lists filled with spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Print the board with column labels on top.
    The top row of the board is index 0, bottom is ROWS-1.
    """
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    # Print horizontal line
    print(" +" + "---+" * COLS)

    for r in range(ROWS):
        row_cells = []
        for c in range(COLS):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print(" +" + "---+" * COLS)


def column_from_input(user_input):
    """
    Convert a user input string (like 'A'..'G') to a column index (0..6).
    Returns None if invalid.
    """
    if not user_input:
        return None
    letter = user_input.strip().upper()
    if len(letter) != 1:
        return None
    if letter in COLUMN_LABELS:
        return COLUMN_LABELS.index(letter)
    return None


def drop_piece(board, col, token):
    """
    Attempt to drop a piece (token) into the given column.
    The piece falls to the lowest available spot in that column.
    Returns the row index where the piece landed, or None if the column is full.
    """
    # Start from bottom row and go upward
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = token
            return r
    return None  # Column is full


def in_bounds(r, c):
    """Check if (r, c) is within the board."""
    return 0 <= r < ROWS and 0 <= c < COLS


def check_win(board, last_row, last_col, token):
    """
    Check if placing token at (last_row, last_col) creates a four-in-a-row.
    We check 4 directions: horizontal, vertical, and two diagonals.
    """
    directions = [
        (0, 1),   # Horizontal (right)
        (1, 0),   # Vertical (down)
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # Include the last placed piece

        # Check one direction (positive step)
        r, c = last_row + dr, last_col + dc
        while in_bounds(r, c) and board[r][c] == token:
            count += 1
            r += dr
            c += dc

        # Check the opposite direction (negative step)
        r, c = last_row - dr, last_col - dc
        while in_bounds(r, c) and board[r][c] == token:
            count += 1
            r -= dr
            c -= dc

        # Win if 4 or more in a row
        if count >= 4:
            return True

    return False


def board_full(board):
    """Return True if the board has no empty spaces."""
    for c in range(COLS):
        if board[0][c] == ' ':
            # If the top cell is empty, the column is not full -> board not full
            return False
    return True


def get_valid_move(board, current_token):
    """
    Prompt the current player to enter a valid move.
    Valid move is a column letter A-G that is not full.
    Keeps asking until a valid move is entered.
    """
    while True:
        user_input = input(f"Player {current_token}, choose a column (A-G): ").strip()
        col = column_from_input(user_input)
        if col is None:
            print("Invalid input. Please enter a single letter A-G.")
            continue
        # Check if column still has space
        if board[0][col] != ' ':
            print(f"Column {COLUMN_LABELS[col]} is full. Choose a different column.")
            continue
        return col


# -------------------- Main Game Loop --------------------

def main():
    # Validate configuration
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if NUM_PLAYERS > len(TOKENS):
        print("Error: Not enough tokens provided for the number of players.")
        sys.exit(1)

    players = TOKENS[:NUM_PLAYERS]  # Use the first NUM_PLAYERS tokens
    board = create_board(ROWS, COLS)

    # Randomly choose a starting player
    current_index = random.randrange(NUM_PLAYERS)

    while True:
        clear_screen()
        print_board(board)
        current_token = players[current_index]
        print(f"Players: {', '.join(players)}")
        print(f"Current player: {current_token}")

        # Get a valid move and drop the piece
        col = get_valid_move(board, current_token)
        row = drop_piece(board, col, current_token)

        # Safety check: row should never be None because we validated the column is not full
        if row is None:
            print("Unexpected error: Column is full after validation.")
            sys.exit(1)

        # After placing, check for win or draw
        if check_win(board, row, col, current_token):
            clear_screen()
            print_board(board)
            print(f"Player {current_token} wins! Congratulations!")
            break

        if board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw! No more moves possible.")
            break

        # Advance to the next player
        current_index = (current_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
