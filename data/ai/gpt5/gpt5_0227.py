import os
import random
import string
import sys

# ----------------------------- Configuration ---------------------------------
# Submission requires 6 rows x 7 columns and 2 players by default.
ROWS = 6
COLS = 7            # Max 26
NUM_PLAYERS = 2     # Between 2 and 5 inclusive
CHECKERS = ["X", "O", "V", "H", "M"]

# ------------------------------ Utilities ------------------------------------
def clear_screen():
    # Required by assignment to clear before printing
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    # Returns list of 'A', 'B', ...
    return [chr(ord('A') + i) for i in range(cols)]


def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows else 0
    labels = column_labels(cols)

    # Header with column labels
    print("  " + "   ".join(labels))
    # Top border
    print("+" + "+".join(["---"] * cols) + "+")

    # Each row
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + "+".join(["---"] * cols) + "+")


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def get_lowest_empty_row(board, col):
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None  # Column is full


def drop_checker(board, col, checker):
    r = get_lowest_empty_row(board, col)
    if r is None:
        return False
    board[r][col] = checker
    return True


def is_winner(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Directions: (dr, dc)
    directions = [
        (0, 1),    # horizontal right
        (1, 0),    # vertical down
        (1, 1),    # diagonal down-right
        (1, -1),   # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while in_bounds(rr, cc, rows, cols) and board[rr][cc] == checker:
                    count += 1
                    if count == 4:
                        return True
                    rr += dr
                    cc += dc
    return False


def is_draw(board):
    # Draw if no empty cells remain
    for row in board:
        if " " in row:
            return False
    return True


def prompt_for_column(valid_cols):
    # valid_cols: number of columns
    labels = column_labels(valid_cols)
    valid_set = set(labels)

    while True:
        user_input = input().strip()
        if len(user_input) != 1:
            print("Invalid input. Please enter a single uppercase letter corresponding to a column:")
            continue
        ch = user_input.upper()
        if ch not in valid_set:
            print("Invalid column. Please enter one of: " + ", ".join(labels))
            continue
        return ord(ch) - ord('A')


def enforce_config():
    # Ensure constraints are within allowed bounds
    global COLS, NUM_PLAYERS
    if COLS > 26:
        COLS = 26
    if NUM_PLAYERS < 2:
        NUM_PLAYERS = 2
    if NUM_PLAYERS > 5:
        NUM_PLAYERS = 5


# ------------------------------ Game Loop -------------------------------------
def play_connect4(rows, cols, num_players):
    enforce_config()

    # Select checkers for players
    players = CHECKERS[:num_players]

    # Initialize board
    board = create_board(rows, cols)

    # Randomly choose starting player
    current = random.randrange(num_players)

    # Initial display
    clear_screen()
    print_board(board)

    while True:
        current_checker = players[current]
        print(f"Player {current_checker}, please enter a column:")
        col = prompt_for_column(cols)

        # Attempt to place checker
        placed = drop_checker(board, col, current_checker)

        # After the turn (whether placed or not), clear and print the board
        clear_screen()
        print_board(board)

        if not placed:
            # Column full, player loses the turn
            print(f"Column {chr(ord('A') + col)} is full. Player {current_checker} loses the turn.")
            # Advance to next player
            current = (current + 1) % num_players
            continue

        # Check for win
        if is_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player
        current = (current + 1) % num_players


def main():
    # Seed randomness
    random.seed()

    play_connect4(ROWS, COLS, NUM_PLAYERS)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print("Game interrupted.")
        sys.exit(0)
