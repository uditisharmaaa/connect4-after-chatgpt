import os
import random
import string
from typing import List, Optional, Tuple

# ------------------------------ Configuration ------------------------------
# Board dimensions (rows and columns). Submission requires 6x7.
ROWS = 6
COLS = 7  # Must be <= 26 (letters A-Z)

# Number of players (between 2 and 5). Submission requires 2 players.
NUM_PLAYERS = 2

# Checker symbols in order. Players are assigned from this list in order.
CHECKERS = ["X", "O", "V", "H", "M"]

# Number of connected checkers required to win (always 4 for this assignment).
CONNECT_N = 4
# ---------------------------------------------------------------------------


def clear_screen() -> None:
    """Clear the terminal screen (Linux/Unix)."""
    os.system('clear')


def create_board(rows: int, cols: int) -> List[List[str]]:
    """Create a board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols: int) -> List[str]:
    """Return list of column labels A, B, C, ... up to number of columns."""
    return list(string.ascii_uppercase[:cols])


def print_board(board: List[List[str]]) -> None:
    """Print the board to the terminal in the required format."""
    rows = len(board)
    cols = len(board[0])
    labels = column_labels(cols)

    # Header
    print("  " + "   ".join(labels))
    # Separator line
    horizontal = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(horizontal)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(horizontal)


def get_player_symbols(num_players: int) -> List[str]:
    """Return the list of checker symbols for the number of players."""
    return CHECKERS[:num_players]


def prompt_for_column(current_symbol: str, cols: int) -> int:
    """
    Prompt the user for a column letter and validate input.
    Returns the column index (0-based). Keeps asking until a valid letter is provided.
    Does not handle 'full column' (that is handled by placement).
    """
    valid_labels = column_labels(cols)
    last_label = valid_labels[-1]

    while True:
        try:
            user_input = input(f"Player {current_symbol}, please enter a column: ").strip()
        except EOFError:
            # In case of non-interactive environment; treat as invalid and keep prompting
            user_input = ""

        if len(user_input) != 1:
            print(f"Invalid input. Please enter a single letter between A and {last_label}.")
            continue

        ch = user_input.upper()
        if not ch.isalpha():
            print(f"Invalid input. Please enter a letter between A and {last_label}.")
            continue

        if ch not in valid_labels:
            print(f"Out of range. Please enter a letter between A and {last_label}.")
            continue

        return valid_labels.index(ch)


def place_checker(board: List[List[str]], col: int, symbol: str) -> Optional[Tuple[int, int]]:
    """
    Place the checker in the lowest available row of the given column.
    Returns (row_index, col_index) if placed, or None if the column is full.
    """
    rows = len(board)
    # Start from bottom-most row
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return (r, col)
    return None  # Column full


def in_bounds(r: int, c: int, rows: int, cols: int) -> bool:
    """Check if a cell is inside the board bounds."""
    return 0 <= r < rows and 0 <= c < cols


def check_win(board: List[List[str]], start_r: int, start_c: int, symbol: str) -> bool:
    """
    Check if placing 'symbol' at (start_r, start_c) created a winning line
    of length CONNECT_N. Checks horizontal, vertical, and two diagonals.
    """
    rows = len(board)
    cols = len(board[0])

    # Direction vectors: horizontal, vertical, diag down-right, diag down-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for dr, dc in directions:
        count = 1  # Count includes the starting cell

        # Extend in the positive direction
        r, c = start_r + dr, start_c + dc
        while in_bounds(r, c, rows, cols) and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc

        # Extend in the negative direction
        r, c = start_r - dr, start_c - dc
        while in_bounds(r, c, rows, cols) and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc

        if count >= CONNECT_N:
            return True

    return False


def board_full(board: List[List[str]]) -> bool:
    """Return True if there are no empty cells left on the board."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def main() -> None:
    # Basic validations
    if COLS < 1 or COLS > 26:
        raise ValueError("COLS must be between 1 and 26.")
    if ROWS < 1:
        raise ValueError("ROWS must be >= 1.")
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")

    board = create_board(ROWS, COLS)
    player_symbols = get_player_symbols(NUM_PLAYERS)

    # Randomly select starting player
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial board display
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        current_symbol = player_symbols[current_player_idx]

        # Ask current player for a valid column letter
        col = prompt_for_column(current_symbol, COLS)

        # Try placing the checker
        placement = place_checker(board, col, current_symbol)
        if placement is None:
            # Column full: player loses the turn
            clear_screen()
            print_board(board)
            labels = column_labels(COLS)
            print(f"Column {labels[col]} is full. Player {current_symbol} loses the turn.")
            # Advance to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        placed_r, placed_c = placement

        # After a valid placement, check for a win
        if check_win(board, placed_r, placed_c, current_symbol):
            clear_screen()
            print_board(board)
            print(f"Player {current_symbol} won!")
            break

        # Check for a draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

        # Show updated board for next turn
        clear_screen()
        print_board(board)


if __name__ == "__main__":
    main()
