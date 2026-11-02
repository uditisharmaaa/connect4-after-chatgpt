import os
import random
import string
import sys

# -------------------------------
# Connect 4 - Python3 Implementation
# -------------------------------

# Global configuration constants
ROWS = 6            # Number of rows (default 6)
COLS = 7            # Number of columns (default 7), max 26
NUM_PLAYERS = 2     # Number of players (2 to 5 supported)

# Player checkers in order; only the first NUM_PLAYERS are used
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Win condition: number of checkers in a row needed to win
WIN_LENGTH = 4


def clear_screen():
    """
    Clear the terminal screen using the 'clear' command as specified.
    """
    # On Windows, 'clear' won't work; assignment specifies Linux/Unix terminal.
    # Still, for portability, try 'cls' if 'clear' fails silently.
    try:
        os.system('clear')
    except Exception:
        os.system('cls')


def make_board(rows, cols):
    """
    Create a board with the given dimensions initialized with spaces.
    Board is represented as a list of lists: board[row][col].
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Print the board in the required ASCII-art format with column headers A..,
    and grid lines. Rows do not have labels.
    """
    rows = len(board)
    cols = len(board[0])

    # Header with column letters
    letters = string.ascii_uppercase[:cols]
    header = "  " + "   ".join(letters)
    border = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(border)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
        print(border)


def col_from_input(inp, cols):
    """
    Convert a user input string to a column index.
    Return an integer column index if valid, otherwise None.
    """
    if not inp or len(inp) != 1:
        return None
    ch = inp.upper()
    letters = string.ascii_uppercase[:cols]
    if ch in letters:
        return letters.index(ch)
    return None


def find_drop_row(board, col):
    """
    Given a column index, find the lowest available row in that column.
    Return the row index if available, otherwise None if the column is full.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def is_full(board):
    """
    Check if the entire board is full (no spaces left).
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def count_in_direction(board, start_r, start_c, dr, dc, symbol):
    """
    Count consecutive symbols starting from (start_r, start_c) moving in direction (dr, dc).
    Includes the starting cell if it matches symbol (assumed).
    """
    rows = len(board)
    cols = len(board[0])
    r, c = start_r + dr, start_c + dc
    count = 0
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    return count


def has_won(board, last_r, last_c, symbol):
    """
    Check if placing 'symbol' at (last_r, last_c) creates a win of WIN_LENGTH.
    We check in 4 directions: horizontal, vertical, and two diagonals.
    """
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (-1, 1),  # diagonal up-right
    ]

    for dr, dc in directions:
        # Count both directions, including the last placed checker
        total = 1  # start with the last placed checker
        total += count_in_direction(board, last_r, last_c, dr, dc, symbol)
        total += count_in_direction(board, last_r, last_c, -dr, -dc, symbol)
        if total >= WIN_LENGTH:
            return True
    return False


def validate_config():
    """
    Validate global configuration and exit with message if invalid.
    """
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if COLS < 1 or COLS > 26:
        print("Error: COLS must be between 1 and 26.")
        sys.exit(1)
    if ROWS < 1:
        print("Error: ROWS must be at least 1.")
        sys.exit(1)
    if WIN_LENGTH < 2:
        print("Error: WIN_LENGTH must be at least 2.")
        sys.exit(1)


def main():
    validate_config()

    rows, cols = ROWS, COLS
    symbols = CHECKERS[:NUM_PLAYERS]

    # Initialize board
    board = make_board(rows, cols)

    # Randomly select starting player index
    current_idx = random.randrange(NUM_PLAYERS)

    # Show initial empty board
    clear_screen()
    print_board(board)
    # Game loop
    while True:
        # If the board is full before a player can move, it's a draw
        if is_full(board):
            print("Game is a draw.")
            break

        current_symbol = symbols[current_idx]
        # Prompt for input, validate, and handle turn
        while True:
            # Prompt
            user_inp = input(f"Player {current_symbol}, please enter a column: ").strip()

            # Validate input (must be a single letter within A..)
            col = col_from_input(user_inp, cols)
            if col is None:
                print("Invalid input. Please enter a valid column letter.")
                continue

            # Determine drop row
            drop_row = find_drop_row(board, col)
            if drop_row is None:
                # Column full: turn is invalid and the player loses the turn
                print("Column is full. You lose your turn.")
                # Advance to next player
                current_idx = (current_idx + 1) % NUM_PLAYERS
                # After losing turn, print current board for next player
                clear_screen()
                print_board(board)
                break

            # Place checker
            board[drop_row][col] = current_symbol

            # After a successful move, clear and print updated board
            clear_screen()
            print_board(board)

            # Check for win
            if has_won(board, drop_row, col, current_symbol):
                print(f"Player {current_symbol} won!")
                return

            # Check for draw (board full after this move)
            if is_full(board):
                print("Game is a draw.")
                return

            # Advance to next player
            current_idx = (current_idx + 1) % NUM_PLAYERS
            break  # end inner input loop and proceed to next turn


if __name__ == "__main__":
    main()
