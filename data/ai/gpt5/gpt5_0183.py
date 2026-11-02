import os
import random
import sys

# ------------------------------
# Connect 4 - Python 3
# Works in a Linux/Unix terminal
# ------------------------------

# Configuration (submission requires 6 rows x 7 columns and 2 players)
ROWS = 6
COLS = 7  # max 26 (A-Z)
NUM_PLAYERS = 2  # allowed: 2 to 5
CHECKERS = ["X", "O", "V", "H", "M"]  # in order for up to 5 players
WIN_LENGTH = 4  # always 4, independent of number of players

# Validate configuration
if COLS > 26:
    print("Error: COLS must be <= 26 (A-Z).")
    sys.exit(1)
if not (2 <= NUM_PLAYERS <= 5):
    print("Error: NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

ACTIVE_CHECKERS = CHECKERS[:NUM_PLAYERS]
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]


def clear_screen():
    # Per assignment: ensure screen is cleared before printing updated board
    os.system('clear')


def create_board(rows, cols):
    # 2D board initialized with spaces (" ")
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
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
        print(sep)


def is_valid_column_label(label):
    return len(label) == 1 and label.isalpha() and label.upper() in COLUMN_LABELS[:COLS]


def column_to_index(label):
    return ord(label.upper()) - ord('A')


def find_lowest_empty_row(board, col_idx):
    # Return the row index of the lowest empty cell in column col_idx, or None if full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_idx] == " ":
            return r
    return None


def board_full(board):
    # If any top cell is empty, board isn't full
    return all(board[0][c] != " " for c in range(len(board[0])))


def check_direction(board, start_r, start_c, dr, dc, checker):
    rows = len(board)
    cols = len(board[0])
    count = 0
    r, c = start_r, start_c
    for _ in range(WIN_LENGTH):
        if 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        else:
            return False
    return count == WIN_LENGTH


def check_win(board, last_r, last_c, checker):
    # Check all directions through the last placed cell
    # To cover runs longer than 4, scan windows that include last cell

    rows = len(board)
    cols = len(board[0])

    # Directions: (dr, dc)
    directions = [
        (0, 1),    # horizontal right
        (1, 0),    # vertical down
        (1, 1),    # diag down-right
        (1, -1),   # diag down-left
    ]

    for dr, dc in directions:
        # We want to scan a sliding window of size WIN_LENGTH centered around last move,
        # moving back up to WIN_LENGTH-1 steps in the negative direction.
        for offset in range(-(WIN_LENGTH - 1), 1):
            start_r = last_r + offset * dr
            start_c = last_c + offset * dc
            if check_direction(board, start_r, start_c, dr, dc, checker):
                return True
    return False


def get_player_input(current_checker):
    while True:
        user_in = input(f"Player {current_checker}, please enter a column: ").strip()
        # Validate input: must be a single letter corresponding to a column
        if not is_valid_column_label(user_in):
            print("Invalid input. Please enter a valid column letter (e.g., A).")
            continue
        return user_in.upper()


def game_loop():
    board = create_board(ROWS, COLS)
    # Random first player
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial board display
    clear_screen()
    print_board(board)

    while True:
        current_checker = ACTIVE_CHECKERS[current_player_idx]
        col_label = get_player_input(current_checker)
        col_idx = column_to_index(col_label)

        # Attempt to place checker
        row_idx = find_lowest_empty_row(board, col_idx)

        if row_idx is None:
            # Column is full: invalid turn, player loses the turn
            print(f"Column {col_label} is full. Player {current_checker} loses the turn.")
            # Show the unchanged board again
            input("Press Enter to continue...")
            # Next player's turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            clear_screen()
            print_board(board)
            continue

        # Place checker
        board[row_idx][col_idx] = current_checker

        # Update display
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, row_idx, col_idx, current_checker):
            print(f"Player {current_checker} won!")
            return

        # Check for draw
        if board_full(board):
            print("Game is a draw.")
            return

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


def main():
    # Seed randomness for first-player selection
    random.seed()
    game_loop()


if __name__ == "__main__":
    main()
