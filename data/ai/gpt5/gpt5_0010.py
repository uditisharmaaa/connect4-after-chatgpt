import os
import random
import string
import sys

# ---------------------------
# Configuration (submission requires these defaults)
# ---------------------------
ROWS = 6                 # number of rows (height)
COLS = 7                 # number of columns (width) - must be <= 26
NUM_PLAYERS = 2          # number of players (2 to 5 supported)
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4
MAX_COLUMNS = 26

# Clamp/validate configuration
COLS = max(1, min(COLS, MAX_COLUMNS))
NUM_PLAYERS = max(2, min(NUM_PLAYERS, len(CHECKERS)))
PLAYER_SYMBOLS = CHECKERS[:NUM_PLAYERS]


# ---------------------------
# Utility functions
# ---------------------------
def clear_screen():
    """
    Clear the terminal screen (Unix/Linux).
    """
    os.system('clear')


def create_board(rows, cols):
    """
    Create a 2D board initialized with spaces.
    Returns a list of lists with dimensions rows x cols.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Print the board with column headers (A..), borders, and cells.
    """
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Column labels
    labels = list(string.ascii_uppercase[:cols])
    header = "  " + "   ".join(labels)
    sep_line = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep_line)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print(sep_line)


def is_valid_column_input(inp, cols):
    """
    Validate the user's input:
    - Must be a single alphabetic character.
    - Must be uppercase letter within A..(A+cols-1).
    Returns (True, col_index) if valid, else (False, None).
    """
    if not isinstance(inp, str):
        return False, None
    s = inp.strip()
    if len(s) != 1:
        return False, None
    if not s.isalpha():
        return False, None
    s = s.upper()
    # Map letter to index
    labels = list(string.ascii_uppercase[:cols])
    if s in labels:
        return True, labels.index(s)
    return False, None


def drop_checker(board, col_idx, symbol):
    """
    Attempt to drop 'symbol' into column 'col_idx'.
    The checker should occupy the lowest available space in that column.
    Returns the row index where it was placed, or -1 if the column is full.
    """
    rows = len(board)
    # Start from bottom row to top
    for r in range(rows - 1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = symbol
            return r
    return -1  # column full


def within_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win(board, symbol):
    """
    Check whether 'symbol' has a connect of WIN_LENGTH on the board
    horizontally, vertically, or diagonally (both directions).
    """
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    L = WIN_LENGTH

    # Directions: (dr, dc)
    directions = [
        (0, 1),    # horizontal right
        (1, 0),    # vertical down
        (1, 1),    # diagonal down-right
        (1, -1),   # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while count < L and within_bounds(rr, cc, rows, cols) and board[rr][cc] == symbol:
                    count += 1
                    rr += dr
                    cc += dc
                if count >= L:
                    return True
    return False


def is_draw(board):
    """
    A draw occurs when the board is full and no more moves can be made.
    """
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    for c in range(cols):
        if board[0][c] == " ":
            return False
    return True


# ---------------------------
# Game loop
# ---------------------------
def main():
    # Initialize
    board = create_board(ROWS, COLS)

    # Random starting player
    current_player_index = random.randrange(NUM_PLAYERS)

    # Initial render
    clear_screen()
    print_board(board)
    # Game loop
    while True:
        current_symbol = PLAYER_SYMBOLS[current_player_index]
        # Prompt
        prompt = f"Player {current_symbol}, please enter a column: "
        user_input = input(prompt)

        # Validate input (accept lowercase but validate to uppercase A..)
        valid, col_idx = is_valid_column_input(user_input, COLS)
        while not valid:
            print("Invalid input. Please enter a valid uppercase column letter (e.g., A, B, C).")
            user_input = input(prompt)
            valid, col_idx = is_valid_column_input(user_input, COLS)

        # Try to place checker
        placed_row = drop_checker(board, col_idx, current_symbol)
        if placed_row == -1:
            # Column full -> lose turn
            clear_screen()
            print_board(board)
            col_letter = string.ascii_uppercase[col_idx]
            print(f"Column {col_letter} is full. You lose your turn.")
            # Check for draw just in case (board could already be full)
            if is_draw(board):
                print("It's a draw!")
                break
            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        # After a successful move, clear and print board
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C
        sys.exit(0)
