import os
import random
import string
import sys

# ----------------------------
# Configuration (as required for submission)
# ----------------------------
ROWS = 6
COLUMNS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5 inclusive

# ----------------------------
# Constants and Validation
# ----------------------------
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]  # In order, as required

if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if not (1 <= COLUMNS <= 26):
    print("COLUMNS must be between 1 and 26.")
    sys.exit(1)

if ROWS < 1:
    print("ROWS must be at least 1.")
    sys.exit(1)

PLAYER_SYMBOLS = CHECKERS[:NUM_PLAYERS]
COLUMN_LABELS = list(string.ascii_uppercase[:COLUMNS])


# ----------------------------
# Utility Functions
# ----------------------------
def clear_screen():
    # Clear terminal screen (Linux/Unix)
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    # Header with column labels
    header = "  " + "   ".join(COLUMN_LABELS)
    sep_line = "+" + "+".join(["---"] * COLUMNS) + "+"

    print(header)
    print(sep_line)
    for r in range(ROWS):
        row_cells = "|".join(f" {board[r][c]} " for c in range(COLUMNS))
        print(f"|{row_cells}|")
        print(sep_line)


def get_column_index_from_label(label):
    label = label.upper()
    if label in COLUMN_LABELS:
        return COLUMN_LABELS.index(label)
    return None


def get_lowest_empty_row(board, col):
    # Returns the row index where the checker will land, or None if the column is full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def place_checker(board, row, col, symbol):
    board[row][col] = symbol


def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLUMNS


def check_win(board, symbol):
    # Check all cells as potential start of a winning line
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while count < WIN_LENGTH and in_bounds(nr, nc) and board[nr][nc] == symbol:
                    count += 1
                    nr += dr
                    nc += dc
                if count == WIN_LENGTH:
                    return True
    return False


def is_draw(board):
    # Draw if no spaces left
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == " ":
                return False
    return True


def prompt_for_column(player_symbol):
    while True:
        try:
            inp = input(f"Player {player_symbol}, please enter a column: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting game.")
            sys.exit(0)

        if len(inp) != 1 or not inp.isalpha():
            print("Invalid input. Please enter a single letter corresponding to a column.")
            continue

        col_idx = get_column_index_from_label(inp)
        if col_idx is None:
            print(f"Invalid column. Please enter a letter between {COLUMN_LABELS[0]} and {COLUMN_LABELS[-1]}.")
            continue

        return col_idx


# ----------------------------
# Game Loop
# ----------------------------
def main():
    board = create_board(ROWS, COLUMNS)

    # Randomly choose starting player
    current_player_index = random.randrange(NUM_PLAYERS)

    # Initial board print
    clear_screen()
    print_board(board)

    while True:
        current_symbol = PLAYER_SYMBOLS[current_player_index]

        # Ask for a valid column letter (invalid letters do not lose the turn)
        col = prompt_for_column(current_symbol)

        # Determine if the move can be made (if column is full, the turn is lost)
        row = get_lowest_empty_row(board, col)
        if row is None:
            print(f"Column {COLUMN_LABELS[col]} is full. Turn lost.")
            # Next player's turn, print same board (no update)
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            clear_screen()
            print_board(board)
            continue

        # Place checker
        place_checker(board, row, col, current_symbol)

        # Clear and print updated board
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check for draw
        if is_draw(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
