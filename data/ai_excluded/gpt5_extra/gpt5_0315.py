import os
import random
import sys

# ---------------------------
# Configuration (constants)
# ---------------------------

ROWS = 6                  # Number of rows (default required by assignment: 6)
COLS = 7                  # Number of columns (default required by assignment: 7; max 26)
NUM_PLAYERS = 2           # Number of players (between 2 and 5; default required: 2)
CHECKERS = ["X", "O", "V", "H", "M"]  # Order of player checkers
CONNECT_N = 4             # Number of checkers in a row to win (fixed at 4)

# Validate configuration
if not (2 <= NUM_PLAYERS <= 5):
    raise ValueError("NUM_PLAYERS must be between 2 and 5.")
if not (1 <= COLS <= 26):
    raise ValueError("COLS must be between 1 and 26.")
if ROWS < 1:
    raise ValueError("ROWS must be at least 1.")


# ---------------------------
# Utility functions
# ---------------------------

def clear_screen():
    # Clear terminal screen (Unix/Linux)
    os.system('clear')


def make_board(rows, cols):
    # Create a board filled with spaces " "
    return [[" " for _ in range(cols)] for _ in range(rows)]


def col_label(i):
    # Convert zero-based index to column label 'A'..'Z'
    return chr(ord('A') + i)


def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0])

    # Header row with column letters
    header = "  " + "   ".join(col_label(c) for c in range(cols))
    print(header)

    # Separator
    sep = "+" + "+".join("---" for _ in range(cols)) + "+"

    # Each row
    for r in range(rows):
        print(sep)
        row_cells = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row_cells)
    print(sep)


def get_valid_column_input(cols):
    # Prompt until the user enters a syntactically valid column (A..)
    # Does NOT check if the column is full. That is handled separately.
    while True:
        try:
            user_in = input("Please enter a column: ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting game.")
            sys.exit(0)

        if len(user_in) != 1:
            print("Invalid input. Please enter a single letter corresponding to a column.")
            continue

        if not ('A' <= user_in <= 'Z'):
            print("Invalid input. Please enter a letter A-Z.")
            continue

        col_idx = ord(user_in) - ord('A')
        if not (0 <= col_idx < cols):
            print("Invalid input. Column is out of range.")
            continue

        return col_idx


def drop_checker(board, col, checker):
    # Attempt to drop a checker into the specified column.
    # Returns the row index where it landed, or None if the column is full.
    rows = len(board)
    for r in range(rows - 1, -1, -1):  # start from bottom row upwards
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return None  # column full


def check_direction(board, start_r, start_c, dr, dc, checker):
    # Count consecutive checkers in a given direction (including start cell).
    rows = len(board)
    cols = len(board[0])
    r, c = start_r, start_c
    count = 0
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count


def is_winning_move(board, row, col, checker):
    # Check all directions from (row, col) for a connect of CONNECT_N.
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        # Count in both positive and negative directions and subtract 1 (start counted twice)
        total = (
            check_direction(board, row, col, dr, dc, checker) +
            check_direction(board, row, col, -dr, -dc, checker) - 1
        )
        if total >= CONNECT_N:
            return True
    return False


def board_full(board):
    # Determine if the board has no empty cells
    return all(cell != " " for row in board for cell in row)


# ---------------------------
# Game loop
# ---------------------------

def play_game():
    board = make_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current_idx = random.randrange(NUM_PLAYERS)  # Random starting player

    # Initial board print
    print_board(board)
    print(f"Player {players[current_idx]}, you start!")

    while True:
        # Show board and prompt for input
        print_board(board)
        print(f"Player {players[current_idx]}, please enter a column:")
        col = get_valid_column_input(COLS)

        # Try to drop; if full, lose the turn
        landed_row = drop_checker(board, col, players[current_idx])
        if landed_row is None:
            print_board(board)
            print(f"Column {col_label(col)} is full. Player {players[current_idx]} loses the turn.")
            # Move to next player
            current_idx = (current_idx + 1) % NUM_PLAYERS
            continue

        # After a successful move, show updated board
        print_board(board)

        # Check for win
        if is_winning_move(board, landed_row, col, players[current_idx]):
            print(f"Player {players[current_idx]} won!")
            break

        # Check for draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
