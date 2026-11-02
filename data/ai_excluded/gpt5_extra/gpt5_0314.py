import os
import random
import string
import sys

# =========================
# Configuration (Constants)
# =========================
ROWS = 6                    # Number of rows (default 6)
COLS = 7                    # Number of columns (default 7, max 26)
NUM_PLAYERS = 2             # Number of players (between 2 and 5)
WIN_LENGTH = 4              # Number of checkers needed in a row to win (fixed to 4 by spec)

# Checker symbols in order for up to 5 players
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# =========================
# Validation of configuration
# =========================
if not (2 <= NUM_PLAYERS <= 5):
    print("Error: NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if COLS < 1 or COLS > 26:
    print("Error: COLS must be between 1 and 26.")
    sys.exit(1)

if ROWS < 1:
    print("Error: ROWS must be at least 1.")
    sys.exit(1)

# Select the symbols for the enabled number of players
ACTIVE_SYMBOLS = PLAYER_SYMBOLS[:NUM_PLAYERS]


# =========================
# Board Functions
# =========================
def create_board(rows, cols):
    """
    Create a 2D game board initialized with spaces (" ").
    Board is represented as a list of lists [rows][cols].
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def clear_screen():
    """
    Clear the terminal screen (Linux/Unix).
    """
    os.system('clear')


def print_board(board):
    """
    Clear the screen and print the board in the required format.
    Columns are labeled A.. and rows are unlabeled.
    """
    clear_screen()

    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header with column letters
    col_labels = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(col_labels))

    # Horizontal separator line for the top of the board and between rows
    sep = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(sep)
        # Print each cell in the row
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
    print(sep)


def is_full(board):
    """
    Check whether the board is full (no spaces in the top row).
    """
    return all(cell != " " for cell in board[0])


def column_full(board, col):
    """
    Check whether a given column is full.
    """
    return board[0][col] != " "


def drop_checker(board, col, symbol):
    """
    Drop a checker with 'symbol' into column 'col'.
    The checker occupies the lowest available space.
    Returns the (row, col) where the checker was placed, or None if the column is full.
    """
    rows = len(board)
    if column_full(board, col):
        return None
    # Start from bottom row and find the first empty space
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return (r, col)
    return None  # Should not reach here due to earlier check


# =========================
# Win Checking Functions
# =========================
def count_in_direction(board, start_r, start_c, dr, dc, symbol):
    """
    Count consecutive checkers matching 'symbol' starting from (start_r, start_c)
    moving in direction (dr, dc), not including the starting cell.
    Stops when out of bounds or mismatch encountered.
    """
    rows = len(board)
    cols = len(board[0])
    r, c = start_r + dr, start_c + dc
    count = 0
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    return count


def check_win_from_cell(board, r, c, symbol):
    """
    Check if placing 'symbol' at (r, c) creates a connect of WIN_LENGTH
    in any of the four primary directions.
    """
    directions = [
        (0, 1),   # horizontal (right)
        (1, 0),   # vertical (down)
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for dr, dc in directions:
        # Count both forward and backward directions from the placed cell
        total = 1  # include the starting cell
        total += count_in_direction(board, r, c, dr, dc, symbol)
        total += count_in_direction(board, r, c, -dr, -dc, symbol)
        if total >= WIN_LENGTH:
            return True
    return False


# =========================
# Input Handling
# =========================
def get_column_input(prompt, cols):
    """
    Prompt the user repeatedly for a column letter.
    Validate input: single letter within A..(A+cols-1).
    Returns the corresponding column index (0-based).
    """
    valid_letters = [string.ascii_uppercase[i] for i in range(cols)]
    valid_set = set(valid_letters)

    while True:
        try:
            user_input = input(prompt).strip().upper()
        except EOFError:
            print("\nInput closed. Exiting game.")
            sys.exit(0)

        # Validate: must be a single letter in range
        if len(user_input) == 1 and user_input in valid_set:
            return valid_letters.index(user_input)

        # If invalid input, ask again (turn is not lost)
        print(f"Invalid input. Please enter one of: {', '.join(valid_letters)}")


# =========================
# Game Loop
# =========================
def main():
    board = create_board(ROWS, COLS)

    # Randomly select the first player
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial board print to show layout
    print_board(board)

    # Main game loop
    while True:
        current_symbol = ACTIVE_SYMBOLS[current_player_idx]

        # Prompt current player for a column letter
        print(f"Player {current_symbol}, please enter a column:")
        col = get_column_input("> ", COLS)

        # If selected column is full, the turn is invalid and the player loses the turn
        if column_full(board, col):
            print(f"Column {string.ascii_uppercase[col]} is full. You lose your turn.")
            # Move to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            # Show board again after message
            print_board(board)
            continue

        # Place the checker
        placed = drop_checker(board, col, current_symbol)
        # Reprint the board after the move
        print_board(board)

        # Safety check (should not be None due to earlier full check)
        if placed is None:
            # Treat as losing a turn just in case
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        r, c = placed

        # Check for win
        if check_win_from_cell(board, r, c, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check for draw (board full and no winner)
        if is_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
