#!/usr/bin/env python3
"""
Connect 4 (Intro CS Version)

- Board: 6 rows x 7 columns
- Columns labeled A-G
- Supports 2 to 5 players using symbols in PLAYER_SYMBOLS (X, O, V, H, M)
- Randomly selects the first player each game
- Validates input (valid column, not full)
- Detects wins (horizontal, vertical, diagonal) and draws
- Clears the screen each turn with os.system('clear') on non-Windows systems

Author: Your Name
"""

import os
import random
import sys
from typing import List, Optional, Tuple

# ---------------------------
# Configuration Constants
# ---------------------------

ROWS: int = 6
COLS: int = 7
COLUMN_LABELS: List[str] = list("ABCDEFG")

# Order of possible player symbols; NUM_PLAYERS (below) picks from the start of this list.
PLAYER_SYMBOLS: List[str] = ["X", "O", "V", "H", "M"]

# Change this to choose how many players (2 to 5).
NUM_PLAYERS: int = 2

# ---------------------------
# Validation of configuration
# ---------------------------

if not (2 <= NUM_PLAYERS <= len(PLAYER_SYMBOLS)):
    raise ValueError(f"NUM_PLAYERS must be between 2 and {len(PLAYER_SYMBOLS)}")

ACTIVE_PLAYERS: List[str] = PLAYER_SYMBOLS[:NUM_PLAYERS]

# ---------------------------
# Utility: clear screen
# ---------------------------

def clear_screen() -> None:
    """
    Clears the terminal screen. Uses 'cls' on Windows, 'clear' otherwise.
    Requirement specified os.system('clear'), which is used on non-Windows.
    """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

# ---------------------------
# Board helpers
# ---------------------------

def create_board(rows: int = ROWS, cols: int = COLS) -> List[List[str]]:
    """Create an empty game board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board: List[List[str]]) -> None:
    """Print the board with column labels A-G."""
    # Column headers
    print("  " + " ".join(COLUMN_LABELS))
    # Rows
    for r in range(ROWS):
        row_str = []
        for c in range(COLS):
            row_str.append(board[r][c])
        print("| " + " ".join(row_str))
    print()  # trailing newline

def column_label_to_index(label: str) -> Optional[int]:
    """Convert a column label (A-G) to its index 0-6. Returns None if invalid."""
    label = label.strip().upper()
    if label in COLUMN_LABELS:
        return COLUMN_LABELS.index(label)
    return None

def find_drop_row(board: List[List[str]], col: int) -> Optional[int]:
    """
    Given a column index, find the lowest empty row index to drop a piece.
    Returns None if the column is full.
    """
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

# ---------------------------
# Win detection
# ---------------------------

def in_bounds(r: int, c: int) -> bool:
    return 0 <= r < ROWS and 0 <= c < COLS

def count_in_direction(board: List[List[str]], start: Tuple[int, int], dr: int, dc: int, symbol: str) -> int:
    """
    Count how many consecutive 'symbol' cells starting from (start) moving in direction (dr, dc),
    including the starting cell.
    """
    r, c = start
    count = 0
    while in_bounds(r, c) and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    return count

def is_winning_move(board: List[List[str]], last_row: int, last_col: int, symbol: str) -> bool:
    """
    Check if placing 'symbol' at (last_row, last_col) created a connect-4.
    We check 4 directions: horizontal, vertical, and two diagonals.
    """
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for dr, dc in directions:
        # Count both directions from the last piece (to cover both sides)
        total = (
            count_in_direction(board, (last_row, last_col), dr, dc, symbol) +
            count_in_direction(board, (last_row, last_col), -dr, -dc, symbol) - 1
        )
        if total >= 4:
            return True
    return False

def is_draw(board: List[List[str]]) -> bool:
    """A draw occurs if the top row has no empty spaces (board is full)."""
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

# ---------------------------
# Input handling
# ---------------------------

def get_player_move(player_symbol: str, board: List[List[str]]) -> int:
    """
    Prompt the current player to select a valid column.
    Returns a valid column index (0..6). Re-prompts on invalid input.
    Allows 'Q' or 'QUIT' to exit the game.
    """
    while True:
        user_input = input(f"Player {player_symbol}, choose a column (A-G) or Q to quit: ").strip()

        if user_input.upper() in ("Q", "QUIT"):
            print("Quitting game. Goodbye!")
            sys.exit(0)

        col = column_label_to_index(user_input)
        if col is None:
            print("Invalid column. Please enter a letter A-G.")
            continue

        drop_row = find_drop_row(board, col)
        if drop_row is None:
            print(f"Column {COLUMN_LABELS[col]} is full. Choose another column.")
            continue

        return col

# ---------------------------
# Main game loop
# ---------------------------

def main() -> None:
    # Initialize
    board = create_board()
    # Randomize starting player index
    start_index = random.randrange(len(ACTIVE_PLAYERS))
    turn_order = ACTIVE_PLAYERS[:]  # copy
    # Rotate so the randomly chosen player goes first
    turn_order = turn_order[start_index:] + turn_order[:start_index]

    current_index = 0

    clear_screen()
    print("Welcome to Connect 4!")
    print(f"Players: {', '.join(turn_order)}")
    print_board(board)

    try:
        while True:
            current_player = turn_order[current_index]
            col = get_player_move(current_player, board)
            row = find_drop_row(board, col)
            assert row is not None, "Invariant: find_drop_row should not return None after validation."

            # Place piece
            board[row][col] = current_player

            # Refresh display
            clear_screen()
            print_board(board)

            # Check win/draw
            if is_winning_move(board, row, col, current_player):
                print(f"Player {current_player} wins! Congratulations!")
                break

            if is_draw(board):
                print("It's a draw! No more moves possible.")
                break

            # Next player's turn
            current_index = (current_index + 1) % len(turn_order)

    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")

if __name__ == "__main__":
    main()
