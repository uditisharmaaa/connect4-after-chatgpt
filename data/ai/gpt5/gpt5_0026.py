import os
import random
import string
import sys

# ------------------------------
# Connect 4 - Python 3
# ------------------------------
# This program implements a configurable Connect 4 game playable in a terminal.
# It supports:
# - Variable board dimensions (up to 26 columns)
# - 2 to 5 players with predefined checker symbols
# - Random starting player
# - Input validation
# - Turn skipping when a chosen column is full
# - Win checking (horizontal, vertical, and both diagonals)
# - Draw detection
#
# Note: For submission, the constants below are set to 6 rows x 7 columns and 2 players.
# ------------------------------

# ------------------------------
# Configuration constants
# ------------------------------
ROWS = 6                 # Number of rows (e.g., 6)
COLS = 7                 # Number of columns (e.g., 7); must be <= 26
NUM_PLAYERS = 2          # Number of players (2 to 5)

# Checker symbols in order of assignment to players
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# Number of consecutive checkers needed to win
WIN_LENGTH = 4

# ------------------------------
# Validation of configuration
# ------------------------------
if not (2 <= NUM_PLAYERS <= 5):
    print("Error: NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if COLS < 1 or COLS > 26:
    print("Error: COLS must be between 1 and 26.")
    sys.exit(1)

if ROWS < 1:
    print("Error: ROWS must be at least 1.")
    sys.exit(1)

# Assign symbols for the number of players
ACTIVE_SYMBOLS = PLAYER_SYMBOLS[:NUM_PLAYERS]

# Precompute column labels A, B, C, ... up to COLS
COLUMN_LABELS = list(string.ascii_uppercase[:COLS])


# ------------------------------
# Utility functions
# ------------------------------
def clear_screen():
    """Clear the terminal screen (Linux/Unix)."""
    os.system('clear')


def create_board(rows, cols):
    """Create and return an empty board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Print the board with headers and grid lines."""
    clear_screen()
    # Header: column labels
    header = "  " + "   ".join(COLUMN_LABELS)
    print(header)
    # Top border
    print("+" + "---+" * COLS)
    # Each row
    for r in range(ROWS):
        row_cells = []
        for c in range(COLS):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + "---+" * COLS)


def is_board_full(board):
    """Return True if the board has no empty cells."""
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True


def validate_input(user_input):
    """
    Validate user input:
    - Must be a single letter corresponding to an existing column label.
    Returns the column index if valid, otherwise None.
    """
    if not user_input:
        return None
    token = user_input.strip().upper()
    if len(token) != 1:
        return None
    if token not in COLUMN_LABELS:
        return None
    return COLUMN_LABELS.index(token)


def drop_checker(board, col, symbol):
    """
    Attempt to place 'symbol' into column 'col'.
    The checker falls to the lowest available row.
    Returns the row index where the checker is placed, or None if the column is full.
    """
    # Start from bottom row and find the first empty cell
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return r
    # Column is full
    return None


def count_in_direction(board, start_r, start_c, dr, dc, symbol):
    """
    Count consecutive 'symbol' pieces starting from (start_r, start_c),
    moving in direction (dr, dc), excluding the starting cell.
    """
    r, c = start_r + dr, start_c + dc
    count = 0
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    return count


def check_win(board, last_r, last_c, symbol):
    """
    Check if placing 'symbol' at (last_r, last_c) creates a winning line.
    We check 4 directions: horizontal, vertical, diag down-right, diag up-right.
    For each direction, count both forward and backward and add 1 for the last move.
    """
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (-1, 1),  # diagonal up-right
    ]
    for dr, dc in directions:
        total = 1  # include the last placed checker
        total += count_in_direction(board, last_r, last_c, dr, dc, symbol)
        total += count_in_direction(board, last_r, last_c, -dr, -dc, symbol)
        if total >= WIN_LENGTH:
            return True
    return False


# ------------------------------
# Main game loop
# ------------------------------
def main():
    # Create board
    board = create_board(ROWS, COLS)

    # Randomly select starting player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Show the initial board and prompt the first player
    print_board(board)

    # Game loop
    while True:
        # If board is full before a turn, it's a draw
        if is_board_full(board):
            print("The game is a draw!")
            break

        current_symbol = ACTIVE_SYMBOLS[current_player_idx]
        prompt = f"Player {current_symbol}, please enter a column: "

        # Get valid input (reprompt until valid column letter)
        col_idx = None
        while col_idx is None:
            user_in = input(prompt)
            col_idx = validate_input(user_in)
            if col_idx is None:
                print("Invalid input. Please enter a valid column letter (e.g., A, B, C).")

        # Attempt to drop the checker
        placed_row = drop_checker(board, col_idx, current_symbol)
        if placed_row is None:
            # Column full: player loses the turn
            print_board(board)
            print(f"Column {COLUMN_LABELS[col_idx]} is full. Player {current_symbol} loses the turn.")
            # Advance to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Successfully placed; print updated board
        print_board(board)

        # Check for a win
        if check_win(board, placed_row, col_idx, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check for draw after a valid move
        if is_board_full(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
