import os
import random
import sys

# =========================
# Configuration constants
# =========================
ROWS = 6                  # Number of rows (default submission setting)
COLS = 7                  # Number of columns (default submission setting, max 26)
NUM_PLAYERS = 2           # Number of players (2 to 5 for this assignment)
TOKENS = ["X", "O", "V", "H", "M"]  # Order of tokens
WIN_LENGTH = 4            # Number of checkers in a row needed to win (always 4)

# =========================
# Validation of constants
# =========================
if COLS > 26:
    print("Error: Maximum supported columns is 26.")
    sys.exit(1)

if not (2 <= NUM_PLAYERS <= 5):
    print("Error: Number of players must be between 2 and 5.")
    sys.exit(1)

PLAYER_TOKENS = TOKENS[:NUM_PLAYERS]


# =========================
# Utility functions
# =========================
def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')


def create_board(rows, cols):
    """Create a board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    """Return list of column labels as uppercase letters starting from 'A'."""
    return [chr(ord('A') + i) for i in range(cols)]


def print_board(board):
    """Print the board in the required ASCII format with column labels."""
    labels = column_labels(len(board[0]))
    # Header with column letters
    header = "  " + "   ".join(labels)
    sep = "+" + "+".join(["---"] * len(labels)) + "+"

    print(header)
    print(sep)
    for r in range(len(board)):
        row_cells = []
        for c in range(len(board[0])):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
        print(sep)


def is_valid_column_input(user_input, cols):
    """Validate that user_input is a single letter within A..A+cols-1."""
    if not user_input:
        return False
    s = user_input.strip().upper()
    if len(s) != 1:
        return False
    if not s.isalpha():
        return False
    label_min = 'A'
    label_max = chr(ord('A') + cols - 1)
    return label_min <= s <= label_max


def column_index_from_input(user_input):
    """Convert validated input letter to zero-based column index."""
    s = user_input.strip().upper()
    return ord(s) - ord('A')


def find_drop_row(board, col):
    """Return the row index where a checker would land in the given column, or None if column full."""
    for r in reversed(range(len(board))):
        if board[r][col] == " ":
            return r
    return None


def place_checker(board, col, token):
    """Place a checker in the given column if possible. Return (row_index or None)."""
    row = find_drop_row(board, col)
    if row is None:
        return None
    board[row][col] = token
    return row


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_winner(board, last_row, last_col, token):
    """
    Check if placing 'token' at (last_row, last_col) created a connect-4.
    We only need to check lines through this last placed position.
    """
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # Counting the last placed checker
        # Extend in positive direction
        r, c = last_row + dr, last_col + dc
        while in_bounds(r, c, rows, cols) and board[r][c] == token:
            count += 1
            r += dr
            c += dc
        # Extend in negative direction
        r, c = last_row - dr, last_col - dc
        while in_bounds(r, c, rows, cols) and board[r][c] == token:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_LENGTH:
            return True

    return False


def is_draw(board):
    """Return True if the board is full (no spaces)."""
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def prompt_for_column(token, cols):
    """Prompt the current player for a valid column letter and return the zero-based index."""
    while True:
        try:
            user_input = input(f"Player {token}, please enter a column: ").strip()
        except EOFError:
            # If input stream is closed, gracefully exit
            print()
            sys.exit(0)

        if not is_valid_column_input(user_input, cols):
            print("Invalid input. Please enter a single uppercase letter within the board's columns.")
            continue
        return column_index_from_input(user_input)


# =========================
# Main game loop
# =========================
def main():
    board = create_board(ROWS, COLS)
    current_player_index = random.randrange(NUM_PLAYERS)

    # Initial display
    clear_screen()
    print_board(board)

    while True:
        token = PLAYER_TOKENS[current_player_index]
        cols = COLS

        # Prompt for valid column letter
        col = prompt_for_column(token, cols)

        # Attempt to place checker
        drop_row = place_checker(board, col, token)

        if drop_row is None:
            # Column full -> player loses the turn
            print(f"Column {chr(ord('A') + col)} is full. Invalid turn - Player {token} loses the turn.")
            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            # After a successful move, clear screen and print updated board
            clear_screen()
            print_board(board)

            # Check for win
            if check_winner(board, drop_row, col, token):
                print(f"Player {token} won!")
                break

            # Check for draw
            if is_draw(board):
                print("Game is a draw.")
                break

            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
