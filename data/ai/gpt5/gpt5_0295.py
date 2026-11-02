import os
import random
import string
import sys

# -------------------------
# Configuration (constants)
# -------------------------
ROWS = 6               # Number of rows (e.g., 6)
COLS = 7               # Number of columns (e.g., 7, max 26)
NUM_PLAYERS = 2        # Number of players (between 2 and 5)
WIN_LENGTH = 4         # Number in a row needed to win (always 4)
CHECKERS = ["X", "O", "V", "H", "M"]  # Order of player checkers

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
    print("ROWS must be >= 1.")
    sys.exit(1)

# Select the checkers for the given number of players
PLAYERS = CHECKERS[:NUM_PLAYERS]
COL_LABELS = list(string.ascii_uppercase[:COLS])

# -------------------------
# Board creation and utils
# -------------------------
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    # Clear screen for Unix/Linux/macOS terminals
    os.system('clear')

def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Header with column labels
    header = "  " + "   ".join(COL_LABELS[:cols])
    sep = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print(sep)

def board_full(board):
    # If any top cell in any column is empty, board is not full
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def find_drop_row(board, col):
    # Return the bottom-most empty row index for given column, or None if column full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

# -------------------------
# Win checking
# -------------------------
def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_direction(board, start_r, start_c, dr, dc, symbol):
    rows = len(board)
    cols = len(board[0])
    count = 0
    r, c = start_r, start_c
    for _ in range(WIN_LENGTH):
        if in_bounds(r, c, rows, cols) and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        else:
            break
    return count == WIN_LENGTH

def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])
    # For each cell, check 4 directions that cover all lines:
    # Right (0,1), Down (1,0), Down-Right (1,1), Down-Left (1,-1)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                if check_direction(board, r, c, dr, dc, symbol):
                    return True
    return False

# -------------------------
# Input handling
# -------------------------
def prompt_for_column(current_player_symbol):
    while True:
        user_input = input(f"Player {current_player_symbol}, please enter a column: ").strip()
        if not user_input:
            print("Invalid input. Please enter a column letter.")
            continue

        # Accept letters, case-insensitive
        col_letter = user_input.upper()

        if len(col_letter) != 1 or col_letter < "A" or col_letter > chr(ord("A") + COLS - 1):
            print(f"Invalid column. Enter a letter between A and {COL_LABELS[COLS - 1]}.")
            continue

        col_index = ord(col_letter) - ord("A")
        return col_index

# -------------------------
# Game loop
# -------------------------
def main():
    board = create_board(ROWS, COLS)

    # Randomly choose starting player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Initial display
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        # Check draw before asking (entire board filled)
        if board_full(board):
            print("The game is a draw.")
            break

        current_symbol = PLAYERS[current_player_idx]

        # Get a valid column letter from user
        col = prompt_for_column(current_symbol)

        # Determine drop row
        drop_row = find_drop_row(board, col)
        if drop_row is None:
            # Column is full: turn is invalid and the player loses the turn
            clear_screen()
            print_board(board)
            print(f"Column {COL_LABELS[col]} is full. Player {current_symbol} loses the turn.")
            # Move to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Place the checker
        board[drop_row][col] = current_symbol

        # Print updated board
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check for draw
        if board_full(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    # Seed randomness for fairness
    random.seed()
    # Show initial empty board and indicate random player chosen before first turn
    # The main loop will handle displaying and prompting.
    main()
