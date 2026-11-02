import os
import random
import string
import sys

# ------------------------------
# Configuration (submission must be 6x7 and 2 players)
# You can change these constants (max 26 columns, 2 to 5 players) to test,
# but submit with ROWS=6, COLS=7, NUM_PLAYERS=2.
# ------------------------------
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# ------------------------------
# Constants and validations
# ------------------------------
MAX_COLS = 26
CHECKER_ORDER = ['X', 'O', 'V', 'H', 'M']
EMPTY = ' '

if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if not (1 <= ROWS and 1 <= COLS <= MAX_COLS):
    print(f"Board must have at least 1 row and 1 column, with columns ≤ {MAX_COLS}.")
    sys.exit(1)

PLAYERS = CHECKER_ORDER[:NUM_PLAYERS]
COL_LABELS = list(string.ascii_uppercase[:COLS])

# ------------------------------
# Board utilities
# ------------------------------
def create_board(rows, cols):
    """Create a board initialized with spaces."""
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    """Clear the terminal screen (Unix/Linux)."""
    os.system('clear')

def print_board(board):
    """Clear screen and print the board with column labels and grid."""
    clear_screen()
    # Header with column letters
    header = "  " + "   ".join(COL_LABELS)
    print(header)
    # Top border
    border = "+" + "+".join(["---"] * COLS) + "+"
    # Rows (top to bottom)
    for r in range(ROWS):
        print(border)
        row_cells = []
        for c in range(COLS):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    # Bottom border
    print(border)

def is_full(board):
    """Return True if the board has no empty cells."""
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == EMPTY:
                return False
    return True

def find_available_row(board, col):
    """Return the lowest available row index in the given column or None if full."""
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            return r
    return None

def drop_checker(board, row, col, symbol):
    """Place the symbol at the specified row and column."""
    board[row][col] = symbol

# ------------------------------
# Input handling
# ------------------------------
def get_valid_column_input():
    """
    Prompt the user for a column input.
    Repeat until user provides a valid column label (A.. up to current COLS).
    Returns the integer column index.
    """
    valid_labels = set(COL_LABELS)
    while True:
        user_in = input("Please enter a column: ").strip()
        if len(user_in) != 1:
            print("Invalid input. Enter a single uppercase letter for the column.")
            continue
        ch = user_in.upper()
        if ch not in valid_labels:
            print(f"Invalid column. Enter a letter between A and {COL_LABELS[-1]}.")
            continue
        return COL_LABELS.index(ch)

# ------------------------------
# Win checking
# ------------------------------
def check_winner(board, symbol):
    """Check for 4 in a row with the given symbol in any direction."""
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == symbol and
                board[r][c + 1] == symbol and
                board[r][c + 2] == symbol and
                board[r][c + 3] == symbol):
                return True
    # Vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if (board[r][c] == symbol and
                board[r + 1][c] == symbol and
                board[r + 2][c] == symbol and
                board[r + 3][c] == symbol):
                return True
    # Diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if (board[r][c] == symbol and
                board[r + 1][c + 1] == symbol and
                board[r + 2][c + 2] == symbol and
                board[r + 3][c + 3] == symbol):
                return True
    # Diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == symbol and
                board[r - 1][c + 1] == symbol and
                board[r - 2][c + 2] == symbol and
                board[r - 3][c + 3] == symbol):
                return True
    return False

# ------------------------------
# Game loop
# ------------------------------
def run_game():
    board = create_board(ROWS, COLS)
    current_player_idx = random.randrange(NUM_PLAYERS)
    winner = None

    # Initial print before the game starts
    print_board(board)

    while True:
        symbol = PLAYERS[current_player_idx]
        # Print board and prompt
        print_board(board)
        print(f"Player {symbol}, please enter a column:")
        col = get_valid_column_input()

        # Try to place the checker
        row = find_available_row(board, col)
        if row is None:
            # Column full: turn is invalid and player loses the turn
            print_board(board)
            print(f"Column {COL_LABELS[col]} is full. Player {symbol} loses the turn.")
            input("Press Enter to continue...")
        else:
            drop_checker(board, row, col, symbol)
            # After placing, print updated board
            print_board(board)
            # Check for a win
            if check_winner(board, symbol):
                winner = symbol
                break
            # Check for a draw (board full and no winner)
            if is_full(board):
                break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

    # Final state and outcome
    if winner is not None:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    run_game()
