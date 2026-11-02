import os
import random
import string
import sys

# ----- Configuration constants -----
ROWS = 6                  # Number of rows (height)
COLS = 7                  # Number of columns (width), max 26
NUM_PLAYERS = 2           # Number of players, between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]  # Player symbols in order
WIN_LENGTH = 4            # Number of checkers in a row to win

# ----- Validation of configuration -----
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if not (1 <= COLS <= 26):
    print("COLS must be between 1 and 26.")
    sys.exit(1)

PLAYERS = CHECKERS[:NUM_PLAYERS]
COLUMN_LABELS = list(string.ascii_uppercase[:COLS])


# ----- Utility functions -----
def clear_screen():
    # Clear terminal screen (Unix-like)
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    # Header with column letters
    header = "  " + "   ".join(COLUMN_LABELS)
    sep = "+" + "+".join(["---"] * COLS) + "+"
    print(header)
    print(sep)
    for r in range(ROWS):
        row_str = "|" + "|".join(f" {board[r][c]} " for c in range(COLS)) + "|"
        print(row_str)
        print(sep)


def is_full(board):
    # Board is full if no spaces in top row (or equivalently anywhere)
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True


def drop_checker(board, col, symbol):
    # Attempt to drop 'symbol' into column 'col' (0-indexed).
    # Returns tuple (success, row_index) where success is True if placed.
    # If column is full, returns (False, None).
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return True, r
    return False, None


def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS


def count_in_direction(board, start_r, start_c, dr, dc, symbol):
    # Count consecutive 'symbol' cells starting from (start_r, start_c) inclusive
    # going in direction (dr, dc).
    count = 0
    r, c = start_r, start_c
    while in_bounds(r, c) and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    return count


def check_win(board, r, c, symbol):
    # Check all 4 directions (pairs) through the placed piece at (r, c).
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        # Count both directions, subtract 1 to avoid double-counting the origin
        total = (
            count_in_direction(board, r, c, dr, dc, symbol) +
            count_in_direction(board, r, c, -dr, -dc, symbol) - 1
        )
        if total >= WIN_LENGTH:
            return True
    return False


def prompt_for_column(player_symbol):
    while True:
        try:
            user_input = input(f"Player {player_symbol}, please enter a column: ").strip()
        except EOFError:
            # If input ends unexpectedly, treat as invalid and continue prompting
            continue

        if len(user_input) != 1:
            print("Invalid input. Please enter a single uppercase letter for the column.")
            continue

        ch = user_input.upper()
        if ch not in COLUMN_LABELS:
            print("Invalid column. Please enter a valid column letter on the board.")
            continue

        return COLUMN_LABELS.index(ch)


# ----- Game loop -----
def main():
    board = create_board(ROWS, COLS)

    # Randomly select starting player index
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial display
    clear_screen()
    print_board(board)

    # Main game loop
    while True:
        player_symbol = PLAYERS[current_player_idx]

        # Prompt for a valid column letter
        col = prompt_for_column(player_symbol)

        # Try to place the checker
        placed, row = drop_checker(board, col, player_symbol)

        # After action, clear and show board (as per requirement)
        clear_screen()

        if not placed:
            # Column full: player loses the turn (no re-prompt)
            print_board(board)
            print(f"Column {COLUMN_LABELS[col]} is full. Player {player_symbol} loses the turn.")
            # Move to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Print updated board
        print_board(board)

        # Check for win after a successful placement
        if check_win(board, row, col, player_symbol):
            print(f"Player {player_symbol} won!")
            break

        # Check for draw
        if is_full(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
