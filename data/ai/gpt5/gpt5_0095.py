import os
import random
import string
import sys

# =======================
# Configuration constants
# =======================
ROWS = 6          # number of rows (height)
COLS = 7          # number of columns (width), max 26
NUM_PLAYERS = 2   # between 2 and 5 inclusive

# Checker symbols in order for players 1..5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# =======================
# Validation of constants
# =======================
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if COLS > 26 or COLS < 1:
    print("COLS must be between 1 and 26.")
    sys.exit(1)
if ROWS < 1:
    print("ROWS must be at least 1.")
    sys.exit(1)

# =======================
# Utility functions
# =======================
def clear_screen():
    # Per assignment, use Unix clear
    os.system('clear')

def create_board(rows, cols):
    # Initialize board with spaces
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Column labels A.. up to cols
    col_labels = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(col_labels)
    # Top border line
    border = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(border)
        # Row content from left to right
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    # Bottom border
    print(border)

def get_column_index_from_input(inp, cols):
    # Expect a single alphabetic character A.. up to column count
    if not inp or len(inp) != 1 or not inp.isalpha():
        return None
    ch = inp.upper()
    index = ord(ch) - ord('A')
    if 0 <= index < cols:
        return index
    return None

def drop_checker(board, col, symbol):
    """
    Attempts to drop 'symbol' into column 'col'.
    Returns (row_index, col_index) if placed, or None if the column is full.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):  # start from bottom
        if board[r][col] == " ":
            board[r][col] = symbol
            return (r, col)
    return None  # column full

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def count_in_direction(board, start_r, start_c, dr, dc, symbol):
    """
    Count contiguous 'symbol' including start cell in both + and - (dr,dc) directions.
    Returns total count.
    """
    rows = len(board)
    cols = len(board[0])

    count = 1  # include starting cell
    # Forward direction
    r, c = start_r + dr, start_c + dc
    while in_bounds(r, c, rows, cols) and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    # Backward direction
    r, c = start_r - dr, start_c - dc
    while in_bounds(r, c, rows, cols) and board[r][c] == symbol:
        count += 1
        r -= dr
        c -= dc
    return count

def check_win(board, last_r, last_c, symbol):
    """
    Check whether placing 'symbol' at (last_r, last_c) wins the game.
    Win if 4 in a row horizontally, vertically, or diagonally.
    """
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        if count_in_direction(board, last_r, last_c, dr, dc, symbol) >= 4:
            return True
    return False

def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

# =======================
# Main game loop
# =======================
def main():
    # Prepare players
    symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]

    # Create and display initial board
    board = create_board(ROWS, COLS)
    # Randomly select starting player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Show initial empty board and whose turn it is
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        current_symbol = symbols[current_player_idx]

        # Prompt for input and validate
        # Keep asking until valid input character within board range
        while True:
            user_input = input(f"Player {current_symbol}, please enter a column: ").strip()
            col_idx = get_column_index_from_input(user_input, COLS)
            if col_idx is None:
                # Invalid input, reprompt
                clear_screen()
                print_board(board)
                print("Invalid input. Please enter a single letter for a column within the board (e.g., A, B, C).")
                continue
            else:
                break

        # Attempt to drop checker
        placement = drop_checker(board, col_idx, current_symbol)
        move_made = placement is not None

        # After action, clear and print updated board
        clear_screen()
        print_board(board)

        if not move_made:
            # Column is full: invalid turn, player loses the turn
            col_label = string.ascii_uppercase[col_idx]
            print(f"Column {col_label} is full. Turn lost.")
            # Next player's turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            # Continue to next iteration
            # Note: no win/draw check since board unchanged
            continue

        # Check for win after a successful move
        last_r, last_c = placement
        if check_win(board, last_r, last_c, current_symbol):
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
