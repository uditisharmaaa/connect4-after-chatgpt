import os
import random
import string
import sys

# -------------------------
# Configuration (constants)
# -------------------------
ROWS = 6
COLS = 7  # Max 26 (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5

CHECKERS = ["X", "O", "V", "H", "M"]

# -------------------------
# Validation of constants
# -------------------------
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if COLS < 1 or COLS > 26:
    print("COLS must be between 1 and 26.")
    sys.exit(1)

if ROWS < 1:
    print("ROWS must be at least 1.")
    sys.exit(1)

PLAYERS = CHECKERS[:NUM_PLAYERS]

# -------------------------
# Board utilities
# -------------------------
def make_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    # As per assignment spec, use 'clear' (Linux/Unix)
    os.system('clear')

def print_board(board):
    rows = len(board)
    cols = len(board[0])
    letters = string.ascii_uppercase[:cols]

    # Header
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

def board_full(board):
    for r in board:
        for cell in r:
            if cell == " ":
                return False
    return True

def find_lowest_empty_row(board, col):
    # Return the row index of the lowest empty cell in a column, or None if full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

# -------------------------
# Input handling
# -------------------------
def prompt_for_column(current_checker, max_col_index):
    last_letter = string.ascii_uppercase[max_col_index]
    while True:
        try:
            user_in = input(f"Player {current_checker}, please enter a column: ").strip()
        except EOFError:
            # Treat EOF as invalid input; reprompt
            continue
        if len(user_in) != 1:
            # invalid length
            continue
        ch = user_in.upper()
        if "A" <= ch <= last_letter:
            return ord(ch) - ord('A')
        # otherwise invalid; loop to reprompt

# -------------------------
# Win checking
# -------------------------
def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while in_bounds(nr, nc, rows, cols) and board[nr][nc] == checker:
                    count += 1
                    if count == 4:
                        return True
                    nr += dr
                    nc += dc
    return False

# -------------------------
# Main game loop
# -------------------------
def main():
    board = make_board(ROWS, COLS)

    # Randomly select first player
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial print
    clear_screen()
    print_board(board)

    while True:
        current_checker = PLAYERS[current_player_idx]

        # Get a valid column letter input
        col = prompt_for_column(current_checker, COLS - 1)

        # Try to place checker
        row = find_lowest_empty_row(board, col)
        if row is None:
            # Column full: turn is invalid and player loses the turn
            clear_screen()
            print_board(board)
            # Move to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            # Continue to next turn
            continue
        else:
            board[row][col] = current_checker

        # After placing, check for a win
        if check_win(board, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("Game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

        # Print updated board
        clear_screen()
        print_board(board)

if __name__ == "__main__":
    main()
