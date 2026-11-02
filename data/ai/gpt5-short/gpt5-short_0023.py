#!/usr/bin/env python3
"""
Connect 4 (Intro CS version)
- Board: 6 rows x 7 columns (columns labeled A-G)
- Players: 2 to 5 players, tokens from the set ['X', 'O', 'V', 'H', 'M']
- Random starting player each game
- Validates input (column letters, column not full)
- Detects wins (horizontal, vertical, both diagonals) and draws
- Clears the screen each turn using os.system('clear')

Author: Your Name
"""

import os
import random
import sys
from typing import List, Tuple, Optional

# --------------------------
# Configuration constants
# --------------------------

ROWS = 6
COLS = 7
COLUMN_LABELS = tuple("ABCDEFG")  # Must be length COLS

# Choose between 2 and 5
NUM_PLAYERS = 2

# Available tokens in play order (first NUM_PLAYERS are used)
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']

# Whether to allow quitting by entering 'Q'
ALLOW_QUIT = True


# --------------------------
# Utility and validation
# --------------------------

def clear_screen() -> None:
    """Clear terminal screen using 'clear'; attempt 'cls' as a fallback."""
    # Primary requirement: use 'clear'
    ret = os.system('clear')
    if ret != 0:
        # Fallback for Windows or environments lacking 'clear'
        os.system('cls')


def validate_config() -> None:
    """Validate configuration constants at startup."""
    if COLS != len(COLUMN_LABELS):
        raise ValueError("COLS must match length of COLUMN_LABELS.")
    if not (2 <= NUM_PLAYERS <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5 inclusive.")
    if len(PLAYER_TOKENS) < NUM_PLAYERS:
        raise ValueError("PLAYER_TOKENS must contain at least NUM_PLAYERS symbols.")
    if len(set(PLAYER_TOKENS[:NUM_PLAYERS])) != NUM_PLAYERS:
        raise ValueError("PLAYER_TOKENS for active players must be unique.")


# --------------------------
# Board representation
# --------------------------

Board = List[List[str]]  # ROWS x COLS grid of strings (tokens or ' ')


def new_board(rows: int = ROWS, cols: int = COLS) -> Board:
    """Create an empty board with spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board: Board) -> None:
    """Display the board with column labels."""
    # Header
    print("   " + "   ".join(COLUMN_LABELS))
    # Rows from top to bottom (row 0 is top)
    for r in range(ROWS):
        row_cells = []
        for c in range(COLS):
            row_cells.append(board[r][c] if board[r][c] != ' ' else '.')
        print(" | " + " | ".join(row_cells) + " |")
    print("   " + "---" * COLS)


def column_from_input(user_input: str) -> Optional[int]:
    """
    Convert a user input string to a column index.
    Returns None if input is invalid (not A-G).
    """
    if not user_input:
        return None
    ch = user_input.strip().upper()
    if ALLOW_QUIT and ch == 'Q':
        return -1  # Signal quit
    if ch in COLUMN_LABELS:
        return COLUMN_LABELS.index(ch)
    return None


def first_empty_row(board: Board, col: int) -> Optional[int]:
    """
    Return the row index (from bottom) where a piece can be placed in the given column.
    If the column is full, return None.
    """
    # We place from bottom to top; bottom row index is ROWS - 1
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None


def is_draw(board: Board) -> bool:
    """Return True if the board is full (no spaces), indicating a draw."""
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == ' ':
                return False
    return True


# --------------------------
# Win checking
# --------------------------

def check_win(board: Board, row: int, col: int, token: str) -> bool:
    """
    Check if placing 'token' at (row, col) creates a Connect 4.
    We count contiguous tokens in four directions:
    - Horizontal (0,1)
    - Vertical (1,0)
    - Diagonal down-right (1,1)
    - Diagonal up-right (-1,1)
    """
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (-1, 1),  # diag up-right
    ]
    for dr, dc in directions:
        if count_in_direction(board, row, col, dr, dc, token) >= 4:
            return True
    return False


def count_in_direction(board: Board, row: int, col: int, dr: int, dc: int, token: str) -> int:
    """
    Count contiguous tokens including (row, col) in both positive and negative
    directions defined by (dr, dc). Returns the total length.
    """
    total = 1  # Count the current piece
    # Forward direction
    r, c = row + dr, col + dc
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == token:
        total += 1
        r += dr
        c += dc
    # Backward direction
    r, c = row - dr, col - dc
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == token:
        total += 1
        r -= dr
        c -= dc
    return total


# --------------------------
# Game loop
# --------------------------

def get_player_order() -> List[str]:
    """
    Return the tokens for active players in a round-robin order,
    with a random starting player.
    """
    active = PLAYER_TOKENS[:NUM_PLAYERS]
    start_index = random.randrange(len(active))
    # Rotate list so that random index comes first
    return active[start_index:] + active[:start_index]


def prompt_move(current_token: str) -> Optional[int]:
    """
    Prompt the current player for a column letter (A-G).
    Returns:
      - column index (0..COLS-1) if valid move chosen,
      - -1 if player chose to quit (when ALLOW_QUIT),
      - None for invalid input (to re-prompt).
    """
    prompt = f"Player {current_token}, choose a column ({'/'.join(COLUMN_LABELS)})"
    if ALLOW_QUIT:
        prompt += " or Q to quit"
    prompt += ": "
    choice = input(prompt)
    col = column_from_input(choice)
    return col


def play_game() -> None:
    """Run one full game of Connect 4."""
    board = new_board()
    turn_order = get_player_order()
    current_index = 0

    # Explain the game briefly and show the initial board
    clear_screen()
    print("Welcome to Connect 4!")
    print(f"Board: {ROWS} rows x {COLS} columns  |  Columns: {', '.join(COLUMN_LABELS)}")
    print(f"Players (in turn order this game): {' '.join(turn_order)}")
    print("(Connect four in a row: horizontal, vertical, or diagonal.)")
    if ALLOW_QUIT:
        print("Enter Q at any time to quit.\n")
    print_board(board)

    while True:
        current_token = turn_order[current_index]

        # Input loop for the current player
        while True:
            col = prompt_move(current_token)
            if col == -1:
                print("Game ended by user.")
                return
            if col is None:
                print(f"Invalid input. Please enter one of: {', '.join(COLUMN_LABELS)}.")
                continue
            # Validate column not full
            r = first_empty_row(board, col)
            if r is None:
                print(f"Column {COLUMN_LABELS[col]} is full. Choose a different column.")
                continue

            # Apply the move
            board[r][col] = current_token
            break  # valid move made

        # Clear and reprint board after the move
        clear_screen()
        print(f"Turn order: {' '.join(turn_order)}   |   Current move: Player {current_token} -> Column {COLUMN_LABELS[col]}")
        print_board(board)

        # Check for win
        if check_win(board, r, col, current_token):
            print(f"Player {current_token} wins! Congratulations!")
            return

        # Check for draw
        if is_draw(board):
            print("It's a draw! The board is full.")
            return

        # Next player's turn
        current_index = (current_index + 1) % len(turn_order)


# --------------------------
# Entry point
# --------------------------

def main() -> None:
    try:
        validate_config()
    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        play_game()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")


if __name__ == "__main__":
    main()
