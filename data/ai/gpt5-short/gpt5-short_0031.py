# Connect 4 (6x7) with 2–5 players for Intro CS
# - Columns labeled A–G
# - Players use symbols from PLAYER_SYMBOLS (X, O, V, H, M)
# - Number of active players set by ACTIVE_PLAYERS (2–5)
# - Random first player
# - Validates input
# - Checks wins and draws
# - Uses os.system('clear') to refresh display
#
# Run this file directly to play.

import os
import random
import sys
from typing import List, Optional, Tuple

# -----------------------------
# Configuration constants
# -----------------------------
NUM_ROWS = 6
NUM_COLS = 7
COLUMN_LABELS = tuple("ABCDEFG")

# Available player symbols in turn order. The first ACTIVE_PLAYERS of these will be used.
PLAYER_SYMBOLS = ("X", "O", "V", "H", "M")

# Set how many players are active (must be 2–5).
ACTIVE_PLAYERS = 2  # Change to 3, 4, or 5 if desired


# -----------------------------
# Utility and game logic
# -----------------------------
def clear_screen() -> None:
    """
    Clear the console screen. Uses 'clear' by requirement, and falls back to 'cls' on Windows.
    """
    # Primary as requested
    ret = os.system("clear")
    # Fallback for Windows if 'clear' fails
    if ret != 0:
        os.system("cls")


def create_board(rows: int = NUM_ROWS, cols: int = NUM_COLS) -> List[List[str]]:
    """
    Create an empty Connect 4 board filled with spaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board: List[List[str]]) -> None:
    """
    Print the board to the console with column labels.
    """
    # Column labels
    print("  " + "   ".join(COLUMN_LABELS))
    print("+" + "---+" * NUM_COLS)
    # Rows
    for r in range(NUM_ROWS):
        row_cells = []
        for c in range(NUM_COLS):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + "---+" * NUM_COLS)


def column_from_input(user_input: str) -> Optional[int]:
    """
    Convert user input (A-G) to a zero-based column index.
    Returns None if invalid.
    """
    if len(user_input) != 1:
        return None
    ch = user_input.upper()
    if ch in COLUMN_LABELS:
        return COLUMN_LABELS.index(ch)
    return None


def first_empty_row(board: List[List[str]], col: int) -> Optional[int]:
    """
    Return the index of the lowest empty row in a given column, or None if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def drop_piece(board: List[List[str]], col: int, symbol: str) -> Optional[Tuple[int, int]]:
    """
    Place the player's symbol into the chosen column if possible.
    Returns (row, col) where the piece landed, or None if the column is full.
    """
    r = first_empty_row(board, col)
    if r is None:
        return None
    board[r][col] = symbol
    return (r, col)


def in_bounds(r: int, c: int) -> bool:
    return 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS


def check_winner(board: List[List[str]], last_row: int, last_col: int, symbol: str) -> bool:
    """
    Check if placing 'symbol' at (last_row, last_col) creates a 4-in-a-row.
    We scan in four directions: horizontal, vertical, diagonal down-right, diagonal up-right.
    """
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (-1, 1),  # diagonal up-right
    ]

    for dr, dc in directions:
        count = 1  # includes the last placed piece
        # forward
        r, c = last_row + dr, last_col + dc
        while in_bounds(r, c) and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        # backward
        r, c = last_row - dr, last_col - dc
        while in_bounds(r, c) and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True

    return False


def check_draw(board: List[List[str]]) -> bool:
    """
    A draw occurs when there are no empty spaces left on the board.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False
    return True


def get_validated_move(board: List[List[str]], symbol: str) -> Optional[int]:
    """
    Prompt the user for a column (A-G) or Q to quit, validating:
    - Correct label
    - Column not full
    Returns the zero-based column index, or None if player quits.
    """
    while True:
        raw = input(f"Player {symbol}, choose a column (A-G) or Q to quit: ").strip()
        if raw.lower() == "q":
            return None

        col = column_from_input(raw)
        if col is None:
            print("Invalid input. Please enter a single letter A-G.")
            continue

        if first_empty_row(board, col) is None:
            print(f"Column {COLUMN_LABELS[col]} is full. Choose another column.")
            continue

        return col


def validate_settings() -> List[str]:
    """
    Validate configuration constants and return the active player list.
    Raises SystemExit on invalid settings to help students catch mistakes early.
    """
    if NUM_ROWS != 6 or NUM_COLS != 7:
        print("Error: Board must be 6 rows by 7 columns.")
        sys.exit(1)
    if len(COLUMN_LABELS) != NUM_COLS:
        print("Error: COLUMN_LABELS must match NUM_COLS.")
        sys.exit(1)
    if not (2 <= ACTIVE_PLAYERS <= 5):
        print("Error: ACTIVE_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if ACTIVE_PLAYERS > len(PLAYER_SYMBOLS):
        print("Error: Not enough PLAYER_SYMBOLS for the requested number of players.")
        sys.exit(1)

    active = list(PLAYER_SYMBOLS[:ACTIVE_PLAYERS])

    # Ensure symbols are single visible characters and unique
    if any((not isinstance(s, str) or len(s) != 1 or s.isspace()) for s in active):
        print("Error: Each player symbol must be a single, non-space character.")
        sys.exit(1)
    if len(set(active)) != len(active):
        print("Error: Player symbols must be unique.")
        sys.exit(1)

    return active


def play_game() -> None:
    """
    Main game loop for multi-player Connect 4.
    """
    players = validate_settings()
    # Randomize turn order and pick a random first player
    random.shuffle(players)

    board = create_board()
    turn_index = 0

    while True:
        clear_screen()
        print_board(board)

        current_symbol = players[turn_index]
        move = get_validated_move(board, current_symbol)
        if move is None:
            print(f"Player {current_symbol} quit. Game over.")
            break

        placed = drop_piece(board, move, current_symbol)
        if placed is None:
            # This should not happen due to validation, but included for safety.
            print("Unexpected error: could not place piece. Try again.")
            input("Press Enter to continue...")
            continue

        r, c = placed

        # Check for win or draw
        if check_winner(board, r, c, current_symbol):
            clear_screen()
            print_board(board)
            print(f"Player {current_symbol} wins! Congratulations!")
            break

        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! No more moves available.")
            break

        # Next player's turn
        turn_index = (turn_index + 1) % len(players)


if __name__ == "__main__":
    play_game()
