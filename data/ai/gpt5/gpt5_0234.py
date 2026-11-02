import os
import random
import sys

# ----------------------------
# Configurable constants
# ----------------------------
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns due to labeling with letters A-Z
NUM_PLAYERS = 2  # Between 2 and 5 inclusive

# Checker symbols in order for up to 5 players
ALL_CHECKERS = ["X", "O", "V", "H", "M"]
CHECKERS = ALL_CHECKERS[:NUM_PLAYERS]

# ----------------------------
# Utility functions
# ----------------------------
def clear_screen():
    """
    Clears the terminal screen.
    Uses 'clear' for Unix/Linux/Mac and 'cls' for Windows.
    """
    try:
        os.system('clear' if os.name != 'nt' else 'cls')
    except Exception:
        # As a fallback, print a few newlines
        print("\n" * 100)


def create_board(rows, cols):
    """
    Creates and returns a board with given rows and cols.
    Each cell is initialized with a single space " " (empty).
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Clears the screen and prints the board with column headers (A..).
    Uses the same visual style as the example (grid with +---+ separators).
    """
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header with column letters
    header_letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(header_letters))

    # Print each row with separators
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)


def column_from_input(user_input, cols):
    """
    Converts user input (expected single uppercase letter) to column index.
    Returns an integer column index if valid, otherwise returns None.
    """
    if not user_input or len(user_input) != 1:
        return None
    ch = user_input.upper()
    if not ('A' <= ch <= 'Z'):
        return None
    idx = ord(ch) - ord('A')
    if 0 <= idx < cols:
        return idx
    return None


def is_column_full(board, col):
    """
    Returns True if the given column is full (no spaces), else False.
    """
    for r in range(len(board)):
        if board[r][col] == " ":
            return False
    return True


def drop_checker(board, col, symbol):
    """
    Drops the checker with 'symbol' into the given column 'col',
    placing it at the lowest available row in that column.
    Assumes the column is not full.
    Returns the (row, col) where the checker was placed.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return (r, col)
    # Should not reach here if caller checks for fullness
    return None


def check_win(board, symbol):
    """
    Checks if the player with 'symbol' has four in a row.
    Considers horizontal, vertical, and both diagonals.
    Returns True if win detected, else False.
    """
    rows = len(board)
    cols = len(board[0])

    # Horizontal (left to right)
    for r in range(rows):
        for c in range(cols - 3):
            if (board[r][c] == symbol and
                board[r][c + 1] == symbol and
                board[r][c + 2] == symbol and
                board[r][c + 3] == symbol):
                return True

    # Vertical (top to bottom)
    for c in range(cols):
        for r in range(rows - 3):
            if (board[r][c] == symbol and
                board[r + 1][c] == symbol and
                board[r + 2][c] == symbol and
                board[r + 3][c] == symbol):
                return True

    # Diagonal down-right
    for r in range(rows - 3):
        for c in range(cols - 3):
            if (board[r][c] == symbol and
                board[r + 1][c + 1] == symbol and
                board[r + 2][c + 2] == symbol and
                board[r + 3][c + 3] == symbol):
                return True

    # Diagonal up-right
    for r in range(3, rows):
        for c in range(cols - 3):
            if (board[r][c] == symbol and
                board[r - 1][c + 1] == symbol and
                board[r - 2][c + 2] == symbol and
                board[r - 3][c + 3] == symbol):
                return True

    return False


def board_full(board):
    """
    Returns True if the board has no empty spaces, else False.
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def validate_configuration():
    """
    Validates the global configuration constants.
    Exits the program with a message if configuration is invalid.
    """
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if not (1 <= NUM_ROWS and 1 <= NUM_COLS <= 26):
        print("Invalid board size. NUM_ROWS must be >= 1; NUM_COLS must be between 1 and 26.")
        sys.exit(1)


def main():
    validate_configuration()

    # Initialize board
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly select the starting player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Initial board print to show layout before the game starts
    print_board(board)

    # Game loop
    while True:
        current_symbol = CHECKERS[current_player_idx]
        # Prompt player for input until a syntactically valid input is given
        while True:
            prompt = f"Player {current_symbol}, please enter a column: "
            user_in = input(prompt).strip().upper()
            col = column_from_input(user_in, NUM_COLS)
            if col is None:
                # Invalid input (not a single valid column letter)
                print_board(board)
                print("Invalid input. Please enter a single letter corresponding to a column (e.g., A, B, C).")
                continue
            # If the column is full, the turn is invalid and player loses the turn
            if is_column_full(board, col):
                print_board(board)
                print(f"Column {chr(ord('A') + col)} is full. Turn lost.")
                # Move to next player
                current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
                break  # Break the input loop to proceed to next player's turn

            # Valid input and column not full: place checker
            drop_checker(board, col, current_symbol)
            print_board(board)

            # Check for win
            if check_win(board, current_symbol):
                print(f"Player {current_symbol} won!")
                return

            # Check for draw
            if board_full(board):
                print("It's a draw!")
                return

            # Next player's turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            break  # End of this player's turn (since a valid move was made)


if __name__ == "__main__":
    main()
