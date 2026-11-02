import os
import random
import string
import sys

# ==============================
# Configuration (changeable)
# ==============================
ROWS = 6
COLUMNS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5 inclusive

# Win condition is always 4 in a row per assignment
WIN_LENGTH = 4

# Player symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# ==============================
# Validation of configuration
# ==============================
if not (2 <= NUM_PLAYERS <= 5):
    print("Error: NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if COLUMNS < 1 or COLUMNS > 26:
    print("Error: COLUMNS must be between 1 and 26.")
    sys.exit(1)
if ROWS < 1:
    print("Error: ROWS must be at least 1.")
    sys.exit(1)

# ==============================
# Board utilities
# ==============================
def create_board(rows, cols):
    """Create a rows x cols board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def clear_and_print_board(board):
    """Clear the terminal and print the current board with column headers."""
    os.system('clear')
    rows = len(board)
    cols = len(board[0])

    # Header with letters A.. up to cols
    letters = [chr(ord('A') + i) for i in range(cols)]
    header = "  " + "   ".join(letters)
    print(header)

    # Horizontal line helper
    hline = "+" + "+".join(["---"] * cols) + "+"

    # Print grid, top row first
    for r in range(rows):
        print(hline)
        row_cells = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row_cells)
    print(hline)


def is_board_full(board):
    """Return True if no empty cells remain."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def drop_checker(board, col, symbol):
    """
    Attempt to drop a checker into column 'col'.
    Returns True if placed; False if the column is full.
    """
    rows = len(board)
    # Start from bottom-most row upwards
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return True
    return False


def check_win(board, symbol):
    """Check if 'symbol' has WIN_LENGTH in a row in any direction."""
    rows = len(board)
    cols = len(board[0])
    L = WIN_LENGTH

    # Horizontal
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == symbol:
                count += 1
                if count >= L:
                    return True
            else:
                count = 0

    # Vertical
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == symbol:
                count += 1
                if count >= L:
                    return True
            else:
                count = 0

    # Diagonal down-right
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            # Try extend L-1 steps down-right
            ok = True
            for k in range(1, L):
                rr = r + k
                cc = c + k
                if rr >= rows or cc >= cols or board[rr][cc] != symbol:
                    ok = False
                    break
            if ok:
                return True

    # Diagonal down-left
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            # Try extend L-1 steps down-left
            ok = True
            for k in range(1, L):
                rr = r + k
                cc = c - k
                if rr >= rows or cc < 0 or board[rr][cc] != symbol:
                    ok = False
                    break
            if ok:
                return True

    return False


def get_valid_column_input(cols, current_symbol):
    """
    Prompt until a syntactically valid column letter (within board) is entered.
    Returns zero-based column index.
    Note: If the player inputs syntactically invalid data (numbers, out of range, etc.),
    they are reprompted and do not lose the turn.
    """
    min_letter = 'A'
    max_letter = chr(ord('A') + cols - 1)

    while True:
        user_in = input(f"Player {current_symbol}, please enter a column: ").strip()
        if len(user_in) != 1:
            print("Invalid input. Please enter a single letter corresponding to a column.")
            continue
        ch = user_in.upper()
        if not ('A' <= ch <= max_letter):
            print(f"Invalid column. Please enter a letter between {min_letter} and {max_letter}.")
            continue
        return ord(ch) - ord('A')


# ==============================
# Game loop
# ==============================
def main():
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]

    # Randomly select starting player
    current_index = random.randrange(NUM_PLAYERS)

    # Show initial empty board before the game starts
    clear_and_print_board(board)

    while True:
        current_symbol = players[current_index]

        # Ask for input (validated syntactically)
        col = get_valid_column_input(COLUMNS, current_symbol)

        # Try to place checker; if column is full, turn is lost (no reprompt)
        placed = drop_checker(board, col, current_symbol)

        # Print updated board after the move attempt
        clear_and_print_board(board)

        if not placed:
            # Column full: turn is invalid and lost
            col_letter = chr(ord('A') + col)
            print(f"Column {col_letter} is full. Turn lost.")

            # After a lost turn, check for draw in case the board is already full
            if is_board_full(board):
                print("It's a draw!")
                break

            # Advance to next player
            current_index = (current_index + 1) % NUM_PLAYERS
            continue

        # Successful placement: check for win
        if check_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_index = (current_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
