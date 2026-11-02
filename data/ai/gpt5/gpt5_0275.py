import os
import random
import sys
from typing import List, Optional, Tuple

# =========================
# Configuration (constants)
# =========================
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

SYMBOLS = ["X", "O", "V", "H", "M"]  # In order
WIN_LENGTH = 4  # Always 4, regardless of board size

# Validate configuration
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if COLS > 26:
    print("COLS must be <= 26.")
    sys.exit(1)

PLAYER_SYMBOLS = SYMBOLS[:NUM_PLAYERS]


# =========================
# Utility functions
# =========================
def clear_screen() -> None:
    """Clear the terminal screen (Linux/Unix)."""
    os.system('clear')


def create_board(rows: int, cols: int) -> List[List[str]]:
    """Create a rows x cols board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board: List[List[str]]) -> None:
    """Print the board with column headers A.. and ASCII grid."""
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header letters
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(header)

    horizontal = "+" + "+".join("---" for _ in range(cols)) + "+"

    for r in range(rows):
        print(horizontal)
        row_cells = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row_cells)
    print(horizontal)


def is_valid_column_input(user_input: str, cols: int) -> bool:
    """Return True if user_input is a single letter within the column range."""
    if len(user_input) != 1:
        return False
    ch = user_input.upper()
    if not ('A' <= ch <= 'Z'):
        return False
    col_index = ord(ch) - ord('A')
    return 0 <= col_index < cols


def column_index_from_input(user_input: str) -> int:
    """Convert a valid letter input to a zero-based column index."""
    return ord(user_input.upper()) - ord('A')


def drop_checker(board: List[List[str]], col: int, symbol: str) -> Optional[Tuple[int, int]]:
    """
    Drop a checker into the given column.
    Returns (row, col) where placed, or None if the column is full.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return r, col
    return None


def check_win(board: List[List[str]], symbol: str) -> bool:
    """Check if the given symbol has a sequence of WIN_LENGTH in any direction."""
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    L = WIN_LENGTH

    # Directions: (dr, dc)
    directions = [
        (0, 1),    # right
        (1, 0),    # down
        (1, 1),    # down-right
        (1, -1),   # down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                end_r = r + (L - 1) * dr
                end_c = c + (L - 1) * dc
                # Check bounds for the end of the segment
                if not (0 <= end_r < rows and 0 <= end_c < cols):
                    continue
                win = True
                for k in range(1, L):
                    rr = r + k * dr
                    cc = c + k * dc
                    if board[rr][cc] != symbol:
                        win = False
                        break
                if win:
                    return True
    return False


def check_draw(board: List[List[str]]) -> bool:
    """Return True if the board is full (no spaces)."""
    return all(cell != " " for row in board for cell in row)


def prompt_player(symbol: str, cols: int) -> str:
    """Prompt for a valid column letter; re-prompt on invalid input."""
    while True:
        user_input = input(f"Player {symbol}, please enter a column: ").strip()
        if is_valid_column_input(user_input, cols):
            return user_input.upper()
        print("Invalid input. Enter a single uppercase letter within the board (e.g., A, B, C...).")


def game_loop() -> None:
    """Run a single game of Connect 4 with configured constants."""
    board = create_board(ROWS, COLS)
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial board display
    clear_screen()
    print_board(board)

    while True:
        symbol = PLAYER_SYMBOLS[current_player_idx]
        # Prompt until a valid column letter is provided (does not lose turn on invalid input)
        col_letter = prompt_player(symbol, COLS)
        col_idx = column_index_from_input(col_letter)

        # Attempt to drop the checker
        placed = drop_checker(board, col_idx, symbol)

        # After action, refresh screen and show updated board (even if move failed)
        clear_screen()
        print_board(board)

        if placed is None:
            # Column full: the turn is invalid and the player loses the turn
            print(f"Column {col_letter} is full. Player {symbol} loses the turn.")
            # Next player's turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Successful placement; check for win
        if check_win(board, symbol):
            print(f"Player {symbol} won!")
            break

        # Check for draw
        if check_draw(board):
            print("Game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


def main() -> None:
    random.seed()
    game_loop()


if __name__ == "__main__":
    main()
