import os
import random
import string
import sys

# ====== Configuration (as constants) ======
ROWS = 6            # Number of rows (height)
COLS = 7            # Number of columns (width), max 26 due to letter labels
NUM_PLAYERS = 2     # Between 2 and 5 players
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # In order of assignment requirement

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

PLAYER_SYMBOLS = CHECKERS[:NUM_PLAYERS]
COLUMN_LABELS = list(string.ascii_uppercase[:COLS])


# ====== Board utilities ======
def create_board(rows, cols):
    """Create a board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')


def print_board(board):
    """Print the board in the required ASCII format with column labels."""
    clear_screen()
    # Header with column letters
    header = "  " + "   ".join(COLUMN_LABELS)
    print(header)
    # Separator line
    sep = "+" + "+".join(["---"] * COLS) + "+"
    # Rows (from top to bottom as stored)
    for r in range(ROWS):
        print(sep)
        row_cells = []
        for c in range(COLS):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)


def is_board_full(board):
    """Return True if there are no empty spaces left."""
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True


def get_next_open_row(board, col):
    """
    Given a column index, return the row index where the checker
    should land (the lowest available space). Return None if the column is full.
    """
    # Start from bottom row moving upward to find first empty space
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def drop_piece(board, row, col, piece):
    """Place a piece on the board at row, col."""
    board[row][col] = piece


# ====== Win detection ======
def check_win(board, piece):
    """Check for a win condition (4 in a row) for a given piece."""
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == piece and
                board[r][c + 1] == piece and
                board[r][c + 2] == piece and
                board[r][c + 3] == piece):
                return True

    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - 3):
            if (board[r][c] == piece and
                board[r + 1][c] == piece and
                board[r + 2][c] == piece and
                board[r + 3][c] == piece):
                return True

    # Diagonal (down-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if (board[r][c] == piece and
                board[r + 1][c + 1] == piece and
                board[r + 2][c + 2] == piece and
                board[r + 3][c + 3] == piece):
                return True

    # Diagonal (up-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == piece and
                board[r - 1][c + 1] == piece and
                board[r - 2][c + 2] == piece and
                board[r - 3][c + 3] == piece):
                return True

    return False


# ====== Input handling ======
def prompt_for_column(player_symbol):
    """
    Prompt the current player for a column letter.
    Keep asking until a valid letter within the board range is entered.
    Note: If the chosen valid column is full, this function returns that column
    and the caller will handle the 'turn lost' condition.
    """
    while True:
        user_input = input(f"Player {player_symbol}, please enter a column: ").strip()
        if not user_input:
            print("Invalid input. Please enter a column letter.")
            continue
        # Accept uppercase only per spec, but tolerate lowercase by converting
        letter = user_input.upper()
        if len(letter) != 1 or letter < 'A' or letter > 'Z':
            print("Invalid input. Please enter a single column letter (e.g., A, B, C).")
            continue
        if letter not in COLUMN_LABELS:
            print(f"Invalid column. Please choose between {COLUMN_LABELS[0]} and {COLUMN_LABELS[-1]}.")
            continue
        return COLUMN_LABELS.index(letter)


# ====== Game loop ======
def main():
    board = create_board(ROWS, COLS)

    # Randomly select the starting player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Initial display of the empty board before the game starts
    print_board(board)

    # Main game loop
    while True:
        player_symbol = PLAYER_SYMBOLS[current_player_idx]

        # Prompt for a valid column letter
        col = prompt_for_column(player_symbol)

        # Find row to drop piece; if column full, player loses the turn
        row = get_next_open_row(board, col)
        if row is None:
            # Column is full: invalid turn, player loses the turn
            print(f"Column {COLUMN_LABELS[col]} is full. Player {player_symbol} loses this turn.")
            input("Press Enter to continue...")
            print_board(board)
            # Move to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Place the piece
        drop_piece(board, row, col, player_symbol)

        # Print updated board
        print_board(board)

        # Check for a win
        if check_win(board, player_symbol):
            print(f"Player {player_symbol} won!")
            break

        # Check for a draw
        if is_board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
