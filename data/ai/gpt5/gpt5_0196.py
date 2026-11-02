import os
import random
import string
import sys

# ----- Configuration (submission requires 6 rows x 7 cols and 2 players) -----
ROWS = 6
COLS = 7   # Maximum is 26 (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

# ----- Validation for configuration -----
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if not (1 <= COLS <= 26):
    print("COLS must be between 1 and 26.")
    sys.exit(1)
if ROWS < 1:
    print("ROWS must be at least 1.")
    sys.exit(1)

PLAYER_SYMBOLS = CHECKERS[:NUM_PLAYERS]
COLUMN_LABELS = list(string.ascii_uppercase[:COLS])

# ----- Board functions -----
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    os.system('clear')

def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows else 0

    # Header
    header = "  " + "   ".join(COLUMN_LABELS[:cols])
    print(header)
    # Top border of first row
    horizontal = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(horizontal)
        # Row content
        row_cells = "|"
        for c in range(cols):
            row_cells += f" {board[r][c]} |"
        print(row_cells)
    # Bottom border
    print(horizontal)

def board_full(board):
    # Full if top row has no spaces
    return all(cell != " " for cell in board[0])

def lowest_empty_row(board, col):
    # Return the row index of the lowest empty slot in given column, or None if column is full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def place_checker(board, col, symbol):
    r = lowest_empty_row(board, col)
    if r is None:
        return None, None
    board[r][col] = symbol
    return r, col

# ----- Input -----
def get_column_input(current_symbol):
    while True:
        user_in = input(f"Player {current_symbol}, please enter a column: ").strip()
        if len(user_in) != 1:
            print("Invalid input. Please enter a single uppercase letter corresponding to a column.")
            continue
        ch = user_in.upper()
        if ch not in COLUMN_LABELS:
            print("Invalid column. Please enter a valid column letter on the board.")
            continue
        return COLUMN_LABELS.index(ch)

# ----- Win checking -----
def count_in_direction(board, start_r, start_c, dr, dc, symbol):
    rows = len(board)
    cols = len(board[0])
    r, c = start_r + dr, start_c + dc
    count = 0
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    return count

def check_win(board, r, c, symbol):
    # Check 4 directions: horizontal, vertical, diag1 (/), diag2 (\)
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        total = 1
        total += count_in_direction(board, r, c, dr, dc, symbol)
        total += count_in_direction(board, r, c, -dr, -dc, symbol)
        if total >= WIN_LENGTH:
            return True
    return False

# ----- Game loop -----
def main():
    board = create_board(ROWS, COLS)
    # Randomly select starting player index
    current_idx = random.randrange(NUM_PLAYERS)

    # Initial display
    clear_screen()
    print_board(board)

    while True:
        # Check for draw at start of turn (board already full)
        if board_full(board):
            print("Game is a draw!")
            break

        current_symbol = PLAYER_SYMBOLS[current_idx]
        # Prompt for input until valid column letter
        col = get_column_input(current_symbol)

        # Attempt to place the checker
        r, c = place_checker(board, col, current_symbol)

        # Clear and reprint board after the attempt (updated or not)
        clear_screen()
        print_board(board)

        if r is None:
            # Column full; turn is lost
            col_label = COLUMN_LABELS[col]
            print(f"Column {col_label} is full. Turn lost.")
            # After a lost turn, check draw condition
            if board_full(board):
                print("Game is a draw!")
                break
        else:
            # Successful placement: check win
            if check_win(board, r, c, current_symbol):
                print(f"Player {current_symbol} won!")
                break

        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
