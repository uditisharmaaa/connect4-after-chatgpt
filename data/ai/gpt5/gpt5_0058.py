import os
import random
import sys

# =========================
# Configuration (constants)
# =========================
# Board dimensions (ROWS x COLS)
ROWS = 6
COLS = 7  # Maximum allowed is 26 (A..Z)

# Number of players (between 2 and 5)
NUM_PLAYERS = 2

# Player checker symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# Number of checkers in a row needed to win
CONNECT_N = 4

# =========================
# Input validation of constants
# =========================
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if not (1 <= COLS <= 26):
    print("COLS must be between 1 and 26.")
    sys.exit(1)

if ROWS < 1:
    print("ROWS must be at least 1.")
    sys.exit(1)

# Select only as many symbols as needed by the number of players
PLAYERS = PLAYER_SYMBOLS[:NUM_PLAYERS]


# =========================
# Board Utilities
# =========================
def create_board(rows, cols):
    """Create a 2D board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def clear_screen():
    """Clear the terminal (Linux/Unix)."""
    os.system('clear')


def print_board(board):
    """Print the board with column labels as specified."""
    clear_screen()
    rows = len(board)
    cols = len(board[0])

    # Header with letters
    letters = [chr(ord('A') + c) for c in range(cols)]
    header = "  " + "   ".join(letters)
    print(header)

    # Separator and rows
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(sep)
        row_cells = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row_cells)
    print(sep)


def board_full(board):
    """Return True if the board has no empty spaces."""
    for row in board:
        if " " in row:
            return False
    return True


# =========================
# Move Handling
# =========================
def column_letter_to_index(letter):
    """Convert a column letter (A..Z) to a zero-based column index."""
    if not letter or len(letter) != 1:
        return None
    if not letter.isalpha():
        return None
    letter = letter.upper()
    idx = ord(letter) - ord('A')
    return idx


def get_valid_column_input(cols):
    """
    Prompt the user until they enter a syntactically valid column letter
    within the board (A.. corresponding to number of columns).
    This does not check whether the column is full.
    """
    while True:
        try:
            user_in = input().strip()
        except EOFError:
            # Graceful exit on EOF
            print("\nInput closed. Exiting game.")
            sys.exit(0)

        if len(user_in) == 0:
            print("Invalid input. Please enter a column letter:")
            continue

        idx = column_letter_to_index(user_in[0])
        if idx is None:
            print("Invalid input. Please enter a letter (A-Z):")
            continue

        if not (0 <= idx < cols):
            print("Invalid column. Please choose a valid column within the board:")
            continue

        return idx


def find_available_row(board, col):
    """Return the lowest available row index in the given column, or None if full."""
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def drop_checker(board, col, symbol):
    """
    Attempt to drop a checker with 'symbol' into column 'col'.
    Returns True if placed, False if the column is full.
    """
    row = find_available_row(board, col)
    if row is None:
        return False
    board[row][col] = symbol
    return True


# =========================
# Win Checking
# =========================
def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win(board, symbol):
    """
    Check if the given symbol has CONNECT_N in a row anywhere on the board.
    Directions checked: horizontal (right), vertical (down),
    diagonal down-right, diagonal up-right.
    """
    rows = len(board)
    cols = len(board[0])

    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (-1, 1),  # diagonal up-right
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while count < CONNECT_N and in_bounds(rr, cc, rows, cols) and board[rr][cc] == symbol:
                    count += 1
                    rr += dr
                    cc += dc
                if count == CONNECT_N:
                    return True
    return False


# =========================
# Game Loop
# =========================
def main():
    board = create_board(ROWS, COLS)

    # Randomly select starting player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Show initial board
    print_board(board)

    while True:
        # Draw check before asking for move (in case of custom sizes and unusual flows)
        if board_full(board):
            print("It's a draw!")
            break

        current_symbol = PLAYERS[current_player_idx]
        print(f"Player {current_symbol}, please enter a column:")

        # Read and validate input for valid column letter/within range
        col = get_valid_column_input(COLS)

        # Attempt to drop; if full, lose the turn
        placed = drop_checker(board, col, current_symbol)
        if not placed:
            # Print current board again to reflect no change and inform about lost turn
            print_board(board)
            print(f"Column {chr(ord('A') + col)} is full. Player {current_symbol} loses the turn.")
            # Advance to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Print updated board
        print_board(board)

        # Check for win
        if check_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check for draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
