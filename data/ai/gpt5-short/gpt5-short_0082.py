#!/usr/bin/env python3
# Connect 4 (6 rows x 7 columns) for 2–5 players.
# - Columns labeled A–G
# - Players use tokens from PLAYER_TOKENS (in order)
# - Number of players set by NUM_PLAYERS constant
# - Random first player
# - Input validation (column exists, not full)
# - Win and draw detection
# - Clears screen with os.system('clear')
#
# Suitable for an Intro CS class, with explanatory comments.

import os
import random
import sys
from typing import List, Optional, Tuple

# -------------------- Configuration --------------------
ROWS = 6
COLS = 7
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]  # ['A', 'B', ..., 'G']

# Tokens available for players, in order they will be assigned.
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players supported

# Choose how many players will play (between 2 and 5)
NUM_PLAYERS = 2  # Change to 3, 4, or 5 if desired

# Character for an empty cell on the board
EMPTY = '.'

# -------------------- Utility / Display --------------------
def clear_screen() -> None:
    """Clear the terminal screen."""
    # Requirement specifies using os.system('clear')
    os.system('clear')


def make_board(rows: int = ROWS, cols: int = COLS) -> List[List[str]]:
    """Create a new empty board as a list of lists."""
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]


def print_board(board: List[List[str]]) -> None:
    """Print the board with column labels. Top row printed first."""
    # Print column headers (A-G)
    print("   " + " ".join(COLUMN_LABELS))
    # Print each row with an index (optional) or just the contents
    for r in range(ROWS):
        # Row contents
        print(f"{r+1:2d} " + " ".join(board[r]))
    print()  # Extra newline for spacing


# -------------------- Game Logic --------------------
def next_open_row(board: List[List[str]], col: int) -> Optional[int]:
    """
    Return the row index where a piece will land for the given column,
    or None if the column is full.
    We fill from the bottom (ROWS-1) up to 0.
    """
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            return r
    return None


def drop_piece(board: List[List[str]], row: int, col: int, token: str) -> None:
    """Place a player's token in the specified cell."""
    board[row][col] = token


def in_bounds(r: int, c: int) -> bool:
    """Check if row/column is inside the board."""
    return 0 <= r < ROWS and 0 <= c < COLS


def check_direction(board: List[List[str]], start_r: int, start_c: int,
                    dr: int, dc: int, token: str) -> bool:
    """
    Check for 4 in a row starting at (start_r, start_c) moving by (dr, dc).
    Returns True if we find 4 consecutive 'token' cells including the start.
    """
    count = 0
    r, c = start_r, start_c
    for _ in range(4):
        if not in_bounds(r, c) or board[r][c] != token:
            return False
        count += 1
        r += dr
        c += dc
    return count == 4


def check_win(board: List[List[str]], token: str) -> bool:
    """
    Check if the given token has 4 in a row anywhere on the board.
    We try all start cells and 4 directions:
      - Horizontal (0, +1)
      - Vertical (+1, 0)
      - Diagonal down-right (+1, +1)
      - Diagonal down-left (+1, -1)
    """
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                if check_direction(board, r, c, dr, dc, token):
                    return True
    return False


def board_full(board: List[List[str]]) -> bool:
    """Return True if there are no EMPTY cells in the top row (i.e., all columns full)."""
    return all(board[0][c] != EMPTY for c in range(COLS))


def parse_column_input(user_input: str) -> Optional[int]:
    """
    Convert a user input (e.g., 'A' or 'g') to a column index.
    Return None if input is invalid.
    """
    if not user_input:
        return None
    ch = user_input.strip().upper()
    if len(ch) != 1:
        return None
    if ch in COLUMN_LABELS:
        return COLUMN_LABELS.index(ch)
    return None


# -------------------- Game Loop --------------------
def play_game() -> None:
    """Run the main game loop."""
    # Validate player count
    if not (2 <= NUM_PLAYERS <= len(PLAYER_TOKENS)):
        print(f"NUM_PLAYERS must be between 2 and {len(PLAYER_TOKENS)}")
        sys.exit(1)

    # Active players and their tokens
    players = PLAYER_TOKENS[:NUM_PLAYERS]

    # Create board
    board = make_board()

    # Pick random starting player index
    current = random.randrange(NUM_PLAYERS)

    # Main loop
    winner: Optional[str] = None
    while True:
        clear_screen()
        print("Connect 4 - 6x7")
        print(f"Players: {' '.join(players)}  |  Turn: {players[current]}")
        print_board(board)

        # Prompt input
        print("Enter a column letter (A-G) to drop a piece, or Q to quit.")
        raw = input(f"Player {players[current]}, choose column: ").strip()

        # Quit option
        if raw.lower() == 'q':
            print("Game aborted. Goodbye!")
            return

        # Validate column
        col = parse_column_input(raw)
        if col is None:
            print("Invalid input. Please enter a single letter A-G.")
            input("Press Enter to continue...")
            continue

        # Find open row in this column
        row = next_open_row(board, col)
        if row is None:
            print(f"Column {COLUMN_LABELS[col]} is full. Choose another column.")
            input("Press Enter to continue...")
            continue

        # Drop the piece
        token = players[current]
        drop_piece(board, row, col, token)

        # Check for win
        if check_win(board, token):
            clear_screen()
            print_board(board)
            print(f"Player {token} wins! Congratulations!")
            winner = token
            break

        # Check for draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw! No more moves possible.")
            break

        # Next player's turn (cycle through players)
        current = (current + 1) % NUM_PLAYERS

    # Game over; optional prompt to play again
    print()
    _ = input("Press Enter to exit...")


# -------------------- Entry Point --------------------
if __name__ == "__main__":
    play_game()
