import os
import random
import string
from typing import List, Optional, Tuple

# ----------------------- Configuration (constants) -----------------------

# Board size (rows x columns). Standard Connect 4 is 6 rows x 7 columns.
ROWS = 6
COLS = 7  # Max 26 columns (A-Z)

# Number of players (between 2 and 5)
NUM_PLAYERS = 2

# Player checkers in order; use the first NUM_PLAYERS of this list
CHECKERS = ["X", "O", "V", "H", "M"]

# Number in a row to win
WIN_LENGTH = 4


# ----------------------- Utility and Game Logic -----------------------

def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('clear')


def create_board(rows: int, cols: int) -> List[List[str]]:
    """Create a board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols: int) -> List[str]:
    """Return list of column labels starting from 'A' up to the number of columns."""
    if cols < 1 or cols > 26:
        raise ValueError("Number of columns must be between 1 and 26.")
    return list(string.ascii_uppercase[:cols])


def print_board(board: List[List[str]]) -> None:
    """Print the board with column labels and grid lines."""
    cols = len(board[0])
    labels = column_labels(cols)

    # Header labels
    print("  " + "   ".join(labels))

    # Horizontal separator line
    hline = "+" + "+".join(["---"] * cols) + "+"
    for r in range(len(board)):
        print(hline)
        row_cells = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row_cells)
    print(hline)


def is_valid_column_input(user_input: str, cols: int) -> bool:
    """Validate that input is a single letter within the column range."""
    if not isinstance(user_input, str) or len(user_input.strip()) != 1:
        return False
    ch = user_input.strip().upper()
    if ch < "A" or ch > chr(ord("A") + cols - 1):
        return False
    return True


def col_index_from_input(user_input: str) -> int:
    """Convert a valid column letter to a zero-based column index."""
    return ord(user_input.strip().upper()) - ord("A")


def drop_checker(board: List[List[str]], col: int, checker: str) -> Optional[Tuple[int, int]]:
    """
    Drop a checker into the given column.
    Returns (row, col) if placed, or None if the column is full.
    """
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None  # Column full


def in_bounds(board: List[List[str]], r: int, c: int) -> bool:
    """Check if (r, c) is within board bounds."""
    return 0 <= r < len(board) and 0 <= c < len(board[0])


def count_in_direction(board: List[List[str]], start_r: int, start_c: int, dr: int, dc: int, checker: str) -> int:
    """Count consecutive checkers from a starting cell in a direction (dr, dc)."""
    r, c = start_r + dr, start_c + dc
    count = 0
    while in_bounds(board, r, c) and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count


def check_win(board: List[List[str]], last_r: int, last_c: int, checker: str) -> bool:
    """
    Check for a win condition including the last placed checker.
    Looks in four lines: horizontal, vertical, two diagonals.
    """
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    for dr, dc in directions:
        total = 1  # Include the last placed checker
        total += count_in_direction(board, last_r, last_c, dr, dc, checker)
        total += count_in_direction(board, last_r, last_c, -dr, -dc, checker)
        if total >= WIN_LENGTH:
            return True
    return False


def board_full(board: List[List[str]]) -> bool:
    """Return True if the board is full (no spaces)."""
    return all(cell != " " for row in board for cell in row)


def prompt_for_column(current_checker: str, cols: int) -> str:
    """
    Prompt the current player for a column letter.
    Keeps asking until a valid input is entered (column letter within range).
    """
    labels_end = chr(ord("A") + cols - 1)
    while True:
        user_input = input(f"Player {current_checker}, please enter a column: ").strip()
        if is_valid_column_input(user_input, cols):
            return user_input.strip().upper()
        # Invalid input; ask again without losing the turn
        # Optionally, we could display a brief message, but keep it simple and re-prompt.


def run_game(rows: int, cols: int, num_players: int) -> None:
    """Run a game of Connect 4 with the given configuration."""
    assert 2 <= num_players <= 5, "Number of players must be between 2 and 5."
    assert 1 <= cols <= 26, "Number of columns must be between 1 and 26."
    players = CHECKERS[:num_players]

    board = create_board(rows, cols)
    current_idx = random.randrange(num_players)  # Randomly select the first player

    # Show initial empty board before the first move
    clear_screen()
    print_board(board)

    while True:
        current_checker = players[current_idx]

        # Prompt and validate input letter (reprompt if invalid input/format/out-of-range)
        col_letter = prompt_for_column(current_checker, cols)
        col = col_index_from_input(col_letter)

        # Attempt to drop checker; if column is full, the player's turn is lost
        placement = drop_checker(board, col, current_checker)
        if placement is None:
            # Turn invalid due to full column; lose turn and continue
            # Redraw updated board (no change) before next player's turn
            clear_screen()
            print_board(board)
            # Advance to next player
            current_idx = (current_idx + 1) % num_players
            continue

        last_r, last_c = placement

        # After a successful move, check for win or draw
        if check_win(board, last_r, last_c, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        if board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        clear_screen()
        print_board(board)
        current_idx = (current_idx + 1) % num_players


# ----------------------- Entry Point -----------------------

if __name__ == "__main__":
    run_game(ROWS, COLS, NUM_PLAYERS)
