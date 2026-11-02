#!/usr/bin/env python3
"""
Connect 4 (6x7) for 2–5 players.
- Columns labeled A–G
- Player symbols: X, O, V, H, M (use a prefix of these via NUM_PLAYERS)
- Random first player each game
- Validates input, detects wins and draws
- Clears screen with os.system('clear') (or 'cls' on Windows)
"""

import os
import random
import sys
from typing import List, Optional, Tuple

# ----------------------------
# Configuration (you can edit)
# ----------------------------
ROWS = 6
COLS = 7

# Player symbols in the order they will play. Use a prefix of these by NUM_PLAYERS.
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# How many players are in this match (2 to 5).
NUM_PLAYERS = 2  # change to 3, 4, or 5 if you want more players

# ----------------------------
# Helpers
# ----------------------------

COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]
EMPTY = " "

def clear_screen() -> None:
    """Clear the terminal screen."""
    # Use 'cls' on Windows, 'clear' elsewhere
    os.system('cls' if os.name == 'nt' else 'clear')

def make_board(rows: int, cols: int) -> List[List[str]]:
    """Create an empty board."""
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]

def print_board(board: List[List[str]]) -> None:
    """Pretty-print the board with column labels."""
    print("  " + "   ".join(COLUMN_LABELS))
    print(" +" + "---+" * COLS)
    for r in range(ROWS):
        row_cells = [board[r][c] if board[r][c] != EMPTY else " " for c in range(COLS)]
        print(" | " + " | ".join(row_cells) + " |")
        print(" +" + "---+" * COLS)

def get_active_players() -> List[str]:
    """Return the list of active player symbols based on NUM_PLAYERS."""
    if not (2 <= NUM_PLAYERS <= min(5, len(PLAYER_SYMBOLS))):
        raise ValueError("NUM_PLAYERS must be between 2 and 5 and <= len(PLAYER_SYMBOLS).")
    return PLAYER_SYMBOLS[:NUM_PLAYERS]

def drop_piece(board: List[List[str]], col: int, symbol: str) -> Optional[Tuple[int, int]]:
    """
    Drop a piece into a column.
    Returns (row, col) where the piece landed, or None if the column is full.
    """
    for r in reversed(range(ROWS)):
        if board[r][col] == EMPTY:
            board[r][col] = symbol
            return (r, col)
    return None

def in_bounds(r: int, c: int) -> bool:
    return 0 <= r < ROWS and 0 <= c < COLS

def count_direction(board: List[List[str]], start: Tuple[int, int], dr: int, dc: int, symbol: str) -> int:
    """
    Count consecutive pieces of 'symbol' from start (exclusive) in direction (dr, dc).
    """
    r, c = start
    count = 0
    while True:
        r += dr
        c += dc
        if not in_bounds(r, c) or board[r][c] != symbol:
            break
        count += 1
    return count

def is_winning_move(board: List[List[str]], last_move: Tuple[int, int], symbol: str) -> bool:
    """
    Check if the last move by 'symbol' at (row, col) created a connect-4.
    """
    r, c = last_move
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        # Count both directions from the last piece (excluding the last piece itself)
        total = 1
        total += count_direction(board, (r, c), dr, dc, symbol)
        total += count_direction(board, (r, c), -dr, -dc, symbol)
        if total >= 4:
            return True
    return False

def is_draw(board: List[List[str]]) -> bool:
    """The game is a draw if the top row has no empty spaces (board full)."""
    return all(board[0][c] != EMPTY for c in range(COLS))

def get_valid_columns(board: List[List[str]]) -> List[int]:
    """Return a list of column indices that are not full."""
    return [c for c in range(COLS) if board[0][c] == EMPTY]

def prompt_for_column(current_symbol: str, valid_cols: List[int]) -> Optional[int]:
    """
    Prompt the user to enter a column label (A-G) or Q to quit.
    Validate the input and return the chosen column index, or None if quitting.
    """
    valid_labels = {COLUMN_LABELS[c]: c for c in valid_cols}
    while True:
        choice = input(f"Player {current_symbol}, choose a column ({'/'.join(COLUMN_LABELS)}), or Q to quit: ").strip().upper()
        if choice == "Q":
            return None
        if len(choice) == 1 and choice in valid_labels:
            return valid_labels[choice]
        elif len(choice) == 1 and choice in COLUMN_LABELS:
            print(f"Column {choice} is full. Choose another.")
        else:
            print("Invalid input. Please enter a valid column letter (A-G) or Q to quit.")

def game_loop() -> None:
    active_players = get_active_players()
    board = make_board(ROWS, COLS)

    # Randomize starting player
    current_index = random.randrange(len(active_players))

    while True:
        clear_screen()
        print_board(board)
        valid_cols = get_valid_columns(board)

        if not valid_cols:
            print("It's a draw! The board is full.")
            break

        current_symbol = active_players[current_index]
        col = prompt_for_column(current_symbol, valid_cols)
        if col is None:
            print("Game ended by user.")
            break

        move = drop_piece(board, col, current_symbol)
        if move is None:
            # Shouldn't happen due to validation, but keep as a guard.
            print("That column is full. Try again.")
            input("Press Enter to continue...")
            continue

        if is_winning_move(board, move, current_symbol):
            clear_screen()
            print_board(board)
            print(f"Player {current_symbol} wins!")
            break

        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! The board is full.")
            break

        # Next player's turn
        current_index = (current_index + 1) % len(active_players)

def main() -> None:
    try:
        game_loop()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()
