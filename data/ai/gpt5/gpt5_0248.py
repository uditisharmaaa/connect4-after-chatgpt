import os
import random
import string
import sys

# ------------------ Constants (adjustable, but submission requires 6x7 and 2 players) ------------------
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5 inclusive

CHECKERS = ["X", "O", "V", "H", "M"]

# ------------------ Helpers ------------------

def clear_screen():
    # As per assignment requirement
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def column_labels(n):
    # Up to 26 columns labeled A..Z
    return list(string.ascii_uppercase[:n])

def print_board(board):
    rows = len(board)
    cols = len(board[0])
    labels = column_labels(cols)

    # Header
    header = "  " + "   ".join(labels)
    sep = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep)
    # Print from top row to bottom row
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print(sep)

def letter_to_col(letter):
    letter = letter.upper()
    if letter and letter in string.ascii_uppercase:
        idx = ord(letter) - ord('A')
        return idx
    return None

def is_board_full(board):
    # If any cell is empty, not full
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def drop_checker(board, col, symbol):
    """
    Attempts to place symbol in column col (0-based).
    Returns:
        (row_index, col_index) if placed successfully
        None if the column is full
    """
    rows = len(board)
    # Start from bottom row upwards
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return (r, col)
    return None

def in_bounds(board, r, c):
    return 0 <= r < len(board) and 0 <= c < len(board[0])

def count_direction(board, start_r, start_c, dr, dc, symbol):
    count = 0
    r, c = start_r, start_c
    while in_bounds(board, r, c) and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    return count

def check_win(board, r, c, symbol):
    """
    Check if placing symbol at (r, c) created a 4-in-a-row.
    We count on both sides for each direction and subtract 1 to avoid double-counting the origin.
    """
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right / up-left
        (1, -1),  # diag down-left / up-right
    ]
    for dr, dc in directions:
        total = (
            count_direction(board, r, c, dr, dc, symbol) +
            count_direction(board, r, c, -dr, -dc, symbol) - 1
        )
        if total >= 4:
            return True
    return False

def get_valid_column_input(prompt, valid_cols):
    """
    Repeatedly prompt user for a column letter until valid.
    Returns a 0-based column index.
    Does NOT handle the case of full columns; the caller must handle that.
    """
    labels = column_labels(valid_cols)
    label_set = set(labels)

    while True:
        user_in = input(prompt).strip().upper()
        if len(user_in) != 1 or user_in not in label_set:
            print(f"Invalid input. Please enter one of: {', '.join(labels)}")
            continue
        col_idx = letter_to_col(user_in)
        if col_idx is None or not (0 <= col_idx < valid_cols):
            print(f"Invalid input. Please enter one of: {', '.join(labels)}")
            continue
        return col_idx

def any_moves_left(board):
    # Quick check: if any top cell is empty, moves remain
    # This is faster than scanning entire board for large sizes.
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return True
    return False

# ------------------ Game ------------------

def main():
    # Validate constants
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if not (1 <= COLS <= 26):
        print("COLS must be between 1 and 26.")
        sys.exit(1)
    if ROWS < 1:
        print("ROWS must be at least 1.")
        sys.exit(1)

    # Select players' symbols in order
    players = CHECKERS[:NUM_PLAYERS]

    # Initialize board
    board = create_board(ROWS, COLS)

    # Random starting player
    current_idx = random.randint(0, NUM_PLAYERS - 1)

    # Initial display
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        current_symbol = players[current_idx]
        print(f"Player {current_symbol}, please enter a column:")

        # Get a valid column letter (reprompt on invalid input)
        col = get_valid_column_input("", COLS)

        # Attempt to drop checker (if column full, player loses the turn)
        placement = drop_checker(board, col, current_symbol)
        if placement is None:
            # Column full: turn is lost
            clear_screen()
            print_board(board)
            print(f"Column {column_labels(COLS)[col]} is full. Player {current_symbol} loses the turn.")
            # Switch player
            current_idx = (current_idx + 1) % NUM_PLAYERS
            continue

        # Successful placement, check for win/draw
        r, c = placement
        clear_screen()
        print_board(board)

        if check_win(board, r, c, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        if not any_moves_left(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
