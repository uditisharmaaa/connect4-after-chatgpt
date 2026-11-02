import os
import random
import string
import sys

# Constants (you may change these for testing, but submit with these values)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

# Player markers in order
PLAYER_MARKERS = ["X", "O", "V", "H", "M"]

# Validate constants
if COLS < 1 or COLS > 26:
    print("Error: COLS must be between 1 and 26.")
    sys.exit(1)
if ROWS < 1:
    print("Error: ROWS must be at least 1.")
    sys.exit(1)
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    print("Error: NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

# Derived values
ACTIVE_MARKERS = PLAYER_MARKERS[:NUM_PLAYERS]
COLUMN_LABELS = [string.ascii_uppercase[i] for i in range(COLS)]


def clear_screen():
    """Clear the terminal screen (Unix/Linux/macOS)."""
    os.system('clear')


def create_board(rows, cols):
    """Create a board with given dimensions, filled with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Print the board in the required ASCII format with column labels."""
    # Header with column labels
    header = "  " + "   ".join(COLUMN_LABELS)
    sep = "+" + "+".join(["---"] * COLS) + "+"
    print(header)
    print(sep)
    for r in range(ROWS):
        row_cells = []
        for c in range(COLS):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print(sep)


def get_valid_column_input(current_marker):
    """
    Prompt the current player for a column letter.
    Only validate that input is a single alphabetic character corresponding to an existing column.
    If invalid, keep asking. This function does not check if the column is full.
    """
    while True:
        user_input = input(f"Player {current_marker}, please enter a column: ").strip().upper()
        if len(user_input) != 1:
            print("Invalid input: please enter a single letter corresponding to a column.")
            continue
        if not user_input.isalpha():
            print("Invalid input: please enter a letter (A-Z).")
            continue
        if user_input not in COLUMN_LABELS:
            print(f"Invalid input: please enter a letter between {COLUMN_LABELS[0]} and {COLUMN_LABELS[-1]}.")
            continue
        return COLUMN_LABELS.index(user_input)


def place_checker(board, col, marker):
    """
    Place the marker in the lowest available row in the given column.
    Returns the row index where the marker was placed, or None if the column is full.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = marker
            return row
    return None


def check_win(board, last_row, last_col, marker):
    """
    Check if placing marker at (last_row, last_col) creates a connect 4.
    We check 4 directions: horizontal, vertical, and two diagonals.
    """

    def count_in_direction(dr, dc):
        """Count consecutive markers starting from last placed, in direction (dr, dc) and opposite."""
        count = 1  # include the last placed piece
        # Forward direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == marker:
            count += 1
            r += dr
            c += dc
        # Backward direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == marker:
            count += 1
            r -= dr
            c -= dc
        return count

    # Directions: horizontal (0,1), vertical (1,0), diag down-right (1,1), diag down-left (1,-1)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        if count_in_direction(dr, dc) >= 4:
            return True
    return False


def check_draw(board):
    """Return True if the board is full (no spaces)."""
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True


def main():
    # Initialize game
    board = create_board(ROWS, COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Initial display
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        current_marker = ACTIVE_MARKERS[current_player_index]

        # Ask for input and attempt to place checker
        col = get_valid_column_input(current_marker)

        placed_row = place_checker(board, col, current_marker)
        if placed_row is None:
            # Column full: invalid turn, player loses turn
            clear_screen()
            print_board(board)
            print(f"Column {COLUMN_LABELS[col]} is full. Player {current_marker} loses the turn.")
            # Advance to next player
            current_player_index = (current_player_index + 1) over  NUM_PLAYERS
            continue

        # After a successful placement, clear screen and reprint board
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, placed_row, col, current_marker):
            print(f"Player {current_marker} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted.")
