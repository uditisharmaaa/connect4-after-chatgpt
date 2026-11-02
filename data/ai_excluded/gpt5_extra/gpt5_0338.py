import os
import random
import sys

# -----------------------------
# Configuration constants
# -----------------------------
ROWS = 6               # Number of rows (default: 6)
COLS = 7               # Number of columns (default: 7), max 26
NUM_PLAYERS = 2        # Number of players supported: 2..5
PLAYER_MARKS = ["X", "O", "V", "H", "M"]
WIN_LEN = 4            # Number of consecutive checkers needed to win (fixed at 4)

# Validate configuration at startup
if not (2 <= NUM_PLAYERS <= 5):
    print("Error: NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if not (1 <= COLS <= 26):
    print("Error: COLS must be between 1 and 26.")
    sys.exit(1)

# Active player symbols for this game based on NUM_PLAYERS
ACTIVE_MARKS = PLAYER_MARKS[:NUM_PLAYERS]

# -----------------------------
# Utility functions
# -----------------------------

def clear_screen():
    """Clear the terminal screen on Unix-like systems."""
    os.system('clear')


def create_board(rows, cols):
    """Create a board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    """Return list of column labels 'A', 'B', ... up to number of columns."""
    return [chr(ord('A') + i) for i in range(cols)]


def print_board(board):
    """Print the board in the required Connect 4 format."""
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    labels = column_labels(cols)

    # Header with column letters
    header = "  " + "   ".join(labels)
    sep = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep)
    for r in range(rows):
        line_cells = []
        for c in range(cols):
            line_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(line_cells) + "|")
        print(sep)


def is_valid_input(inp, cols):
    """
    Validate user input:
    - Single alphabetic character
    - Uppercase letter within A.. (A+cols-1)
    """
    if len(inp) != 1:
        return False
    if not inp.isalpha():
        return False
    if not ('A' <= inp <= chr(ord('A') + cols - 1)):
        return False
    return True


def find_drop_row(board, col):
    """
    Given a column index, return the row index where the checker will land,
    or None if the column is full.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def check_winner(board, mark):
    """
    Check if the given mark has a winning sequence of WIN_LEN
    horizontally, vertically, or diagonally.
    """
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    L = WIN_LEN

    # Directions: (dr, dc)
    directions = [
        (0, 1),    # Right
        (1, 0),    # Down
        (1, 1),    # Down-right
        (1, -1),   # Down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != mark:
                continue
            for dr, dc in directions:
                end_r = r + (L - 1) * dr
                end_c = c + (L - 1) * dc
                # Check bounds for the end of the sequence
                if not (0 <= end_r < rows and 0 <= end_c < cols):
                    continue
                # Check all cells along the direction
                win = True
                for k in range(L):
                    rr = r + k * dr
                    cc = c + k * dc
                    if board[rr][cc] != mark:
                        win = False
                        break
                if win:
                    return True
    return False


def board_full(board):
    """Return True if the board has no empty spaces."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


# -----------------------------
# Game loop
# -----------------------------

def main():
    # Initialize board
    board = create_board(ROWS, COLS)

    # Randomly choose starting player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Initial display
    clear_screen()
    print_board(board)

    # Main game loop
    while True:
        current_mark = ACTIVE_MARKS[current_player_idx]
        # Prompt until valid input (does not include "column full" case)
        while True:
            user_inp = input(f"Player {current_mark}, please enter a column: ").strip().upper()
            if is_valid_input(user_inp, COLS):
                break
            else:
                print("Invalid input. Please enter a valid column letter.")

        # Convert input to column index
        col_idx = ord(user_inp) - ord('A')

        # Attempt to drop the checker in the selected column
        row_idx = find_drop_row(board, col_idx)
        if row_idx is None:
            # Column full: turn is lost
            clear_screen()
            print_board(board)
            print(f"Column {user_inp} is full. Turn lost.")
            # Switch to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Place the checker
        board[row_idx][col_idx] = current_mark

        # Clear and print updated board
        clear_screen()
        print_board(board)

        # Check for win
        if check_winner(board, current_mark):
            print(f"Player {current_mark} won!")
            break

        # Check for draw
        if board_full(board):
            print("Game is a draw!")
            break

        # Switch to next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
