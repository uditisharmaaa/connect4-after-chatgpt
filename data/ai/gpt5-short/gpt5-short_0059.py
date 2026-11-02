#!/usr/bin/env python3
import os
import random
import string
from typing import List, Optional, Tuple

# -------------------------------
# Configuration constants
# -------------------------------
ROWS = 6
COLS = 7
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]  # ['A', 'B', ..., 'G']

# Symbols available for up to 5 players (edit NUM_PLAYERS to choose how many actually play)
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # set to 2..5

EMPTY = '.'  # visual for an empty cell

# -------------------------------
# Board helpers
# -------------------------------
def make_board(rows: int, cols: int) -> List[List[str]]:
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]

def clear_screen() -> None:
    # As requested, use 'clear' (works on most Unix-like systems)
    os.system('clear')

def print_board(board: List[List[str]]) -> None:
    # Header
    print('  ' + ' '.join(COLUMN_LABELS))
    # Rows (top to bottom)
    for r in range(ROWS):
        print(f"{ROWS - r} " + ' '.join(board[r]))
    print()  # blank line

def is_column_full(board: List[List[str]], col: int) -> bool:
    return board[0][col] != EMPTY

def drop_piece(board: List[List[str]], col: int, symbol: str) -> Optional[Tuple[int, int]]:
    """
    Drop symbol into the chosen column. Returns (row, col) where piece lands, or None if column is full.
    """
    if is_column_full(board, col):
        return None
    # Start from bottom, place in first empty spot
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            board[r][col] = symbol
            return (r, col)
    return None  # should not reach here if not full

# -------------------------------
# Win / draw detection
# -------------------------------
def in_bounds(r: int, c: int) -> bool:
    return 0 <= r < ROWS and 0 <= c < COLS

def count_in_direction(board: List[List[str]], r: int, c: int, dr: int, dc: int, symbol: str) -> int:
    """
    Count consecutive pieces matching symbol starting at (r, c), moving by (dr, dc), not including (r, c) itself.
    """
    count = 0
    nr, nc = r + dr, c + dc
    while in_bounds(nr, nc) and board[nr][nc] == symbol:
        count += 1
        nr += dr
        nc += dc
    return count

def is_winning_move(board: List[List[str]], r: int, c: int, symbol: str) -> bool:
    """
    Check all directions from last move (r, c) for 4 in a row.
    Directions: horizontal, vertical, two diagonals.
    """
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        total = 1  # include the current piece
        total += count_in_direction(board, r, c, dr, dc, symbol)
        total += count_in_direction(board, r, c, -dr, -dc, symbol)
        if total >= 4:
            return True
    return False

def is_draw(board: List[List[str]]) -> bool:
    # Draw if no empty cells in the top row
    return all(board[0][c] != EMPTY for c in range(COLS))

# -------------------------------
# Input handling
# -------------------------------
def parse_column_input(user_input: str) -> Optional[int]:
    """
    Convert user input like 'A'..'G' to a zero-based column index. Returns None if invalid.
    """
    s = user_input.strip().upper()
    if len(s) != 1:
        return None
    if s not in COLUMN_LABELS:
        return None
    return ord(s) - ord('A')

def prompt_for_move(board: List[List[str]], player_symbol: str) -> int:
    """
    Prompt the current player for a valid column. Re-prompts until a valid, non-full column is chosen.
    """
    while True:
        raw = input(f"Player {player_symbol}, choose a column ({COLUMN_LABELS[0]}-{COLUMN_LABELS[-1]}): ")
        col = parse_column_input(raw)
        if col is None:
            print(f"Invalid input. Please enter a single letter between {COLUMN_LABELS[0]} and {COLUMN_LABELS[-1]}.")
            continue
        if is_column_full(board, col):
            print(f"Column {COLUMN_LABELS[col]} is full. Choose another.")
            continue
        return col

# -------------------------------
# Game loop
# -------------------------------
def play_game() -> None:
    # Validate number of players
    n = max(2, min(NUM_PLAYERS, len(PLAYER_SYMBOLS)))
    participants = PLAYER_SYMBOLS[:n]

    board = make_board(ROWS, COLS)

    # Randomly choose a starting player index
    current_idx = random.randrange(n)

    # Main loop
    while True:
        clear_screen()
        print("Connect 4")
        print(f"Players: {', '.join(participants)}")
        print_board(board)

        current_symbol = participants[current_idx]

        # Get a valid move
        col = prompt_for_move(board, current_symbol)
        result = drop_piece(board, col, current_symbol)
        assert result is not None  # ensured by prompt_for_move
        r, c = result

        # Check for win or draw
        if is_winning_move(board, r, c, current_symbol):
            clear_screen()
            print("Connect 4")
            print(f"Players: {', '.join(participants)}")
            print_board(board)
            print(f"Player {current_symbol} wins!")
            break

        if is_draw(board):
            clear_screen()
            print("Connect 4")
            print(f"Players: {', '.join(participants)}")
            print_board(board)
            print("It's a draw!")
            break

        # Advance to next player
        current_idx = (current_idx + 1) % n

def main() -> None:
    try:
        play_game()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")

if __name__ == "__main__":
    main()
