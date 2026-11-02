import os
import random
import sys

# =========================
# Configuration (submission requires these defaults)
# =========================
ROWS = 6
COLS = 7  # Max 26 (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5

# Checker symbols in player order (use as many as NUM_PLAYERS)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# =========================
# Utility and Game Logic
# =========================

def clear_screen():
    # Clear terminal screen (Unix/Linux)
    os.system('clear')


def create_board(rows, cols):
    """Create a 2D board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def get_column_labels(cols):
    """Return list of column labels: ['A', 'B', ...]."""
    if cols < 1:
        return []
    if cols > 26:
        raise ValueError("Maximum supported columns is 26.")
    return [chr(ord('A') + i) for i in range(cols)]


def print_board(board):
    """Clear screen and print the board in the required format."""
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    labels = get_column_labels(cols)

    # Header
    header = "  " + "   ".join(labels)
    print(header)

    # Horizontal separator line
    sep = "+" + "+".join(["---"] * cols) + "+"

    # Rows (from top row to bottom row)
    for r in range(rows):
        print(sep)
        row_cells = "|" + "|".join([f" {board[r][c]} " for c in range(cols)]) + "|"
        print(row_cells)
    print(sep)


def get_valid_column_index(cols):
    """Prompt until a valid column letter is entered. Returns 0-based column index."""
    labels = get_column_labels(cols)
    valid_set = set(labels)
    while True:
        user_input = input("Please enter a column (A-{}): ".format(labels[-1])).strip().upper()
        if len(user_input) != 1:
            print("Invalid input. Enter a single letter between A and {}.".format(labels[-1]))
            continue
        if user_input not in valid_set:
            print("Invalid column. Choose a letter between A and {}.".format(labels[-1]))
            continue
        return ord(user_input) - ord('A')


def place_checker(board, col, token):
    """
    Attempt to place 'token' into column 'col'.
    Returns the row index where the token was placed, or None if the column is full.
    """
    rows = len(board)
    # Start from bottom-most row and go up to find first empty space
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r
    return None  # Column full


def check_direction(board, start_r, start_c, dr, dc, token):
    """Check 4 in a row starting at start_r, start_c moving by dr, dc."""
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    r, c = start_r, start_c
    for _ in range(4):
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if board[r][c] != token:
            return False
        r += dr
        c += dc
    return True


def check_win(board, last_r, last_c):
    """
    Check if placing a checker at (last_r, last_c) creates a win.
    Only needs to check from the last move for efficiency.
    """
    token = board[last_r][last_c]
    if token == " ":
        return False

    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    # For each direction, we want to check sequences of 4 that include (last_r, last_c)
    # Slide a window of length 4 that could include the last move.
    for dr, dc in directions:
        for offset in range(-3, 1):
            start_r = last_r + offset * dr
            start_c = last_c + offset * dc
            if check_direction(board, start_r, start_c, dr, dc, token):
                return True
    return False


def check_draw(board):
    """A draw occurs if there are no empty spaces left on the board."""
    for row in board:
        if " " in row:
            return False
    return True


def next_player_index(current, total):
    """Return the next player's index in round-robin fashion."""
    return (current + 1) % total


def main():
    # Validate configuration
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if COLS < 1 or COLS > 26:
        print("COLS must be between 1 and 26.")
        sys.exit(1)
    if ROWS < 1:
        print("ROWS must be at least 1.")
        sys.exit(1)

    # Initialize game
    board = create_board(ROWS, COLS)
    checkers = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player = random.randint(0, NUM_PLAYERS - 1)

    # Initial display
    print_board(board)
    print(f"Players: {' '.join(checkers)}")
    print(f"Randomly selected first player: Player {checkers[current_player]}")

    # Game loop
    while True:
        print_board(board)
        current_checker = checkers[current_player]
        print(f"Player {current_checker}, please enter a column:")
        col_index = get_valid_column_index(COLS)

        placed_row = place_checker(board, col_index, current_checker)

        if placed_row is None:
            # Column full: lose the turn
            print_board(board)
            print(f"Column {chr(ord('A') + col_index)} is full. Player {current_checker} loses the turn.")
            # Move to next player
            current_player = next_player_index(current_player, NUM_PLAYERS)
            continue

        # After a successful placement, show the updated board
        print_board(board)

        # Check for win
        if check_win(board, placed_row, col_index):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player = next_player_index(current_player, NUM_PLAYERS)


if __name__ == "__main__":
    main()
