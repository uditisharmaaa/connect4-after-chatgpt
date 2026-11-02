import os
import random
import string
import sys

# ==========================
# Configuration (Constants)
# ==========================
ROWS = 6               # number of rows (default submission requires 6)
COLS = 7               # number of columns (default submission requires 7)
NUM_PLAYERS = 2        # number of players (between 2 and 5 inclusive)
TOKENS = ["X", "O", "V", "H", "M"]  # in order as specified
WIN_LENGTH = 4         # number of checkers in a row needed to win
MAX_COLS = 26          # cannot exceed 26 columns due to A..Z labeling

# Validate configuration
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    print("Error: NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if COLS < 1 or COLS > MAX_COLS:
    print(f"Error: COLS must be between 1 and {MAX_COLS}.")
    sys.exit(1)
if ROWS < 1:
    print("Error: ROWS must be at least 1.")
    sys.exit(1)

PLAYER_TOKENS = TOKENS[:NUM_PLAYERS]
COL_LABELS = list(string.ascii_uppercase[:COLS])

# ==========================
# Utility Functions
# ==========================

def clear_screen():
    """Clear terminal screen (Linux/Unix)."""
    os.system('clear')


def create_board(rows, cols):
    """Create a rows x cols board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board, labels):
    """Print the board in the format specified in the assignment."""
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Column header
    header = "  " + "   ".join(labels)
    print(header)

    # Board rows
    sep = "+" + ("---+" * cols)
    for r in range(rows):
        print(sep)
        row_str = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row_str)
    print(sep)


def is_column_full(board, col):
    """Return True if the top cell in column col is not empty."""
    return board[0][col] != " "


def place_checker(board, col, token):
    """
    Place the token in the lowest available row in column col.
    Returns the (row, col) where the token was placed, or None if column is full.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return (r, col)
    return None


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win_from_cell(board, r, c, token):
    """Check all directions for WIN_LENGTH in a row starting from (r, c)."""
    if board[r][c] != token:
        return False

    rows = len(board)
    cols = len(board[0])

    # Directions: (dr, dc)
    directions = [
        (0, 1),    # horizontal right
        (1, 0),    # vertical down
        (1, 1),    # diagonal down-right
        (1, -1),   # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # current cell counts as 1
        # Extend forward
        rr, cc = r + dr, c + dc
        while in_bounds(rr, cc, rows, cols) and board[rr][cc] == token:
            count += 1
            rr += dr
            cc += dc
        # Extend backward
        rr, cc = r - dr, c - dc
        while in_bounds(rr, cc, rows, cols) and board[rr][cc] == token:
            count += 1
            rr -= dr
            cc -= dc

        if count >= WIN_LENGTH:
            return True

    return False


def check_win(board, token):
    """Check the entire board for a win for the given token."""
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == token and check_win_from_cell(board, r, c, token):
                return True
    return False


def check_draw(board):
    """Return True if the board is full (no spaces left)."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def prompt_for_column(player_token):
    """Prompt the user to input a column. Returns uppercase string input."""
    return input(f"Player {player_token}, please enter a column: ").strip().upper()


def get_valid_input(board, labels, player_token):
    """
    Prompt until the user provides syntactically valid input (a valid column label).
    If the chosen column is full, the move is invalid and the player loses the turn.
    Returns a tuple: (status, col_index)
      - status == 'ok'    -> column valid and not full
      - status == 'full'  -> column valid but full (turn lost)
    """
    valid_labels = set(labels)
    while True:
        user_in = prompt_for_column(player_token)

        # Input validation for a single uppercase letter within available labels
        if len(user_in) != 1 or user_in not in valid_labels:
            # Invalid input, re-prompt (turn not lost)
            print("Invalid input. Please enter a valid column letter shown above.")
            continue

        col_idx = labels.index(user_in)
        if is_column_full(board, col_idx):
            # Valid input but column full -> return 'full' (turn lost)
            return ('full', col_idx)

        # Valid and available
        return ('ok', col_idx)


# ==========================
# Main Game Loop
# ==========================

def main():
    board = create_board(ROWS, COLS)

    # Randomly select starting player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Show initial empty board
    clear_screen()
    print_board(board, COL_LABELS)

    # Gameplay loop
    while True:
        token = PLAYER_TOKENS[current_player_idx]

        status, col_idx = get_valid_input(board, COL_LABELS, token)

        if status == 'full':
            # Column full: turn is invalid and player loses the turn
            clear_screen()
            print_board(board, COL_LABELS)
            print(f"Column {COL_LABELS[col_idx]} is full. Player {token} loses the turn.")
            # Advance to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Place checker
        placed_pos = place_checker(board, col_idx, token)

        # placed_pos should never be None here due to prior check, but guard anyway
        clear_screen()
        print_board(board, COL_LABELS)

        if placed_pos is not None:
            # Check for win
            if check_win(board, token):
                print(f"Player {token} won!")
                break

            # Check for draw
            if check_draw(board):
                print("It's a draw.")
                break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
