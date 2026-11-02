import os
import random
import sys
from typing import List, Optional, Tuple

# =========================
# Configuration (constants)
# =========================
# Submission requires 6 rows x 7 columns and 2 players enabled.
N_ROWS: int = 6
N_COLS: int = 7  # Max 26 columns (A-Z)
N_PLAYERS: int = 2  # Supported: 2..5 players

# Player checkers in order
CHECKERS: Tuple[str, ...] = ("X", "O", "V", "H", "M")


# =========================
# Utility / Core functions
# =========================
def clear_screen() -> None:
    """Clear the terminal screen using Unix 'clear'."""
    os.system('clear')


def create_board(rows: int, cols: int) -> List[List[str]]:
    """Create an empty board of size rows x cols filled with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols: int) -> List[str]:
    """Return column labels A, B, C, ... up to number of columns."""
    if cols < 1 or cols > 26:
        raise ValueError("Number of columns must be between 1 and 26.")
    return [chr(ord('A') + i) for i in range(cols)]


def print_board(board: List[List[str]]) -> None:
    """Clear screen and print the board in the required format."""
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    labels = column_labels(cols)

    # Header with column labels
    print("  " + "   ".join(labels))
    # Top border
    print("+" + "+".join(["---"] * cols) + "+")
    # Rows
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + "+".join(["---"] * cols) + "+")


def get_valid_column_input(valid_labels: List[str]) -> str:
    """
    Prompt the user until they provide a syntactically valid column input.
    Valid means: a single letter corresponding to available column labels (case-insensitive).
    Does not check for fullness of the column; just that the input refers to a real column.
    """
    prompt = "Please enter a column: "
    while True:
        try:
            raw = input(prompt)
        except (EOFError, KeyboardInterrupt):
            print("\nExiting game.")
            sys.exit(0)

        user_in = raw.strip().upper()
        if len(user_in) != 1 or not user_in.isalpha():
            print("Invalid input. Enter a single column letter (e.g., A, B, C).")
            continue

        if user_in not in valid_labels:
            print(f"Invalid column. Choose one of: {', '.join(valid_labels)}.")
            continue

        return user_in


def drop_checker(board: List[List[str]], col_idx: int, symbol: str) -> Optional[int]:
    """
    Drop a checker into the specified column index.
    Returns the row index where the checker lands, or None if the column is full.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = symbol
            return r
    return None  # Column full


def check_direction(board: List[List[str]], start_r: int, start_c: int,
                    delta_r: int, delta_c: int, symbol: str) -> bool:
    """Check four in a row starting at (start_r,start_c) moving by (delta_r,delta_c)."""
    rows = len(board)
    cols = len(board[0])
    for k in range(4):
        r = start_r + k * delta_r
        c = start_c + k * delta_c
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if board[r][c] != symbol:
            return False
    return True


def check_win(board: List[List[str]], symbol: str) -> bool:
    """Check if the given symbol has 4 in a row (horizontal, vertical, or diagonal)."""
    rows = len(board)
    cols = len(board[0])

    # Horizontal and Vertical
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            # Horizontal right
            if c + 3 < cols and check_direction(board, r, c, 0, 1, symbol):
                return True
            # Vertical down
            if r + 3 < rows and check_direction(board, r, c, 1, 0, symbol):
                return True
            # Diagonal down-right
            if r + 3 < rows and c + 3 < cols and check_direction(board, r, c, 1, 1, symbol):
                return True
            # Diagonal down-left
            if r + 3 < rows and c - 3 >= 0 and check_direction(board, r, c, 1, -1, symbol):
                return True

    return False


def board_full(board: List[List[str]]) -> bool:
    """Return True if the board has no empty spaces."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


# =========================
# Game loop
# =========================
def main() -> None:
    # Validate configuration
    if not (2 <= N_PLAYERS <= 5):
        raise ValueError("N_PLAYERS must be between 2 and 5.")
    if not (1 <= N_COLS <= 26):
        raise ValueError("N_COLS must be between 1 and 26.")
    if N_ROWS < 1:
        raise ValueError("N_ROWS must be at least 1.")

    board = create_board(N_ROWS, N_COLS)
    labels = column_labels(N_COLS)
    players = list(CHECKERS[:N_PLAYERS])

    # Randomly choose starting player index
    current_idx = random.randrange(N_PLAYERS)

    # Initial board display
    print_board(board)
    print(f"Player {players[current_idx]}, please enter a column:")

    # Game loop
    while True:
        # Prompt until syntactically valid column
        col_label = get_valid_column_input(labels)
        col_idx = labels.index(col_label)

        # Attempt to drop checker
        row_placed = drop_checker(board, col_idx, players[current_idx])

        # Print updated board (or unchanged if column was full)
        print_board(board)

        if row_placed is None:
            # Column full: turn is invalid and the player loses the turn.
            print(f"Column {col_label} is full. Player {players[current_idx]} loses the turn.")
            # Switch player
            current_idx = (current_idx + 1) % N_PLAYERS
            print(f"Player {players[current_idx]}, please enter a column:")
            continue

        # Check for win
        if check_win(board, players[current_idx]):
            print(f"Player {players[current_idx]} won!")
            break

        # Check for draw
        if board_full(board):
            print("It's a draw!")
            break

        # Switch to next player
        current_idx = (current_idx + 1) % N_PLAYERS
        print(f"Player {players[current_idx]}, please enter a column:")


if __name__ == "__main__":
    main()
