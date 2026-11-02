import os
import random
import string
from typing import List, Optional, Tuple

# -----------------------------
# Configuration (changeable)
# -----------------------------
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]

# -----------------------------
# Validations for configuration
# -----------------------------
if not (2 <= NUM_PLAYERS <= 5):
    raise ValueError("NUM_PLAYERS must be between 2 and 5.")
if not (1 <= COLS <= 26):
    raise ValueError("COLS must be between 1 and 26.")
if ROWS < 1:
    raise ValueError("ROWS must be at least 1.")

PLAYER_SYMBOLS = CHECKERS[:NUM_PLAYERS]


# -----------------------------
# Board Utilities
# -----------------------------
def create_board(rows: int, cols: int) -> List[List[str]]:
    return [[" " for _ in range(cols)] for _ in range(rows)]


def clear_screen() -> None:
    # As per assignment, we target Linux/Unix
    os.system('clear')


def print_board(board: List[List[str]]) -> None:
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header with column letters
    letters = string.ascii_uppercase[:cols]
    print("  " + "   ".join(letters))
    # Top border
    print("+" + "+".join(["---"] * cols) + "+")

    # Rows
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + "+".join(["---"] * cols) + "+")


def is_column_full(board: List[List[str]], col: int) -> bool:
    return board[0][col] != " "


def first_empty_row(board: List[List[str]], col: int) -> Optional[int]:
    # Returns the row index where a checker will land (from bottom up)
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def place_checker(board: List[List[str]], col: int, checker: str) -> Optional[Tuple[int, int]]:
    """
    Attempts to place a checker in the given column.
    Returns (row, col) if successful, otherwise None if column is full.
    """
    if is_column_full(board, col):
        return None
    r = first_empty_row(board, col)
    if r is None:
        return None
    board[r][col] = checker
    return (r, col)


def board_full(board: List[List[str]]) -> bool:
    return all(cell != " " for row in board for cell in row)


# -----------------------------
# Win / Draw Checking
# -----------------------------
def check_win(board: List[List[str]], checker: str) -> bool:
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    target = checker

    # Horizontal check
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == target:
                count += 1
                if count >= 4:
                    return True
            else:
                count = 0

    # Vertical check
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == target:
                count += 1
                if count >= 4:
                    return True
            else:
                count = 0

    # Diagonal down-right (\)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if (board[r][c] == target and
                board[r + 1][c + 1] == target and
                board[r + 2][c + 2] == target and
                board[r + 3][c + 3] == target):
                return True

    # Diagonal up-right (/)
    for r in range(3, rows):
        for c in range(cols - 3):
            if (board[r][c] == target and
                board[r - 1][c + 1] == target and
                board[r - 2][c + 2] == target and
                board[r - 3][c + 3] == target):
                return True

    return False


# -----------------------------
# Input Handling
# -----------------------------
def prompt_for_column(cols: int, current_checker: str) -> str:
    # Returns raw input string (upper-cased, stripped)
    while True:
        user_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
        if len(user_input) != 1:
            print("Invalid input. Enter a single letter corresponding to a column.")
            continue
        ch = user_input[0]
        if ch < 'A' or ch >= chr(ord('A') + cols):
            print("Invalid column. Please choose a letter within the board's columns.")
            continue
        return ch


def column_index_from_letter(letter: str) -> int:
    return ord(letter) - ord('A')


# -----------------------------
# Game Loop
# -----------------------------
def main() -> None:
    board = create_board(ROWS, COLS)
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial board display
    print_board(board)

    while True:
        checker = PLAYER_SYMBOLS[current_player_idx]
        # Before prompting, show current board and whose turn it is
        # As per example, the prompt follows immediately after the board
        # We already print the board at top of loop
        # But we need to reprint because other player's previous action may have changed it
        # So print now:
        print_board(board)

        # Input loop for validation; invalid inputs are retried; full column loses turn
        col_letter = prompt_for_column(COLS, checker)
        col_idx = column_index_from_letter(col_letter)

        placed_pos = place_checker(board, col_idx, checker)
        if placed_pos is None:
            # Column full: turn is invalid and player loses the turn
            print_board(board)
            print(f"Column {col_letter} is full. Player {checker} loses the turn.")
            # Check draw (board could be full)
            if board_full(board):
                print("It's a draw!")
                return
            # Next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # After a successful placement, print updated board
        print_board(board)

        # Check for win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            return

        # Check for draw
        if board_full(board):
            print("It's a draw!")
            return

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
