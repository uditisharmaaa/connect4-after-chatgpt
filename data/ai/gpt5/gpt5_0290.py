import os
import random
import sys

# ---------------------------
# Configuration (constants)
# ---------------------------

# Board dimensions (rows x columns)
ROWS = 6
COLS = 7  # Max 26 columns supported (A-Z)

# Number of players (between 2 and 5)
NUM_PLAYERS = 2

# Player tokens in order; will use first NUM_PLAYERS tokens
TOKENS = ["X", "O", "V", "H", "M"]

# Win condition (number in a row to win)
WIN_LENGTH = 4

# ---------------------------
# Validation of configuration
# ---------------------------

if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if COLS > 26:
    print("Maximum supported columns is 26 (A-Z).")
    sys.exit(1)

if ROWS < 1 or COLS < 1:
    print("ROWS and COLS must be positive integers.")
    sys.exit(1)

# ---------------------------
# Utility functions
# ---------------------------

def clear_screen():
    """
    Clear the terminal screen. Works on Unix-like systems.
    """
    os.system('clear')


def create_board(rows, cols):
    """
    Create a board initialized with spaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Print the board to the terminal with column headers A.. and
    grid lines matching the assignment's example.
    """
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Column headers (A, B, C, ...)
    headers = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(headers))

    # Horizontal separator line for each row
    sep = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(sep)
        # Row contents
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)


def get_valid_column_input(cols):
    """
    Prompt the user until a valid column letter (A..A+cols-1) is given.
    Returns the zero-based column index.
    Invalid characters (numbers, symbols, out-of-range letters) are rejected.
    """
    min_char = 'A'
    max_char = chr(ord('A') + cols - 1)

    while True:
        user_input = input().strip().upper()

        # Validate exactly one character and in [A..max_char]
        if len(user_input) == 1 and 'A' <= user_input <= max_char:
            return ord(user_input) - ord('A')
        else:
            print(f"Invalid input. Please enter a letter between {min_char} and {max_char}:")


def drop_checker(board, col, token):
    """
    Attempt to drop a checker with 'token' into column 'col'.
    The checker occupies the lowest available space in that column.
    Returns the row index where the checker was placed, or None if the column is full.
    """
    rows = len(board)

    # Start from bottom (last row) upwards to find first empty cell
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r
    return None  # Column full


def check_win(board, token):
    """
    Check if the given token has a winning set of WIN_LENGTH in a row:
    horizontally, vertically, or diagonally.
    """
    rows = len(board)
    cols = len(board[0])

    # Horizontal
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r][c + k] == token for k in range(WIN_LENGTH)):
                return True

    # Vertical
    for c in range(cols):
        for r in range(rows - WIN_LENGTH + 1):
            if all(board[r + k][c] == token for k in range(WIN_LENGTH)):
                return True

    # Diagonal down-right
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r + k][c + k] == token for k in range(WIN_LENGTH)):
                return True

    # Diagonal up-right
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r - k][c + k] == token for k in range(WIN_LENGTH)):
                return True

    return False


def is_draw(board):
    """
    The game is a draw if the board is full (no spaces).
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


# ---------------------------
# Main game logic
# ---------------------------

def main():
    board = create_board(ROWS, COLS)
    players = TOKENS[:NUM_PLAYERS]

    # Randomly select starting player index
    current_idx = random.randint(0, NUM_PLAYERS - 1)

    # Initial display
    clear_screen()
    print_board(board)
    print(f"Player {players[current_idx]}, please enter a column:")

    while True:
        # Get a valid column input (letter within range)
        col_index = get_valid_column_input(COLS)

        # Try to drop the checker
        placed_row = drop_checker(board, col_index, players[current_idx])

        # Clear and print board after the (attempted) move
        clear_screen()
        print_board(board)

        if placed_row is None:
            # Column is full: invalid turn; player loses the turn
            print(f"Column {chr(ord('A') + col_index)} is full. Player {players[current_idx]} loses the turn.")
            # Move to next player
            current_idx = (current_idx + 1) % NUM_PLAYERS
        else:
            # Check for win after a successful move
            if check_win(board, players[current_idx]):
                print(f"Player {players[current_idx]} won!")
                break

            # Check for draw
            if is_draw(board):
                print("The game is a draw.")
                break

            # Next player's turn
            current_idx = (current_idx + 1) % NUM_PLAYERS

        # Prompt next player
        print(f"Player {players[current_idx]}, please enter a column:")


if __name__ == "__main__":
    main()
