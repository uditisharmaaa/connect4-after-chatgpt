import os
import random
import string
from typing import List, Optional, Tuple

# ------------------------- Configuration -------------------------

# Board dimensions (ROWS x COLS). Submission requires 6 rows x 7 cols.
ROWS = 6
COLS = 7  # Max 26 (A-Z)

# Number of players (2 to 5). Submission requires 2 players.
NUM_PLAYERS = 2

# Symbols in order for players 1..5
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Number of checkers in a row needed to win
WIN_LENGTH = 4

# ----------------------- Utility / Validation --------------------

def validate_configuration(rows: int, cols: int, num_players: int) -> None:
    if not (2 <= num_players <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    if not (1 <= rows):
        raise ValueError("ROWS must be >= 1.")
    if not (1 <= cols <= 26):
        raise ValueError("COLS must be between 1 and 26.")
    if num_players > len(PLAYER_CHECKERS):
        raise ValueError("Not enough player checkers defined.")

# ----------------------------- Board -----------------------------

def create_board(rows: int, cols: int) -> List[List[str]]:
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def clear_screen() -> None:
    # Clear screen on Unix/Linux terminals as required
    os.system('clear')

def column_headers(cols: int) -> str:
    letters = string.ascii_uppercase[:cols]
    # Format like: "  A   B   C ..."
    return "  " + "   ".join(letters)

def horizontal_rule(cols: int) -> str:
    # Format: +---+---+...+ (cols times)
    return "+" + ("---+" * cols)

def print_board(board: List[List[str]]) -> None:
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    print(column_headers(cols))
    hr = horizontal_rule(cols)
    for r in range(rows):
        print(hr)
        # Each cell: | {cell} |
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print(hr)

# ------------------------ Game Mechanics -------------------------

def first_empty_row(board: List[List[str]], col: int) -> Optional[int]:
    # Returns the row index where a checker would land in given column, or None if full
    for r in range(len(board) - 1, -1, -1):  # bottom up
        if board[r][col] == ' ':
            return r
    return None

def drop_checker(board: List[List[str]], col: int, checker: str) -> Optional[int]:
    r = first_empty_row(board, col)
    if r is None:
        return None
    board[r][col] = checker
    return r

def in_bounds(rows: int, cols: int, r: int, c: int) -> bool:
    return 0 <= r < rows and 0 <= c < cols

def count_in_direction(board: List[List[str]], start: Tuple[int, int], delta: Tuple[int, int], checker: str) -> int:
    rows, cols = len(board), len(board[0])
    r, c = start
    dr, dc = delta
    count = 0
    while in_bounds(rows, cols, r, c) and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count

def is_winning_move(board: List[List[str]], row: int, col: int, checker: str) -> bool:
    # Check 4 directions: horizontal, vertical, diag1 (/), diag2 (\)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        # Count including both sides from the placed checker
        forward = count_in_direction(board, (row, col), (dr, dc), checker)
        backward = count_in_direction(board, (row, col), (-dr, -dc), checker)
        if forward + backward - 1 >= WIN_LENGTH:
            return True
    return False

def is_board_full(board: List[List[str]]) -> bool:
    return all(cell != ' ' for row in board for cell in row)

def letter_to_col(letter: str, cols: int) -> Optional[int]:
    letter = letter.strip().upper()
    if len(letter) != 1 or letter < 'A' or letter > chr(ord('A') + cols - 1):
        return None
    return ord(letter) - ord('A')

# ---------------------------- I/O Loop ---------------------------

def prompt_for_column(current_checker: str, total_cols: int) -> int:
    while True:
        user_input = input(f"Player {current_checker}, please enter a column: ").strip()
        col = letter_to_col(user_input, total_cols)
        if col is None:
            print("Invalid input. Please enter a single uppercase letter of a valid column (e.g., A, B, C).")
            continue
        return col

# ----------------------------- Game -----------------------------

def main() -> None:
    validate_configuration(ROWS, COLS, NUM_PLAYERS)

    # Setup
    board = create_board(ROWS, COLS)
    player_symbols = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial board display
    print_board(board)

    # Game loop
    while True:
        current_checker = player_symbols[current_player_idx]

        # Prompt for a valid column letter (retry on invalid input)
        col = prompt_for_column(current_checker, COLS)

        # Try to drop checker (if column is full, turn is lost)
        row_placed = drop_checker(board, col, current_checker)
        print_board(board)  # Update board display after the attempt

        if row_placed is None:
            # Column full: turn lost
            col_letter = chr(ord('A') + col)
            print(f"Column {col_letter} is full. Player {current_checker} loses the turn.")
            # Next player's turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Check for a win
        if is_winning_move(board, row_placed, col, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for a draw
        if is_board_full(board):
            print("Game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
