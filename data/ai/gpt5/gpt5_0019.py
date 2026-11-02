import os
import random
import string
import sys
import time

# =========================
# Configuration (constants)
# =========================
ROWS = 6                 # Number of rows (standard Connect 4 uses 6)
COLUMNS = 7              # Number of columns (standard Connect 4 uses 7); must be <= 26
NUM_PLAYERS = 2          # Between 2 and 5

# Player checkers in order (use the first NUM_PLAYERS of these)
PLAYER_TOKENS = ["X", "O", "V", "H", "M"]

# =========================
# Validation of constants
# =========================
if not (2 <= NUM_PLAYERS <= 5):
    print("Error: NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if COLUMNS > 26 or COLUMNS < 1:
    print("Error: COLUMNS must be between 1 and 26.")
    sys.exit(1)

if ROWS < 1:
    print("Error: ROWS must be at least 1.")
    sys.exit(1)

TOKENS = PLAYER_TOKENS[:NUM_PLAYERS]
COLUMN_LABELS = list(string.ascii_uppercase[:COLUMNS])

# =========================
# Utility functions
# =========================
def clear_screen():
    # Clear the terminal screen (Linux/Unix)
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Header with column labels
    header = "  " + "   ".join(COLUMN_LABELS[:cols])
    sep = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
        print(sep)

def get_column_index_from_label(label):
    label = label.upper()
    if len(label) != 1:
        return None
    if label not in COLUMN_LABELS:
        return None
    return COLUMN_LABELS.index(label)

def get_valid_column_input():
    while True:
        try:
            user_input = input("Please enter a column: ").strip().upper()
        except EOFError:
            # In case of EOF, just exit gracefully
            print()
            sys.exit(0)
        idx = get_column_index_from_label(user_input)
        if idx is not None:
            return idx
        print("Invalid input. Enter a single column letter within the board (e.g., A, B, ...).")

def find_lowest_empty_row(board, col):
    # Start from bottom row upwards
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return None

def place_checker(board, col, token):
    row = find_lowest_empty_row(board, col)
    if row is None:
        return False
    board[row][col] = token
    return True

def within_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, token):
    rows = len(board)
    cols = len(board[0])

    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r, c
                for _ in range(3):  # need 3 more
                    rr += dr
                    cc += dc
                    if within_bounds(rr, cc, rows, cols) and board[rr][cc] == token:
                        count += 1
                    else:
                        break
                if count == 4:
                    return True
    return False

def check_draw(board):
    # Draw if there are no empty spaces left
    for row in board:
        if " " in row:
            return False
    return True

# =========================
# Main game loop
# =========================
def main():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randrange(NUM_PLAYERS)  # randomly choose starting player

    # Initial display
    clear_screen()
    print_board(board)
    print(f"Player {TOKENS[current_player]}, please enter a column:")

    while True:
        # Prompt and move
        col = get_valid_column_input()
        moved = place_checker(board, col, TOKENS[current_player])

        # After a selection, clear and show updated state (even if move invalid, board unchanged)
        clear_screen()
        print_board(board)

        if not moved:
            print(f"Column {COLUMN_LABELS[col]} is full. Player {TOKENS[current_player]} loses the turn.")
            time.sleep(1)
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS
            print(f"Player {TOKENS[current_player]}, please enter a column:")
            continue

        # Check win
        if check_win(board, TOKENS[current_player]):
            print(f"Player {TOKENS[current_player]} won!")
            break

        # Check draw
        if check_draw(board):
            print("Game is a draw.")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS
        print(f"Player {TOKENS[current_player]}, please enter a column:")

if __name__ == "__main__":
    main()
