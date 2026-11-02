import os
import random
import string
import sys

# Constants (submission must use 6 rows x 7 columns and 2 players)
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2  # Supported: 2 to 5

# Players' checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]

# Validate constants
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    print("Error: NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if COLUMNS < 1 or COLUMNS > 26:
    print("Error: COLUMNS must be between 1 and 26.")
    sys.exit(1)
if ROWS < 1:
    print("Error: ROWS must be at least 1.")
    sys.exit(1)


def clear_screen():
    # Clear the screen for Unix/Linux/macOS terminals
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0])

    # Header letters
    letters = list(string.ascii_uppercase[:cols])
    header = "  " + "   ".join(letters)
    print(header)

    # Top border
    print("+" + "---+" * cols)

    # Board cells
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
        print("+" + "---+" * cols)


def get_valid_input(cols):
    letters = set(string.ascii_uppercase[:cols])
    while True:
        user_in = input("Please enter a column: ").strip().upper()
        # Validate: must be a single letter within range
        if len(user_in) != 1 or user_in not in letters:
            print("Invalid input. Enter a single letter for a valid column (e.g., A, B, ...).")
            continue
        return ord(user_in) - ord('A')


def drop_checker(board, col, checker):
    """
    Attempt to drop checker in the specified column.
    Returns (placed: bool, row_index: int or None).
    placed == False means the column is full (turn is lost).
    """
    rows = len(board)
    # Start from bottom row
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True, r
    return False, None


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win_from_cell(board, start_r, start_c, dr, dc, checker):
    """
    Count consecutive checkers starting at (start_r, start_c) stepping (dr, dc).
    Return True if sequence of 4 is found including start cell.
    """
    rows = len(board)
    cols = len(board[0])
    count = 0
    r, c = start_r, start_c
    while in_bounds(r, c, rows, cols) and board[r][c] == checker:
        count += 1
        if count == 4:
            return True
        r += dr
        c += dc
    return False


def check_win(board, last_r, last_c, checker):
    """
    Check if placing 'checker' at (last_r, last_c) resulted in a win.
    We check in 4 directions: horizontal, vertical, and two diagonals.
    """
    rows = len(board)
    cols = len(board[0])

    # Directions: horizontal (0,±1), vertical (±1,0), diag1 (±1,±1), diag2 (±1,∓1)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for dr, dc in directions:
        # To count a full line of 4, expand both directions from the last placed cell
        count = 1  # include the last placed cell

        # Forward direction
        r, c = last_r + dr, last_c + dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Backward direction
        r, c = last_r - dr, last_c - dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True

    return False


def is_draw(board):
    # Draw if no spaces left in top row (or anywhere)
    for row in board:
        if " " in row:
            return False
    return True


def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select first player
    current_player_index = random.randrange(NUM_PLAYERS)

    # Initial board print
    print_board(board)
    print(f"Player {players[current_player_index]}, you start.")
    # Also show prompt after board is shown initially as example
    # But we'll move into the loop

    while True:
        checker = players[current_player_index]
        print(f"Player {checker}, please enter a column:")
        col = get_valid_input(COLUMNS)

        placed, row_idx = drop_checker(board, col, checker)
        if not placed:
            # Column full: turn is invalid and player loses the turn
            print("Column is full. Turn lost.")
            # Print board again to reflect no change but UI consistency
            print_board(board)
            # Next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        # Successful placement: print updated board
        print_board(board)

        # Check for win
        if check_win(board, row_idx, col, checker):
            print(f"Player {checker} won!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted.")
