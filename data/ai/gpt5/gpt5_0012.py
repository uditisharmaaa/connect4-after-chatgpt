import os
import random
import string

# =========================
# Configuration (constants)
# =========================
ROWS = 6                 # Number of rows (e.g., 6)
COLS = 7                 # Number of columns (e.g., 7). Max 26 (A-Z).
NUM_PLAYERS = 2          # Supported: 2 to 5 players

TOKENS = ["X", "O", "V", "H", "M"]  # In order, up to 5 players

# =========================
# Validation of constants
# =========================
if not (2 <= NUM_PLAYERS <= 5):
    raise ValueError("NUM_PLAYERS must be between 2 and 5.")
if COLS < 1 or COLS > 26:
    raise ValueError("COLS must be between 1 and 26 (inclusive).")
if ROWS < 1:
    raise ValueError("ROWS must be at least 1.")


# =========================
# Board utilities
# =========================
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def clear_screen():
    # For Linux/Unix systems
    os.system('clear')


def column_labels(cols):
    return [chr(ord('A') + i) for i in range(cols)]


def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0])
    labels = column_labels(cols)

    # Header with column letters
    header = "  " + "   ".join(labels)
    print(header)

    # Top border of the first row
    border = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(border)
        # Print row r (top to bottom)
        row_cells = "|"
        for c in range(cols):
            row_cells += f" {board[r][c]} |"
        print(row_cells)
    # Bottom border
    print(border)


def is_board_full(board):
    # If any top cell (or any cell) is empty, board is not full.
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def drop_checker(board, col, token):
    """
    Attempt to drop 'token' into column index 'col'.
    Returns the row index where the token lands, or None if the column is full.
    """
    rows = len(board)
    # Start from bottom row upwards
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r
    return None


# =========================
# Win checking
# =========================
def count_in_direction(board, start_r, start_c, dr, dc, token):
    """
    Count contiguous tokens equal to 'token' starting from (start_r, start_c),
    moving in the (dr, dc) direction (exclusive of the starting cell).
    """
    rows = len(board)
    cols = len(board[0])
    r, c = start_r + dr, start_c + dc
    count = 0
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == token:
        count += 1
        r += dr
        c += dc
    return count


def check_winner_from_cell(board, r, c, token, needed=4):
    """
    Check if placing 'token' at (r, c) forms a connect-4 (or 'needed') in any direction.
    Directions: horizontal, vertical, diag-down-right, diag-up-right.
    """
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (-1, 1),  # diagonal up-right
    ]
    for dr, dc in directions:
        # Count including both directions from the placed cell
        total = 1
        total += count_in_direction(board, r, c, dr, dc, token)
        total += count_in_direction(board, r, c, -dr, -dc, token)
        if total >= needed:
            return True
    return False


# =========================
# Input handling
# =========================
def prompt_for_column(valid_labels):
    """
    Prompt the user until a valid column label (in valid_labels) is entered.
    Returns the uppercase label.
    """
    while True:
        user_in = input().strip()
        if len(user_in) != 1:
            print("Invalid input. Please enter a single letter corresponding to a column:")
            continue
        ch = user_in.upper()
        if ch not in valid_labels:
            print("Invalid column. Please enter a valid column letter:")
            continue
        return ch


# =========================
# Game loop
# =========================
def play_game():
    board = create_board(ROWS, COLS)
    labels = column_labels(COLS)
    players = TOKENS[:NUM_PLAYERS]

    # Randomly select starting player
    current_index = random.randrange(NUM_PLAYERS)

    # Initial board print
    print_board(board)
    print(f"Player {players[current_index]}, please enter a column:")

    while True:
        # Ask for input until valid label is given (input validation stage)
        col_label = prompt_for_column(labels)
        col_index = ord(col_label) - ord('A')

        # Try to drop checker
        row_index = drop_checker(board, col_index, players[current_index])
        if row_index is None:
            # Column full: turn is invalid and player loses the turn
            print_board(board)  # board unchanged, but reprint as "updated"
            print(f"Column {col_label} is full. Player {players[current_index]} loses the turn.")
            # Next player's turn
            current_index = (current_index + 1) % NUM_PLAYERS
            print(f"Player {players[current_index]}, please enter a column:")
            continue

        # Successful placement: check for win
        if check_winner_from_cell(board, row_index, col_index, players[current_index], needed=4):
            print_board(board)
            print(f"Player {players[current_index]} won!")
            return

        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("It's a draw!")
            return

        # Next turn
        current_index = (current_index + 1) % NUM_PLAYERS
        print_board(board)
        print(f"Player {players[current_index]}, please enter a column:")


if __name__ == "__main__":
    play_game()
