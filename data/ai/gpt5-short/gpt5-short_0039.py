#!/usr/bin/env python3
"""
Connect 4 (supports 2–5 players).
- Board: 6 rows x 7 columns (A–G)
- Players: tokens from PLAYER_TOKENS limited by NUM_PLAYERS
- Random first player
- Validates input; handles full columns and bad input
- Checks wins (horizontal, vertical, diagonals) and draws
- Clears screen using os.system('clear') for a clean UI
"""

import os
import random
import sys
from typing import List, Tuple, Optional

# -----------------------------
# Configuration Constants
# -----------------------------
ROWS = 6
COLS = 7
COLUMN_LABELS = "ABCDEFG"

# Available tokens in order. Only the first NUM_PLAYERS are used.
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']

# Change this to select 2–5 players.
NUM_PLAYERS = 2  # Valid values: 2, 3, 4, or 5

# -----------------------------
# Utility Functions
# -----------------------------

def clear_screen() -> None:
    """
    Clear the terminal screen. Uses 'clear' (as required).
    Attempts 'cls' (Windows) if 'clear' isn't effective.
    """
    # Requirement explicitly says to use os.system('clear'):
    os.system('clear')
    # Fallback for Windows users if running there:
    if os.name == 'nt':
        os.system('cls')


def create_board(rows: int = ROWS, cols: int = COLS) -> List[List[str]]:
    """Create an empty board initialized with spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board: List[List[str]]) -> None:
    """
    Pretty-print the board to the terminal with column labels.
    Top row is displayed first (row 0 at the top).
    """
    print("   " + "   ".join(COLUMN_LABELS))
    print(" +---" * COLS + "+")
    for r in range(ROWS):
        row_cells = []
        for c in range(COLS):
            row_cells.append(board[r][c])
        print(" | " + " | ".join(row_cells) + " |")
        print(" +---" * COLS + "+")
    print()


def get_valid_columns(board: List[List[str]]) -> List[int]:
    """
    Return a list of column indices that are not full.
    A column is valid if its top cell (row 0) is empty.
    """
    valid = []
    for c in range(COLS):
        if board[0][c] == ' ':
            valid.append(c)
    return valid


def col_label_to_index(label: str) -> Optional[int]:
    """Convert column label (A–G) to column index, or None if invalid."""
    label = label.strip().upper()
    if len(label) != 1:
        return None
    if label in COLUMN_LABELS:
        return COLUMN_LABELS.index(label)
    return None


def drop_token(board: List[List[str]], col: int, token: str) -> Tuple[int, int]:
    """
    Drop the token into the given column.
    Returns (row, col) where the token landed.
    Assumes the column is valid (not full).
    """
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = token
            return (r, col)
    # Should never reach here if caller checked validity
    raise ValueError("Attempted to drop token in a full column.")


def in_bounds(r: int, c: int) -> bool:
    """Check if (r, c) is within the board bounds."""
    return 0 <= r < ROWS and 0 <= c < COLS


def check_win(board: List[List[str]], last_r: int, last_c: int, token: str) -> bool:
    """
    Check for a connect-4 from the last placed token.
    We count consecutive tokens in 4 directions: horizontal, vertical, both diagonals.
    """
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]

    for dr, dc in directions:
        count = 1  # include the last placed token

        # Forward direction
        r, c = last_r + dr, last_c + dc
        while in_bounds(r, c) and board[r][c] == token:
            count += 1
            r += dr
            c += dc

        # Backward direction
        r, c = last_r - dr, last_c - dc
        while in_bounds(r, c) and board[r][c] == token:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True

    return False


def check_draw(board: List[List[str]]) -> bool:
    """Return True if the board is full (no spaces in the top row)."""
    return all(cell != ' ' for cell in board[0])


def prompt_move(valid_cols: List[int], current_token: str) -> Optional[int]:
    """
    Prompt the user for a move. Returns the chosen column index, or None if user quits.
    Validates input:
      - Single letter A–G
      - Column must not be full
    """
    valid_labels = [COLUMN_LABELS[c] for c in valid_cols]
    prompt = f"Player {current_token}, choose a column ({'/'.join(valid_labels)}) or Q to quit: "
    while True:
        choice = input(prompt).strip().upper()
        if choice == 'Q':
            return None

        col_index = col_label_to_index(choice)
        if col_index is None:
            print("Invalid input. Please enter a single letter A–G corresponding to a column.")
            continue

        if col_index not in valid_cols:
            print(f"Column {COLUMN_LABELS[col_index]} is full or unavailable. Choose from: {', '.join(valid_labels)}")
            continue

        return col_index


def validate_config() -> None:
    """Validate configuration constants; exit with message if invalid."""
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if NUM_PLAYERS > len(PLAYER_TOKENS):
        print("Error: Not enough PLAYER_TOKENS for the chosen NUM_PLAYERS.")
        sys.exit(1)
    if COLS != len(COLUMN_LABELS):
        print("Error: COLS must match the length of COLUMN_LABELS.")
        sys.exit(1)


# -----------------------------
# Game Loop
# -----------------------------

def main() -> None:
    validate_config()
    tokens = PLAYER_TOKENS[:NUM_PLAYERS]

    board = create_board()

    # Randomly select first player index
    current_idx = random.randrange(NUM_PLAYERS)

    winner: Optional[str] = None

    while True:
        clear_screen()
        print(f"Connect 4 — {ROWS}x{COLS} | Players: {', '.join(tokens)}")
        print(f"Current turn: Player {tokens[current_idx]}")
        print_board(board)

        valid_cols = get_valid_columns(board)
        if not valid_cols:
            # Should be caught by check_draw too, but handle explicitly
            print("It's a draw! No more valid moves.")
            break

        move_col = prompt_move(valid_cols, tokens[current_idx])
        if move_col is None:
            print("Game ended by user. Goodbye!")
            return

        r, c = drop_token(board, move_col, tokens[current_idx])

        # Check for win
        if check_win(board, r, c, tokens[current_idx]):
            clear_screen()
            print_board(board)
            winner = tokens[current_idx]
            print(f"Player {winner} wins! Congratulations!")
            break

        # Check for draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! Board is full.")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS

    # Game over summary
    if winner is None and not check_draw(board):
        # In case exit occurred mid-game without a draw/win (user quit)
        print("Game ended.")
    # Optional replay prompt could be added here


if __name__ == "__main__":
    main()
