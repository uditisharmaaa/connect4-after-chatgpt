import os
import random
import string
import sys
from typing import List, Optional, Tuple

# ----- Configuration constants -----
ROWS = 6            # Number of rows (default 6)
COLS = 7            # Number of columns (default 7, max 26)
NUM_PLAYERS = 2     # Players from 2 to 5
TOKENS = ["X", "O", "V", "H", "M"]  # In order as specified
WIN_LENGTH = 4      # Always 4 to win as per assignment

# ----- Validations for configuration -----
if not (2 <= NUM_PLAYERS <= 5):
    raise ValueError("NUM_PLAYERS must be between 2 and 5.")

if COLS > 26 or COLS < 1:
    raise ValueError("COLS must be between 1 and 26.")

if ROWS < 1:
    raise ValueError("ROWS must be at least 1.")

PLAYER_TOKENS = TOKENS[:NUM_PLAYERS]
COL_LABELS = list(string.ascii_uppercase[:COLS])


def clear_screen():
    # Try to clear the terminal screen on Unix and Windows
    # Assignment requests: os.system('clear')
    # Also attempt 'cls' for Windows environments
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def create_board(rows: int, cols: int) -> List[List[str]]:
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board: List[List[str]]):
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header (column labels)
    header = "  " + "   ".join(COL_LABELS[:cols])
    print(header)

    # Horizontal separator
    sep = "+" + "+".join(["---"] * cols) + "+"

    # Rows
    for r in range(rows):
        print(sep)
        row_cells = "|".join([f" {board[r][c]} " for c in range(cols)])
        print(f"|{row_cells}|")
    print(sep)


def get_column_from_input(prompt: str) -> Optional[int]:
    """
    Prompt the user for a column letter.
    Returns zero-based column index if valid, otherwise None.
    Does not handle 'column full' logic here; only syntactic/semantic validation.
    """
    user_in = input(prompt).strip()
    if len(user_in) != 1:
        return None
    ch = user_in.upper()
    if ch not in COL_LABELS:
        return None
    return COL_LABELS.index(ch)


def lowest_empty_row(board: List[List[str]], col: int) -> Optional[int]:
    """
    Return the index of the lowest empty row for the given column,
    or None if the column is full.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def board_full(board: List[List[str]]) -> bool:
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def in_bounds(r: int, c: int, rows: int, cols: int) -> bool:
    return 0 <= r < rows and 0 <= c < cols


def check_win_from_cell(board: List[List[str]], r: int, c: int, token: str) -> bool:
    """
    Check if there's a winning sequence of WIN_LENGTH starting from (r, c)
    in any of the 4 directions (right, down, diag-down-right, diag-up-right).
    """
    if board[r][c] != token:
        return False

    directions: List[Tuple[int, int]] = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diag down-right
        (-1, 1),  # diag up-right
    ]
    rows = len(board)
    cols = len(board[0])
    for dr, dc in directions:
        count = 0
        rr, cc = r, c
        for _ in range(WIN_LENGTH):
            if in_bounds(rr, cc, rows, cols) and board[rr][cc] == token:
                count += 1
                rr += dr
                cc += dc
            else:
                break
        if count == WIN_LENGTH:
            return True
    return False


def check_win(board: List[List[str]], token: str) -> bool:
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == token and check_win_from_cell(board, r, c, token):
                return True
    return False


def main():
    random.seed()

    board = create_board(ROWS, COLS)

    # Choose random starting player
    current_player_index = random.randrange(NUM_PLAYERS)

    # Initial board print
    print_board(board)
    print(f"Player {PLAYER_TOKENS[current_player_index]}, you start!")

    while True:
        token = PLAYER_TOKENS[current_player_index]

        # Prompt until valid column input (letter in range).
        col_index: Optional[int] = None
        while col_index is None:
            col_index = get_column_from_input(f"Player {token}, please enter a column: ")
            if col_index is None:
                print("Invalid input. Please enter a valid column letter (e.g., A, B, C).")

        # Attempt to place checker
        row_index = lowest_empty_row(board, col_index)
        if row_index is None:
            # Column is full => turn is invalid and the player loses the turn
            print(f"Column {COL_LABELS[col_index]} is full. Turn lost.")
            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            # Show unchanged board
            print_board(board)
            continue

        # Place the checker
        board[row_index][col_index] = token

        # Print updated board
        print_board(board)

        # Check win
        if check_win(board, token):
            print(f"Player {token} won!")
            break

        # Check draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
            print("\nGame terminated.")
            sys.exit(0)
