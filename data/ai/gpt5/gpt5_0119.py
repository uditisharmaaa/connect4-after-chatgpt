import os
import random
import string

# =========================
# Configuration (change if needed)
# =========================
ROWS = 6
COLS = 7  # Max 26 columns
NUM_PLAYERS = 2  # Between 2 and 5

# =========================
# Constants (do not change)
# =========================
MAX_COLS = 26
CHECKERS = ["X", "O", "V", "H", "M"]
EMPTY = " "

# =========================
# Validation of configuration
# =========================
if COLS < 1 or COLS > MAX_COLS:
    raise ValueError(f"COLS must be between 1 and {MAX_COLS}.")
if ROWS < 1:
    raise ValueError("ROWS must be at least 1.")
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    raise ValueError("NUM_PLAYERS must be between 2 and 5.")

# Select the player pieces in order
PLAYER_SYMBOLS = CHECKERS[:NUM_PLAYERS]


# =========================
# Board Utilities
# =========================
def create_board(rows, cols):
    """Create a rows x cols board initialized with spaces."""
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')


def column_labels(cols):
    """Return a list of column labels 'A'.. as many as cols."""
    return list(string.ascii_uppercase[:cols])


def print_board(board):
    """Print the board with column labels and grid lines."""
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    labels = column_labels(cols)

    # Header
    header = "  " + "   ".join(labels)
    sep_line = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep_line)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
        print(sep_line)


def is_valid_column_input(user_input, cols):
    """Check whether user_input is a single letter within column range."""
    if not isinstance(user_input, str):
        return False
    s = user_input.strip()
    if len(s) != 1:
        return False
    ch = s.upper()
    labels = column_labels(cols)
    return ch in labels


def get_column_index_from_input(user_input):
    """Convert a single letter to 0-based column index."""
    return ord(user_input.upper()) - ord('A')


def get_valid_input(prompt, cols):
    """
    Ask the user for input until a valid column letter is provided.
    Returns the 0-based column index.
    """
    while True:
        user_input = input(prompt)
        if is_valid_column_input(user_input, cols):
            return get_column_index_from_input(user_input)
        else:
            print("Invalid input. Please enter a valid column letter (e.g., A, B, C...).")


def find_drop_row(board, col):
    """Return the row index where the checker will land in given column, or None if full."""
    rows = len(board)
    for r in range(rows - 1, -1, -1):  # start from bottom
        if board[r][col] == EMPTY:
            return r
    return None


def drop_checker(board, col, symbol):
    """
    Place the symbol in the lowest available row in the given column.
    Returns the (row, col) where it was placed, or None if the column is full.
    """
    r = find_drop_row(board, col)
    if r is None:
        return None
    board[r][col] = symbol
    return (r, col)


def check_direction(board, row, col, dr, dc, symbol):
    """Count consecutive symbols starting at (row, col) moving by (dr, dc)."""
    rows = len(board)
    cols = len(board[0])
    count = 0
    r, c = row, col
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    return count


def check_win(board, symbol):
    """Check if the given symbol has 4 in a row in any direction."""
    rows = len(board)
    cols = len(board[0])

    # Directions: right, down, diag down-right, diag down-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                # Count both forward and backward to handle complete lines passing through (r,c)
                forward = check_direction(board, r, c, dr, dc, symbol)
                # no need to check backward if forward already >= 4
                if forward >= 4:
                    return True
    return False


def check_draw(board):
    """Return True if the board is full (no EMPTY cells), else False."""
    for row in board:
        if EMPTY in row:
            return False
    return True


def print_state(board, current_symbol=None):
    """Clear screen and print the board, and optionally prompt the current player."""
    clear_screen()
    print_board(board)
    if current_symbol is not None:
        print(f"Player {current_symbol}, please enter a column:")


# =========================
# Game Loop
# =========================
def play_game(rows, cols, player_symbols):
    board = create_board(rows, cols)

    # Randomly select first player index
    current_index = random.randrange(len(player_symbols))

    # Show initial board
    print_state(board, player_symbols[current_index])

    while True:
        current_symbol = player_symbols[current_index]

        # Get a valid column input (letter within range)
        col_index = get_valid_input("", cols)

        # Attempt to drop the checker
        placed = drop_checker(board, col_index, current_symbol)

        if placed is None:
            # Column full: invalid turn; player loses the turn.
            print_state(board)
            print(f"Column {string.ascii_uppercase[col_index]} is full. Player {current_symbol} loses the turn.")
            input("Press Enter to continue...")
            # Move to next player
            current_index = (current_index + 1) % len(player_symbols)
            print_state(board, player_symbols[current_index])
            continue

        # Successfully placed
        r, c = placed

        # Check for win
        if check_win(board, current_symbol):
            print_state(board)
            print(f"Player {current_symbol} won!")
            return

        # Check for draw
        if check_draw(board):
            print_state(board)
            print("It's a draw!")
            return

        # Next player's turn
        current_index = (current_index + 1) % len(player_symbols)
        print_state(board, player_symbols[current_index])


if __name__ == "__main__":
    # Start the game with configured settings
    play_game(ROWS, COLS, PLAYER_SYMBOLS)
