import os
import random
import string
from typing import List, Optional, Tuple

# -------------------------------
# Configuration (submission requires 6 rows x 7 columns and 2 players)
# -------------------------------
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5 inclusive
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]  # In order for up to 5 players

# -------------------------------
# Board creation and printing
# -------------------------------

def create_board(rows: int, cols: int) -> List[List[str]]:
    """Create a rows x cols board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def clear_screen() -> None:
    """Clear terminal screen."""
    os.system('clear')  # As required by the assignment


def column_labels(cols: int) -> List[str]:
    """Return list of column labels ['A', 'B', ...]."""
    return list(string.ascii_uppercase[:cols])


def print_board(board: List[List[str]]) -> None:
    """Print the board in the specified ASCII format."""
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    labels = column_labels(cols)

    # Header with column letters
    print("  " + "   ".join(labels))
    # Board rows
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)


# -------------------------------
# Game mechanics
# -------------------------------

def is_valid_column_letter(s: str, cols: int) -> bool:
    """Check if s is a single uppercase letter within board columns."""
    if len(s) != 1 or not s.isalpha() or not s.isupper():
        return False
    idx = ord(s) - ord('A')
    return 0 <= idx < cols


def get_column_index_from_letter(letter: str) -> int:
    """Map column letter (A..) to zero-based index."""
    return ord(letter) - ord('A')


def get_player_input(current_checker: str, cols: int) -> int:
    """
    Prompt until a valid uppercase column letter is given.
    Returns zero-based column index.
    """
    labels = column_labels(cols)
    while True:
        user_in = input(f"Player {current_checker}, please enter a column: ").strip()
        # Accept lowercase by converting to uppercase, but enforce letter validity and range
        user_in = user_in.upper()
        if not is_valid_column_letter(user_in, cols):
            print(f"Invalid input. Please enter one of: {', '.join(labels)}")
            continue
        return get_column_index_from_letter(user_in)


def find_drop_row(board: List[List[str]], col: int) -> Optional[int]:
    """
    Find the lowest available row in the given column.
    Returns row index or None if column is full.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def place_checker(board: List[List[str]], col: int, checker: str) -> Optional[Tuple[int, int]]:
    """
    Place checker in the specified column if possible.
    Returns (row, col) where placed, or None if column is full.
    """
    row = find_drop_row(board, col)
    if row is None:
        return None
    board[row][col] = checker
    return (row, col)


def in_bounds(r: int, c: int, rows: int, cols: int) -> bool:
    return 0 <= r < rows and 0 <= c < cols


def check_win_from_cell(board: List[List[str]], r: int, c: int, checker: str) -> bool:
    """Check all directions for WIN_LENGTH in a row starting at cell (r, c)."""
    if board[r][c] != checker:
        return False

    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 0
        rr, cc = r, c
        for _ in range(WIN_LENGTH):
            if in_bounds(rr, cc, rows, cols) and board[rr][cc] == checker:
                count += 1
                rr += dr
                cc += dc
            else:
                break
        if count == WIN_LENGTH:
            return True
    return False


def check_win(board: List[List[str]], checker: str) -> bool:
    """Check if the given checker has a winning line of WIN_LENGTH."""
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            if check_win_from_cell(board, r, c, checker):
                return True
    return False


def board_full(board: List[List[str]]) -> bool:
    """Return True if the board has no empty spaces."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def next_player_index(current: int, total: int) -> int:
    return (current + 1) % total


# -------------------------------
# Main game loop
# -------------------------------

def main() -> None:
    # Basic validations according to specs
    assert 2 <= NUM_PLAYERS <= 5, "Number of players must be between 2 and 5."
    assert 1 <= COLS <= 26, "Number of columns must be between 1 and 26."

    players = CHECKERS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    # Randomly select starting player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Initial board display
    print_board(board)
    print(f"Player {players[current_player_idx]} starts.")

    # Game loop
    while True:
        # Show board and prompt for input
        print_board(board)

        current_checker = players[current_player_idx]
        col_idx = get_player_input(current_checker, COLS)

        # Try to place checker
        placement = place_checker(board, col_idx, current_checker)
        if placement is None:
            # Column full: turn is invalid and player loses the turn
            chosen_label = column_labels(COLS)[col_idx]
            print_board(board)
            print(f"Column {chosen_label} is full. Player {current_checker} loses the turn.")
            # Move to next player
            current_player_idx = next_player_index(current_player_idx, NUM_PLAYERS)
            continue

        # After placing, check for win
        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if board_full(board):
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = next_player_index(current_player_idx, NUM_PLAYERS)


if __name__ == "__main__":
    main()
