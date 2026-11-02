import os
import random
import sys

# ====== Configuration Constants ======
ROWS = 6               # Number of rows (default 6 for submission)
COLS = 7               # Number of columns (default 7 for submission, max 26)
NUM_PLAYERS = 2        # Number of players (2 to 5 inclusive)
WIN_LENGTH = 4         # Number of checkers in a row needed to win
CHECKER_ORDER = ["X", "O", "V", "H", "M"]  # Order of player checkers

# ====== Validation of Constants ======
if not (2 <= NUM_PLAYERS <= 5):
    print("Error: NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if not (1 <= COLS <= 26):
    print("Error: COLS must be between 1 and 26.")
    sys.exit(1)

PLAYERS = CHECKER_ORDER[:NUM_PLAYERS]


# ====== Utility Functions ======
def clear_screen():
    # As per assignment, use 'clear' for Linux/Unix terminals
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Column headers (A, B, C, ...)
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(header)

    # Horizontal separator line
    sep = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(sep)
        row_cells = "|".join(f" {board[r][c]} " for c in range(cols))
        print(f"|{row_cells}|")
    print(sep)


def column_from_input(user_input, cols):
    """
    Convert an input letter to a column index, or return None if invalid.
    Accepts only single letters within A.. up to number of columns.
    """
    if not user_input:
        return None
    s = user_input.strip().upper()
    if len(s) != 1 or not s.isalpha():
        return None
    idx = ord(s) - ord('A')
    if 0 <= idx < cols:
        return idx
    return None


def get_valid_column_input(current_checker, cols):
    """
    Prompt user until a syntactically valid column letter (within bounds) is entered.
    Does not check if the column is full; that is handled separately.
    """
    while True:
        try:
            user_input = input(f"Player {current_checker}, please enter a column: ")
        except EOFError:
            # Graceful exit if input stream closes
            print("\nInput closed. Exiting game.")
            sys.exit(0)

        col = column_from_input(user_input, cols)
        if col is not None:
            return col
        else:
            print("Invalid input. Please enter a valid column letter (e.g., A, B, C).")


def place_checker(board, col, checker):
    """
    Attempt to place 'checker' in the given 'col'.
    Returns the row index where it was placed, or None if the column is full.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return None


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win_from_cell(board, row, col, checker):
    """
    Check if placing 'checker' at (row, col) results in a win.
    We check four directions: horizontal, vertical, diagonal down-right, diagonal down-left.
    """
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1  # Count includes the current checker

        # Check in the positive direction (dr, dc)
        r, c = row + dr, col + dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check in the negative direction (-dr, -dc)
        r, c = row - dr, col - dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_LENGTH:
            return True

    return False


def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


# ====== Main Game Loop ======
def main():
    board = create_board(ROWS, COLS)
    current_index = random.randint(0, NUM_PLAYERS - 1)

    # Initial display
    clear_screen()
    print_board(board)
    print(f"Player {PLAYERS[current_index]} starts.\n")

    while True:
        current_checker = PLAYERS[current_index]

        # Prompt for column input (validated for being a letter within bounds)
        col = get_valid_column_input(current_checker, COLS)

        # Try to place checker
        placed_row = place_checker(board, col, current_checker)

        # Clear and print board after the attempt (updated or not)
        clear_screen()
        print_board(board)

        if placed_row is None:
            # Column was full: turn is lost
            col_letter = chr(ord('A') + col)
            print(f"Column {col_letter} is full. Player {current_checker} loses the turn.\n")
            # No win/draw check since no move happened
        else:
            # Check for win
            if check_win_from_cell(board, placed_row, col, current_checker):
                print(f"Player {current_checker} won!")
                break

            # Check for draw
            if board_full(board):
                print("It's a draw!")
                break

        # Advance to next player
        current_index = (current_index + 1) % NUM_PLAYERS

    # Game ended
    # No extra input or output to keep behavior clean for automated testing


if __name__ == "__main__":
    main()
