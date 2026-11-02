import os
import random
import string
import sys

# --------------- Configuration (adjustable constants) ---------------
ROWS = 6                 # Number of rows; submission requires 6
COLS = 7                 # Number of columns; submission requires 7 (max 26)
NUM_PLAYERS = 2          # Number of players (2 to 5); submission requires 2
TOKENS = ["X", "O", "V", "H", "M"]  # Player tokens in order
WIN_LENGTH = 4           # Number of checkers in a row needed to win (fixed to 4)
# --------------------------------------------------------------------

def clear_screen():
    # Clear the terminal screen (Linux/Unix)
    os.system('clear')

def create_board(rows, cols):
    # Initialize board with whitespace cells
    return [[" " for _ in range(cols)] for _ in range(rows)]

def get_column_labels(cols):
    # Labels "A", "B", ..., up to number of columns (max 26)
    cols = min(cols, 26)
    return [string.ascii_uppercase[i] for i in range(cols)]

def print_board(board, col_labels):
    # Print the column header
    header = "  " + "   ".join(col_labels)
    print(header)
    # Print horizontal separator and rows with cells
    sep = "+" + "+".join(["---"] * len(col_labels)) + "+"
    for r in range(len(board)):
        print(sep)
        row_cells = "|" + "|".join(f" {cell} " for cell in board[r]) + "|"
        print(row_cells)
    print(sep)

def is_valid_input(user_input, col_labels):
    # Validate that input is a single letter within range
    if not user_input:
        return False
    if len(user_input) != 1:
        return False
    ch = user_input.upper()
    return ch in col_labels

def column_full(board, col_idx):
    # Column is full if top cell in that column is not whitespace
    return board[0][col_idx] != " "

def place_checker(board, col_idx, token):
    # Place the token in the lowest available row in the given column
    # Returns the (row, col) where placed, or None if column is full
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_idx] == " ":
            board[row][col_idx] = token
            return (row, col_idx)
    return None

def check_direction(board, start_row, start_col, d_row, d_col, token, length):
    # Count consecutive tokens starting at (start_row, start_col) along direction
    rows, cols = len(board), len(board[0])
    for i in range(length):
        r = start_row + i * d_row
        c = start_col + i * d_col
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if board[r][c] != token:
            return False
    return True

def check_win(board, token, win_len=WIN_LENGTH):
    rows, cols = len(board), len(board[0])
    directions = [
        (0, 1),    # Horizontal right
        (1, 0),    # Vertical down
        (1, 1),    # Diagonal down-right
        (1, -1),   # Diagonal down-left
    ]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                if check_direction(board, r, c, dr, dc, token, win_len):
                    return True
    return False

def check_draw(board):
    # Draw if no empty spaces exist on the board
    for row in board:
        if " " in row:
            return False
    return True

def main():
    # Enforce constraints
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if COLS < 1 or COLS > 26:
        print("COLS must be between 1 and 26.")
        sys.exit(1)
    if ROWS < 1:
        print("ROWS must be at least 1.")
        sys.exit(1)

    # Initialize game
    board = create_board(ROWS, COLS)
    col_labels = get_column_labels(COLS)
    players = TOKENS[:NUM_PLAYERS]

    # Randomly select first player index
    current_idx = random.randrange(NUM_PLAYERS)

    # Initial display
    clear_screen()
    print_board(board, col_labels)

    # Game loop
    while True:
        current_token = players[current_idx]
        prompt = f"Player {current_token}, please enter a column: "
        # Input loop for validation (not for full column)
        while True:
            user_input = input(prompt).strip()
            if is_valid_input(user_input, col_labels):
                col_char = user_input.upper()
                col_idx = col_labels.index(col_char)
                break
            else:
                # Invalid input: keep asking until valid
                print(f"Invalid input. Please enter a column letter between {col_labels[0]} and {col_labels[-1]}.")
        
        # Attempt to place checker
        if column_full(board, col_idx):
            # Turn is invalid and lost
            clear_screen()
            print_board(board, col_labels)
            print(f"Column {col_labels[col_idx]} is full. Turn lost.")
            # Check draw after the lost turn (board unchanged but still could already be full)
            if check_draw(board):
                print("It's a draw!")
                break
            # Switch to next player
            current_idx = (current_idx + 1) % NUM_PLAYERS
            continue
        else:
            # Place token
            place_checker(board, col_idx, current_token)
            # Print updated board after placement
            clear_screen()
            print_board(board, col_labels)

            # Check for win
            if check_win(board, current_token, WIN_LENGTH):
                print(f"Player {current_token} won!")
                break

            # Check for draw
            if check_draw(board):
                print("It's a draw!")
                break

            # Switch to next player
            current_idx = (current_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted.")
