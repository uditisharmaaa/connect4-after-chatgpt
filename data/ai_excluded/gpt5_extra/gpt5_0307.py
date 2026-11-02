import os
import random
import string
from typing import List, Optional, Tuple

# ====== Configurable constants (adjustable for testing) ======
ROWS = 6
COLS = 7  # Max 26 (A-Z)
NUM_PLAYERS = 2  # Supported range: 2..5
PLAYER_TOKENS = ['X', 'O', 'V', 'H', 'M']
WIN_LENGTH = 4  # Always 4 per assignment
CLEAR_CMD = 'clear'  # Linux/Unix
# =============================================================


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system(CLEAR_CMD)


def create_board(rows: int, cols: int) -> List[List[str]]:
    """Create a board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols: int) -> List[str]:
    """Return list of column labels A.. up to cols."""
    return list(string.ascii_uppercase[:cols])


def print_board(board: List[List[str]]) -> None:
    """Clear the screen and print the board with column labels and grid."""
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    labels = column_labels(cols)
    # Header
    print("  " + "   ".join(labels))
    # Grid
    horiz = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(horiz)
        row_cells = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row_cells)
    print(horiz)


def prompt_for_column(current_token: str, cols: int) -> int:
    """
    Prompt the user for a column letter and validate.
    Returns the column index (0-based). Keeps prompting until valid input.
    Invalid inputs (non-letters, out-of-range) do not consume the turn.
    """
    labels = column_labels(cols)
    label_set = set(labels)
    while True:
        user_input = input(f"Player {current_token}, please enter a column: ").strip()
        if not user_input:
            print("Invalid input. Please enter a single letter corresponding to a column.")
            continue
        # Normalize to uppercase and take only the first non-space token if multiple chars
        col_label = user_input.upper()[0]
        if col_label in label_set:
            return labels.index(col_label)
        print(f"Invalid column. Please enter one of: {', '.join(labels)}")


def lowest_empty_row(board: List[List[str]], col: int) -> Optional[int]:
    """Return the lowest empty row index in a given column, or None if column is full."""
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def drop_checker(board: List[List[str]], col: int, token: str) -> Optional[Tuple[int, int]]:
    """
    Place the token in the lowest available cell in the specified column.
    Returns (row, col) if placed, or None if the column is full.
    """
    r = lowest_empty_row(board, col)
    if r is None:
        return None
    board[r][col] = token
    return r, col


def in_bounds(r: int, c: int, rows: int, cols: int) -> bool:
    return 0 <= r < rows and 0 <= c < cols


def check_win(board: List[List[str]], token: str) -> bool:
    """
    Check if the given token has a winning sequence of WIN_LENGTH
    horizontally, vertically, or diagonally.
    """
    rows = len(board)
    cols = len(board[0]) if rows else 0
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while in_bounds(nr, nc, rows, cols) and board[nr][nc] == token:
                    count += 1
                    if count >= WIN_LENGTH:
                        return True
                    nr += dr
                    nc += dc
    return False


def is_draw(board: List[List[str]]) -> bool:
    """Return True if the board has no empty cells."""
    for row in board:
        if " " in row:
            return False
    return True


def select_start_player(num_players: int) -> int:
    """Randomly select the index of the starting player."""
    return random.randrange(num_players)


def validate_configuration() -> None:
    """Ensure configuration constants are within supported constraints."""
    assert 2 <= NUM_PLAYERS <= 5, "NUM_PLAYERS must be between 2 and 5."
    assert 1 <= COLS <= 26, "COLS must be between 1 and 26."
    assert ROWS >= 1, "ROWS must be a positive integer."
    assert WIN_LENGTH >= 1, "WIN_LENGTH must be a positive integer."
    assert len(PLAYER_TOKENS) >= NUM_PLAYERS, "Not enough player tokens provided."
    # WIN_LENGTH logically cannot exceed both dimensions; but assignment fixes it to 4.


def main() -> None:
    validate_configuration()

    tokens = PLAYER_TOKENS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    # Random start player
    current_player_idx = select_start_player(NUM_PLAYERS)

    # Show initial board
    print_board(board)

    # Game loop
    while True:
        current_token = tokens[current_player_idx]

        # If board is already full (draw), end game
        if is_draw(board):
            print("The game is a draw!")
            break

        # Prompt until valid column input (letter within range)
        col_idx = prompt_for_column(current_token, COLS)

        # Attempt to drop checker
        drop_result = drop_checker(board, col_idx, current_token)
        if drop_result is None:
            # Column full: turn is invalid and player loses the turn
            print_board(board)
            col_label = column_labels(COLS)[col_idx]
            print(f"Column {col_label} is full. Player {current_token} loses the turn.")
        else:
            # Successful placement: print updated board and check win/draw
            print_board(board)
            if check_win(board, current_token):
                print(f"Player {current_token} won!")
                break
            if is_draw(board):
                print("The game is a draw!")
                break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
