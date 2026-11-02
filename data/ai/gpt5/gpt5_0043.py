import os
import random
import string
from typing import List, Optional, Tuple

# =========================
# Configuration (Constants)
# =========================
ROWS = 6                 # Number of rows (default: 6)
COLS = 7                 # Number of columns (default: 7, max 26)
NUM_PLAYERS = 2          # Number of players (2 to 5)
CHECKERS = ["X", "O", "V", "H", "M"]  # In order of assignment
WIN_LENGTH = 4           # Always 4 to win as per assignment

# Safety checks to adhere to assignment constraints
assert 2 <= NUM_PLAYERS <= 5, "Number of players must be between 2 and 5."
assert 1 <= COLS <= 26, "Number of columns must be between 1 and 26."
assert ROWS >= 1, "Number of rows must be at least 1."


def clear_screen() -> None:
    """Clear the terminal screen (Linux/Unix)."""
    os.system('clear')


def create_board(rows: int, cols: int) -> List[List[str]]:
    """Create a game board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols: int) -> List[str]:
    """Generate column labels A, B, C, ... up to cols."""
    return list(string.ascii_uppercase[:cols])


def print_board(board: List[List[str]]) -> None:
    """Print the board in the specified format."""
    cols = len(board[0])
    labels = column_labels(cols)

    # Column header
    header = "  " + "   ".join(labels)
    print(header)
    # Separator line
    sep = "+" + "+".join(["---"] * cols) + "+"

    for r in range(len(board)):
        print(sep)
        # Row with cells
        row_cells = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row_cells)
    print(sep)


def get_column_index(input_str: str, cols: int) -> Optional[int]:
    """
    Convert input string to a column index if valid.
    Returns None if invalid.
    """
    if not input_str or len(input_str) != 1:
        return None
    ch = input_str.upper()
    labels = column_labels(cols)
    if ch in labels:
        return labels.index(ch)
    return None


def prompt_for_column(current_checker: str, cols: int) -> int:
    """
    Prompt the user for a valid column letter.
    Keeps prompting until the input is a valid column label.
    Returns the zero-based column index.
    """
    while True:
        user_in = input(f"Player {current_checker}, please enter a column: ").strip()
        idx = get_column_index(user_in, cols)
        if idx is not None:
            return idx
        print("Invalid input. Please enter a valid column letter.")


def find_drop_row(board: List[List[str]], col: int) -> Optional[int]:
    """
    Find the row index where a checker would land in the given column.
    Returns None if the column is full.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):  # Start from the bottom
        if board[r][col] == " ":
            return r
    return None


def drop_checker(board: List[List[str]], col: int, checker: str) -> Optional[Tuple[int, int]]:
    """
    Drop the checker into the specified column.
    Returns (row, col) where the checker was placed, or None if the column is full.
    """
    row = find_drop_row(board, col)
    if row is None:
        return None
    board[row][col] = checker
    return (row, col)


def in_bounds(r: int, c: int, rows: int, cols: int) -> bool:
    return 0 <= r < rows and 0 <= c < cols


def count_in_direction(board: List[List[str]], start_r: int, start_c: int, dr: int, dc: int, checker: str) -> int:
    """
    Count consecutive checkers matching 'checker' starting from (start_r, start_c)
    and moving in direction (dr, dc), including the starting cell.
    """
    rows, cols = len(board), len(board[0])
    count = 0
    r, c = start_r, start_c
    while in_bounds(r, c, rows, cols) and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count


def has_won(board: List[List[str]], last_r: int, last_c: int, checker: str) -> bool:
    """
    Check if placing 'checker' at (last_r, last_c) creates a winning condition.
    Checks horizontal, vertical, and both diagonal directions.
    """
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    for dr, dc in directions:
        # Count both directions from the last placed piece
        total = (
            count_in_direction(board, last_r, last_c, dr, dc, checker) +
            count_in_direction(board, last_r, last_c, -dr, -dc, checker) - 1
        )
        if total >= WIN_LENGTH:
            return True
    return False


def is_draw(board: List[List[str]]) -> bool:
    """Return True if the board is completely full (no spaces)."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def next_player_idx(current_idx: int, total_players: int) -> int:
    return (current_idx + 1) % total_players


def main() -> None:
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select starting player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Initial display
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        current_checker = players[current_player_idx]

        # Prompt for input and validate column label (not fullness)
        col = prompt_for_column(current_checker, COLS)

        # Attempt to place the checker
        placement = drop_checker(board, col, current_checker)

        # Clear and print board after the attempt
        clear_screen()

        if placement is None:
            # Column full: turn is invalid and player loses the turn
            print_board(board)
            label = column_labels(COLS)[col]
            print(f"Column {label} is full. Player {current_checker} loses the turn.")
            current_player_idx = next_player_idx(current_player_idx, NUM_PLAYERS)
            continue

        # Successful placement
        last_r, last_c = placement
        print_board(board)

        # Check for win
        if has_won(board, last_r, last_c, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if is_draw(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = next_player_idx(current_player_idx, NUM_PLAYERS)


if __name__ == "__main__":
    main()
