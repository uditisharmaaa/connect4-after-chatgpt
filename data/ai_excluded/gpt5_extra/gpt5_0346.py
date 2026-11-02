import os
import random
import sys

# Connect 4 - Python 3
# Terminal-based game supporting:
# - Adjustable board size (rows, columns) up to 26 columns (A-Z column labels)
# - 2 to 5 players with tokens: X, O, V, H, M
# - Random starting player
# - Turn-based input with validation
# - Placement obeys gravity (lowest available cell in a column)
# - Win detection (4 in a row: horizontal, vertical, diagonals)
# - Draw detection
#
# Submission settings (as required by assignment):
#   - Board dimensions: 6 rows x 7 columns
#   - Players: 2
#
# Usage: Run this file with Python 3 in a Unix/Linux terminal.

# -----------------------------
# Configuration Constants
# -----------------------------
ROWS = 6
COLS = 7  # Max 26 (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5 inclusive
TOKENS = ["X", "O", "V", "H", "M"]  # Order is used to assign to players
WIN_LENGTH = 4  # Always 4 to win, regardless of board size

# Validate configuration
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if COLS > 26:
    print("COLS must be at most 26 (A-Z).")
    sys.exit(1)

PLAYER_TOKENS = TOKENS[:NUM_PLAYERS]


# -----------------------------
# Utility Functions
# -----------------------------
def clear_screen():
    """Clear the terminal screen."""
    # As per instructions, clear using 'clear' (Unix/Linux).
    os.system('clear')


def create_board(rows, cols):
    """Create a board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Clear the screen and print the current board with headers."""
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Column headers (A..)
    header_letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(header_letters))
    print("+" + "---+" * cols)

    # Rows (top to bottom)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + "---+" * cols)


def get_column_index_from_input(cols):
    """
    Prompt the current player to enter a column letter.
    - Accepts any input, strips spaces, converts to uppercase.
    - Returns a valid column index [0..cols-1] after re-prompting for invalid input.
    """
    valid_letters = [chr(ord('A') + i) for i in range(cols)]
    while True:
        user_input = input().strip().upper()
        # Input must be exactly one character and in valid range
        if len(user_input) == 1 and user_input in valid_letters:
            return ord(user_input) - ord('A')
        # Invalid input: re-prompt
        print(f"Invalid input. Please enter a single uppercase letter between A and {valid_letters[-1]}:")


def drop_checker(board, col, token):
    """
    Try to drop 'token' into column 'col'.
    - Returns the row index where the token landed if successful.
    - Returns None if the column is full.
    """
    rows = len(board)
    # Start from bottom-most row, find first empty
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r
    return None


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win(board, token):
    """
    Check if 'token' has a connect WIN_LENGTH in the board.
    Directions: right, down, down-right, down-left.
    """
    rows = len(board)
    cols = len(board[0])

    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (1, 1),   # down-right
        (1, -1),  # down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while count < WIN_LENGTH and in_bounds(nr, nc, rows, cols) and board[nr][nc] == token:
                    count += 1
                    nr += dr
                    nc += dc
                if count == WIN_LENGTH:
                    return True
    return False


def is_board_full(board):
    """Return True if no spaces remain on the board."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


# -----------------------------
# Game Loop
# -----------------------------
def main():
    board = create_board(ROWS, COLS)

    # Randomly select the starting player index
    current_player_index = random.randrange(NUM_PLAYERS)
    current_token = PLAYER_TOKENS[current_player_index]

    # Print initial board and indicate first player
    print_board(board)
    print(f"Player {current_token} will start.")
    input("Press Enter to begin...")

    game_over = False

    while not game_over:
        # Print board at the start of each turn
        print_board(board)
        print(f"Player {current_token}, please enter a column:")

        # Read and validate a column letter
        col_index = get_column_index_from_input(COLS)

        # Attempt to drop checker
        placed_row = drop_checker(board, col_index, current_token)

        if placed_row is None:
            # Column full: per assignment, the turn is invalid and the player loses the turn
            print_board(board)
            letter = chr(ord('A') + col_index)
            print(f"Column {letter} is full. Player {current_token} loses the turn.")
            input("Press Enter to continue...")
        else:
            # Successful placement: check win/draw
            print_board(board)

            if check_win(board, current_token):
                print(f"Player {current_token} won!")
                break

            if is_board_full(board):
                print("It's a draw!")
                break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        current_token = PLAYER_TOKENS[current_player_index]

    # Game over
    # Optionally pause before exit
    # input("Press Enter to exit...")


if __name__ == "__main__":
    main()
