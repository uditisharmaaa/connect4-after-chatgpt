#!/usr/bin/env python3
"""
Connect 4 (Generalized for 2–5 players)

Features:
- 6 rows x 7 columns board
- Columns labeled A–G for input
- 2 to 5 players supported with tokens: X, O, V, H, M (subset chosen by NUM_PLAYERS)
- Randomly selected starting player
- Robust input validation (valid column, not full)
- Win detection (horizontal, vertical, both diagonals)
- Draw detection
- Screen cleared each turn using os.system('clear') with a Windows fallback

Designed for readability and clarity for an intro CS class.
"""

import os
import random
import sys
from typing import List, Optional, Tuple

# -----------------------
# Configuration constants
# -----------------------

ROWS = 6
COLS = 7
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]  # ['A','B','C','D','E','F','G']

# Allowed player tokens in order; NUM_PLAYERS picks the first N of these
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']

# Set number of players (2–5). Change this constant to choose how many will play.
NUM_PLAYERS = 2  # e.g., 2 for classic Connect 4; up to 5 allowed here.

# Optional: Allow quitting by entering 'Q'
ALLOW_QUIT = True

# -----------------------
# Utility and game logic
# -----------------------

def clear_screen() -> None:
    """
    Clear the terminal screen. Uses 'clear' (POSIX) and falls back to 'cls' (Windows).
    """
    # The spec requires os.system('clear'), but we add a safe fallback for Windows.
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def create_board(rows: int, cols: int) -> List[List[str]]:
    """
    Create an empty board represented by a list of lists filled with '.'.
    """
    return [['.' for _ in range(cols)] for _ in range(rows)]


def render_board(board: List[List[str]]) -> None:
    """
    Print the current board and column labels.
    Top row of the list is printed first (visual top).
    """
    print("   " + " ".join(COLUMN_LABELS))
    for r in range(len(board)):
        row_str = " | " + " ".join(board[r])
        print(f"{r+1:2d}{row_str}")
    print()


def column_from_input(user_input: str) -> Optional[int]:
    """
    Convert user input like 'A' or 'g' to a column index [0..COLS-1].
    Returns None if invalid.
    """
    if not user_input:
        return None
    c = user_input.strip().upper()
    if c in COLUMN_LABELS:
        return COLUMN_LABELS.index(c)
    return None


def next_open_row(board: List[List[str]], col: int) -> Optional[int]:
    """
    Return the lowest available row index in the given column, or None if the column is full.
    Rows increase from top (0) to bottom (ROWS-1), but tokens drop to the bottommost '.'.
    """
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == '.':
            return r
    return None


def place_token(board: List[List[str]], col: int, token: str) -> Optional[Tuple[int, int]]:
    """
    Attempt to place a token in the given column. Returns (row, col) where placed, or None if column is full.
    """
    row = next_open_row(board, col)
    if row is None:
        return None
    board[row][col] = token
    return (row, col)


def count_in_direction(board: List[List[str]], start_r: int, start_c: int, dr: int, dc: int, token: str) -> int:
    """
    Count consecutive tokens matching 'token' starting from (start_r, start_c) moving in direction (dr, dc).
    Does not include the starting cell itself.
    """
    r, c = start_r + dr, start_c + dc
    count = 0
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == token:
        count += 1
        r += dr
        c += dc
    return count


def is_winning_move(board: List[List[str]], last_r: int, last_c: int, token: str) -> bool:
    """
    Check if placing 'token' at (last_r, last_c) causes a win.
    Looks in 4 directions (pairs): horizontal, vertical, diag1 (/), diag2 (\).
    A win is 4 in a row (including the last placed token).
    """
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        # Count both directions from the last move
        total = 1  # include the last placed token
        total += count_in_direction(board, last_r, last_c, dr, dc, token)
        total += count_in_direction(board, last_r, last_c, -dr, -dc, token)
        if total >= 4:
            return True
    return False


def is_board_full(board: List[List[str]]) -> bool:
    """
    Determine if the board has no more available moves.
    """
    for c in range(COLS):
        if board[0][c] == '.':
            return False
    return True


def choose_starting_player(num_players: int) -> int:
    """
    Randomly select an index [0..num_players-1] to start.
    """
    return random.randrange(num_players)


def get_active_tokens(num_players: int) -> List[str]:
    """
    Return the first num_players tokens from PLAYER_TOKENS.
    """
    assert 2 <= num_players <= 5, "NUM_PLAYERS must be between 2 and 5."
    return PLAYER_TOKENS[:num_players]


def prompt_for_move(current_token: str) -> Optional[int]:
    """
    Prompt the user for a column letter and validate it.
    Returns column index or None if the user chooses to quit and ALLOW_QUIT is True.
    """
    while True:
        raw = input(f"Player {current_token}, choose a column (A-{COLUMN_LABELS[-1]})"
                    f"{' or Q to quit' if ALLOW_QUIT else ''}: ").strip()
        if ALLOW_QUIT and raw.upper() == 'Q':
            return None
        col = column_from_input(raw)
        if col is None:
            print("Invalid input. Please enter a letter A to G.")
            continue
        return col


def game_loop() -> None:
    """
    Main game loop for Connect 4 supporting 2–5 players.
    """
    tokens = get_active_tokens(NUM_PLAYERS)
    board = create_board(ROWS, COLS)

    current_index = choose_starting_player(len(tokens))

    while True:
        clear_screen()
        print("Connect 4")
        print(f"Players: {' '.join(tokens)}   (Starting: {tokens[current_index]})")
        render_board(board)

        current_token = tokens[current_index]

        col = prompt_for_move(current_token)
        if col is None:
            print("Game ended by user.")
            return

        spot = place_token(board, col, current_token)
        if spot is None:
            print("That column is full. Press Enter to choose again.")
            input()
            continue

        r, c = spot
        if is_winning_move(board, r, c, current_token):
            clear_screen()
            print("Connect 4")
            print(f"Players: {' '.join(tokens)}   (Starting: {tokens[(current_index) % len(tokens)]})")
            render_board(board)
            print(f"Player {current_token} wins! Congratulations!")
            return

        if is_board_full(board):
            clear_screen()
            print("Connect 4")
            render_board(board)
            print("It's a draw! No more moves possible.")
            return

        # Next player's turn
        current_index = (current_index + 1) % len(tokens)


def main():
    # Basic validation for configuration
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)

    # Seed randomness for fairness (optional: can seed with time by default)
    random.seed()

    # Start the game
    game_loop()


if __name__ == "__main__":
    main()
