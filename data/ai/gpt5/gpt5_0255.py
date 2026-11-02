import os
import random
import string
import sys

# =========================
# Configuration constants
# =========================
ROWS = 6                 # Number of rows (default: 6)
COLS = 7                 # Number of columns (default: 7), must be <= 26
NUM_PLAYERS = 2          # Number of players (2 to 5)
WIN_LEN = 4              # Number in a row needed to win (fixed to 4)

# Player checker symbols in order
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# =========================
# Validation of constants
# =========================
def validate_settings():
    ok = True
    if COLS < 1 or COLS > 26:
        print("Error: COLS must be between 1 and 26.", file=sys.stderr)
        ok = False
    if ROWS < 1:
        print("Error: ROWS must be at least 1.", file=sys.stderr)
        ok = False
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: NUM_PLAYERS must be between 2 and 5.", file=sys.stderr)
        ok = False
    if WIN_LEN < 2 or WIN_LEN > max(ROWS, COLS):
        print("Error: WIN_LEN must be between 2 and max(ROWS, COLS).", file=sys.stderr)
        ok = False
    if not ok:
        sys.exit(1)

# =========================
# Board utilities
# =========================
def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    # As required by the assignment: clear using 'clear'
    os.system('clear')

def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header letters
    letters = string.ascii_uppercase[:cols]
    header = "  " + "   ".join(letters)
    sep = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
        print(sep)

# =========================
# Game mechanics
# =========================
def column_from_input(user_input, cols):
    """
    Convert input string to a valid column index or return None if invalid.
    Valid inputs are single letters A.. up to the number of columns.
    """
    if not user_input or len(user_input.strip()) != 1:
        return None
    ch = user_input.strip().upper()
    letters = string.ascii_uppercase[:cols]
    if ch not in letters:
        return None
    return letters.index(ch)

def get_valid_column_input(current_checker, cols):
    """
    Prompt the user until a valid column letter is provided.
    Returns the 0-based column index.
    """
    letters = string.ascii_uppercase[:cols]
    while True:
        try:
            user_in = input(f"Player {current_checker}, please enter a column: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting game.")
            sys.exit(0)
        idx = column_from_input(user_in, cols)
        if idx is not None:
            return idx
        else:
            print(f"Invalid input. Please enter one of: {', '.join(letters)}.")

def place_checker(board, col, checker):
    """
    Attempt to place 'checker' in column 'col'.
    Returns (placed, row_index) where:
      - placed is True if the checker was placed, False if the column is full
      - row_index is the row where placed, or None if not placed
    """
    rows = len(board)
    # Start from bottom row up
    for r in range(rows - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = checker
            return True, r
    return False, None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def count_in_direction(board, start_r, start_c, dr, dc, checker):
    """
    Count consecutive checkers including start cell in both positive and negative directions.
    """
    rows = len(board)
    cols = len(board[0])

    total = 1  # count the starting cell

    # Forward direction
    r, c = start_r + dr, start_c + dc
    while in_bounds(r, c, rows, cols) and board[r][c] == checker:
        total += 1
        r += dr
        c += dc

    # Backward direction
    r, c = start_r - dr, start_c - dc
    while in_bounds(r, c, rows, cols) and board[r][c] == checker:
        total += 1
        r -= dr
        c -= dc

    return total

def check_win(board, last_r, last_c, checker):
    """
    Check if placing 'checker' at (last_r, last_c) creates a win.
    Checks 4 directions: horizontal, vertical, diag down-right, diag up-right.
    """
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (-1, 1),  # diagonal up-right
    ]
    for dr, dc in directions:
        if count_in_direction(board, last_r, last_c, dr, dc, checker) >= WIN_LEN:
            return True
    return False

def board_full(board):
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

# =========================
# Main game loop
# =========================
def main():
    validate_settings()
    rows, cols = ROWS, COLS
    board = create_board(rows, cols)

    # Prepare players
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select first player
    current_idx = random.randint(0, NUM_PLAYERS - 1)

    # Initial display before the game starts
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        current_player = players[current_idx]

        # Prompt for input (must be valid letter)
        col = get_valid_column_input(current_player, cols)

        # Attempt to place; if column is full, turn is lost
        placed, row_idx = place_checker(board, col, current_player)

        # After the "turn" (whether placed or not), clear and print updated board
        clear_screen()
        print_board(board)

        if not placed:
            letters = string.ascii_uppercase[:cols]
            print(f"Column {letters[col]} is full. Player {current_player} loses the turn.")
            # Advance to next player
            current_idx = (current_idx + 1) * 1 % NUM_PLAYERS
            # Continue to next iteration without win/draw check
            continue

        # Check for win
        if check_win(board, row_idx, col, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
