import os
import random
import string
import sys

# ========= Configuration (change these constants for different setups) =========
ROWS = 6               # Number of rows (default: 6)
COLUMNS = 7            # Number of columns (default: 7), must be <= 26
PLAYERS_COUNT = 2      # Number of players (between 2 and 5 inclusive)
WIN_LENGTH = 4         # Number of checkers needed in a row to win (fixed to 4)
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]  # Order of player symbols
# ==============================================================================

def clear_screen():
    """Clear the terminal screen (Linux/Unix)."""
    os.system('clear')

def validate_settings():
    """Validate configuration constants and adjust if necessary."""
    global COLUMNS, PLAYERS_COUNT
    if COLUMNS < 1 or COLUMNS > 26:
        print("COLUMNS must be between 1 and 26.", file=sys.stderr)
        sys.exit(1)
    if ROWS < 1:
        print("ROWS must be at least 1.", file=sys.stderr)
        sys.exit(1)
    if PLAYERS_COUNT < 2 or PLAYERS_COUNT > 5:
        print("PLAYERS_COUNT must be between 2 and 5.", file=sys.stderr)
        sys.exit(1)
    if WIN_LENGTH != 4:
        print("WIN_LENGTH must be 4 per assignment spec.", file=sys.stderr)
        sys.exit(1)

def make_board(rows, cols):
    """Create a rows x cols board filled with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def column_labels(cols):
    """Return a list of column labels 'A'.. up to the number of columns."""
    return list(string.ascii_uppercase[:cols])

def print_board(board):
    """Print the board with column labels and ASCII borders."""
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    labels = column_labels(cols)

    # Header with column letters
    header = "  " + "   ".join(labels)
    sep = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep)
    for r in range(rows):
        # Each row from top to bottom
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
        print(sep)

def render(board):
    """Clear the screen and print the board."""
    clear_screen()
    print_board(board)

def find_drop_row(board, col_idx):
    """
    Given a column index, return the row index where the checker should land,
    or None if the column is full.
    """
    rows = len(board)
    # Start from bottom row and go upwards
    for r in range(rows - 1, -1, -1):
        if board[r][col_idx] == " ":
            return r
    return None

def in_bounds(board, r, c):
    """Check if (r, c) is within the bounds of the board."""
    return 0 <= r < len(board) and 0 <= c < len(board[0])

def count_in_direction(board, start_r, start_c, dr, dc, symbol):
    """
    Count consecutive 'symbol' starting from (start_r, start_c) and moving in (dr, dc).
    Includes the starting cell if it matches.
    """
    r, c = start_r, start_c
    count = 0
    while in_bounds(board, r, c) and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    return count

def check_win(board, r, c, symbol):
    """
    Check if placing 'symbol' at (r, c) created a winning line of length WIN_LENGTH.
    We check four directions: horizontal, vertical, and the two diagonals.
    """
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        # Count both directions from the placed piece minus 1 to avoid double-counting the origin
        total = (
            count_in_direction(board, r, c, dr, dc, symbol) +
            count_in_direction(board, r, c, -dr, -dc, symbol) - 1
        )
        if total >= WIN_LENGTH:
            return True
    return False

def is_draw(board):
    """Return True if the board is full (no spaces left), otherwise False."""
    for row in board:
        if " " in row:
            return False
    return True

def get_valid_column_input(cols):
    """
    Prompt the user for a valid column letter.
    Keeps asking until the input is a single letter within the valid range.
    Returns the corresponding column index (0-based).
    """
    labels = column_labels(cols)
    valid_set = set(labels)

    while True:
        user_input = input().strip()
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter for the column:")
            continue
        ch = user_input.upper()
        if ch not in valid_set:
            print(f"Invalid column. Please choose between {labels[0]} and {labels[-1]}:")
            continue
        return labels.index(ch)

def main():
    validate_settings()

    # Prepare players based on count
    players = PLAYER_SYMBOLS[:PLAYERS_COUNT]

    # Initialize board and choose random starting player
    board = make_board(ROWS, COLUMNS)
    current_player_index = random.randrange(PLAYERS_COUNT)

    # Show initial board
    render(board)

    while True:
        current_symbol = players[current_player_index]
        labels = column_labels(COLUMNS)
        print(f"Player {current_symbol}, please enter a column:", end=" ")

        # Get a valid column letter from the user (does not lose turn on invalid input)
        col_idx = get_valid_column_input(COLUMNS)

        # Attempt to place the checker
        drop_row = find_drop_row(board, col_idx)
        if drop_row is None:
            # Column is full; turn is invalid and the player loses the turn
            render(board)
            print(f"Column {labels[col_idx]} is full. Turn lost.")
            # Move to next player
            current_player_index = (current_player_index + 1) % PLAYERS_COUNT
            continue

        # Place the checker
        board[drop_row][col_idx] = current_symbol

        # Show updated board
        render(board)

        # Check for win
        if check_win(board, drop_row, col_idx, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check for draw
        if is_draw(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % PLAYERS_COUNT

if __name__ == "__main__":
    main()
