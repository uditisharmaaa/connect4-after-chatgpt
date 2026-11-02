import os
import random
import string
from typing import List, Optional, Tuple

# -----------------------------
# Configuration (submission requirements)
# -----------------------------
ROWS = 6            # Number of rows (height)
COLS = 7            # Number of columns (width), max 26
NUM_PLAYERS = 2     # Between 2 and 5 players

# Player symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# -----------------------------
# Utility and Game Functions
# -----------------------------

def clear_screen() -> None:
    """Clear the terminal screen (Linux/Unix)."""
    os.system('clear')


def create_board(rows: int, cols: int) -> List[List[str]]:
    """Create a rows x cols board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols: int) -> List[str]:
    """Return column labels 'A'.. up to the number of columns (max 26)."""
    if cols < 1 or cols > 26:
        raise ValueError("Number of columns must be between 1 and 26.")
    return list(string.ascii_uppercase[:cols])


def print_board(board: List[List[str]]) -> None:
    """Print the board with headers and grid, clearing screen first."""
    clear_screen()
    rows, cols = len(board), len(board[0])
    headers = column_labels(cols)

    # Header row
    print("  " + "   ".join(headers))

    # Horizontal separator line
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(sep)
        # Row content
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)


def next_player_index(current: int, total: int) -> int:
    """Get the next player's index in a circular manner."""
    return (current + 1) % total


def drop_piece(board: List[List[str]], col: int, symbol: str) -> Optional[Tuple[int, int]]:
    """
    Drop a piece into the given column.
    Returns (row, col) where the piece landed, or None if the column is full.
    """
    rows = len(board)
    # Start from bottom-most row
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return (r, col)
    return None  # Column full


def in_bounds(r: int, c: int, rows: int, cols: int) -> bool:
    return 0 <= r < rows and 0 <= c < cols


def check_win(board: List[List[str]], symbol: str) -> bool:
    """
    Check if the given symbol has 4 in a row (horizontal, vertical, or diagonal).
    """
    rows, cols = len(board), len(board[0])

    # Directions: (dr, dc): right, down, diag down-right, diag down-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while count < 4 and in_bounds(nr, nc, rows, cols) and board[nr][nc] == symbol:
                    count += 1
                    nr += dr
                    nc += dc
                if count == 4:
                    return True
    return False


def check_draw(board: List[List[str]]) -> bool:
    """Return True if the board is full (no spaces), else False."""
    for row in board:
        if " " in row:
            return False
    return True


def read_player_input(valid_cols: List[str], player_symbol: str) -> str:
    """
    Read and validate user input for a column.
    Keeps asking until a valid column label from valid_cols is provided.
    Does not check whether the column is full.
    """
    while True:
        try:
            user_input = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
        except EOFError:
            # In case of EOF, keep asking (acts like invalid input)
            user_input = ""
        if len(user_input) != 1:
            continue
        if user_input in valid_cols:
            return user_input
        # If invalid, loop again without losing the turn


# -----------------------------
# Main Game Loop
# -----------------------------

def main() -> None:
    # Validate configuration
    assert 2 <= NUM_PLAYERS <= 5, "NUM_PLAYERS must be between 2 and 5."
    assert COLS <= 26, "COLS must be <= 26 (due to letter labels)."
    player_symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]

    # Initialize game
    board = create_board(ROWS, COLS)
    labels = column_labels(COLS)

    # Choose random starting player
    current_player = random.randrange(NUM_PLAYERS)

    # Show initial empty board
    print_board(board)

    # Game loop
    while True:
        symbol = player_symbols[current_player]

        # Read valid column label (does not penalize for invalid inputs)
        col_label = read_player_input(labels, symbol)
        col_index = labels.index(col_label)

        # Attempt to drop the piece
        landing = drop_piece(board, col_index, symbol)
        if landing is None:
            # Column full: turn is lost (board unchanged)
            print_board(board)
            print(f"Column {col_label} is full. Player {symbol} loses the turn.")
            current_player = next_player_index(current_player, NUM_PLAYERS)
            continue

        # Print updated board
        print_board(board)

        # Check for win
        if check_win(board, symbol):
            print(f"Player {symbol} won!")
            break

        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Next player
        current_player = next_player_index(current_player, NUM_PLAYERS)


if __name__ == "__main__":
    main()
