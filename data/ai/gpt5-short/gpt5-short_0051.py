#!/usr/bin/env python3
"""
Connect 4 (6x7) for 2–5 players.
- Columns labeled A–G
- Player tokens (in order): X, O, V, H, M
- Random first player each game
- Validates input and handles wins/draws
- Clears screen each turn with os.system('clear')  (works on macOS/Linux)

Change NUM_PLAYERS (2–5) below to choose how many players are in the game.
"""

import os
import random
from typing import List, Optional, Tuple

# ---------------- Configuration ----------------
ROWS = 6
COLS = 7
WIN_LENGTH = 4

PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']  # up to 5
NUM_PLAYERS = 2  # set between 2 and 5
EMPTY = '.'
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]
# ------------------------------------------------


def clear_screen() -> None:
    os.system('clear')  # On Windows, you could use 'cls' instead.


def make_board(rows: int, cols: int) -> List[List[str]]:
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]


def print_board(board: List[List[str]]) -> None:
    # Column header
    print("  " + " ".join(COLUMN_LABELS))
    # Rows
    for r in range(len(board)):
        print(f"{ROWS - r} " + " ".join(board[r]))
    # Footer line for spacing
    print()


def col_from_label(label: str) -> Optional[int]:
    label = label.strip().upper()
    if len(label) != 1:
        return None
    if label in COLUMN_LABELS:
        return COLUMN_LABELS.index(label)
    return None


def drop_piece(board: List[List[str]], col: int, token: str) -> Optional[Tuple[int, int]]:
    """
    Drops a piece into the given column.
    Returns the (row, col) where the piece lands, or None if the column is full.
    """
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            board[r][col] = token
            return r, col
    return None


def in_bounds(r: int, c: int) -> bool:
    return 0 <= r < ROWS and 0 <= c < COLS


def count_in_direction(board: List[List[str]], r: int, c: int, dr: int, dc: int, token: str) -> int:
    """
    Counts the number of consecutive tokens (including the starting cell)
    in the given direction (dr, dc) and its opposite.
    """
    total = 1  # start with the placed piece
    # forward direction
    rr, cc = r + dr, c + dc
    while in_bounds(rr, cc) and board[rr][cc] == token:
        total += 1
        rr += dr
        cc += dc
    # backward direction
    rr, cc = r - dr, c - dc
    while in_bounds(rr, cc) and board[rr][cc] == token:
        total += 1
        rr -= dr
        cc -= dc
    return total


def is_winning_move(board: List[List[str]], r: int, c: int, token: str) -> bool:
    # Check all 4 directions: horizontal, vertical, and two diagonals
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        if count_in_direction(board, r, c, dr, dc, token) >= WIN_LENGTH:
            return True
    return False


def is_draw(board: List[List[str]]) -> bool:
    # Draw if no EMPTY cell in the top row (or anywhere)
    return all(cell != EMPTY for cell in board[0])


def next_player_index(curr: int, total: int) -> int:
    return (curr + 1) % total


def get_valid_move(board: List[List[str]], current_token: str) -> int:
    """
    Prompt the user until a valid column is entered (A–G) and not full.
    Returns the column index.
    """
    while True:
        choice = input(f"Player {current_token}, choose a column (A–G): ").strip()
        col = col_from_label(choice)
        if col is None:
            print("Invalid input. Enter a single letter A–G.")
            continue
        if board[0][col] != EMPTY:
            print(f"Column {COLUMN_LABELS[col]} is full. Choose another.")
            continue
        return col


def validate_settings() -> None:
    if not (2 <= NUM_PLAYERS <= len(PLAYER_TOKENS)):
        raise ValueError(f"NUM_PLAYERS must be between 2 and {len(PLAYER_TOKENS)}")
    if COLS != 7 or ROWS != 6:
        # Not strictly necessary, but this enforces standard size per the assignment
        raise ValueError("This game is configured for 6 rows and 7 columns.")
    if WIN_LENGTH != 4:
        raise ValueError("WIN_LENGTH must be 4 for standard Connect 4.")


def main() -> None:
    validate_settings()

    tokens = PLAYER_TOKENS[:NUM_PLAYERS]
    board = make_board(ROWS, COLS)

    # Randomize first player
    start_index = random.randrange(NUM_PLAYERS)
    current_index = start_index

    while True:
        clear_screen()
        print_board(board)

        current_token = tokens[current_index]
        try:
            col = get_valid_move(board, current_token)
        except (EOFError, KeyboardInterrupt):
            print("\nGame aborted.")
            return

        drop_result = drop_piece(board, col, current_token)
        if drop_result is None:
            # Shouldn't happen due to validation, but safe-guard anyway
            print(f"Column {COLUMN_LABELS[col]} is full. Try again.")
            input("Press Enter to continue...")
            continue

        r, c = drop_result

        # Check for win or draw
        if is_winning_move(board, r, c, current_token):
            clear_screen()
            print_board(board)
            print(f"Player {current_token} wins!")
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_index = next_player_index(current_index, NUM_PLAYERS)


if __name__ == "__main__":
    main()
