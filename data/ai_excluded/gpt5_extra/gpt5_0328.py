import os
import random
import string
import sys

# =========================
# Configuration constants
# =========================
ROWS = 6            # Number of rows (default submission: 6)
COLS = 7            # Number of columns, max 26 (default submission: 7)
NUM_PLAYERS = 2     # Number of players, between 2 and 5 (default submission: 2)
CHECKERS = ["X", "O", "V", "H", "M"]  # In this order

WIN_LENGTH = 4      # Always 4-in-a-row to win as per assignment


# =========================
# Utility functions
# =========================
def clear_screen():
    # Assignment requires: os.system('clear') for Linux/Unix
    try:
        os.system('clear')
    except Exception:
        pass


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def col_labels(n):
    # Up to 26 columns: 'A' .. 'Z'
    return list(string.ascii_uppercase[:n])


def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    labels = col_labels(cols)

    # Header labels
    # Example style: two spaces then labels with three spaces separation
    print("  " + "   ".join(labels))

    # Top border
    print("+---" * cols + "+")

    for r in range(rows):
        # Row cells
        row_str = []
        for c in range(cols):
            cell = board[r][c]
            if len(cell) != 1:
                cell = " "
            row_str.append(cell)
        print("| " + " | ".join(row_str) + " |")
        # Row border
        print("+---" * cols + "+")


def input_column(num_cols):
    labels = col_labels(num_cols)
    valid_set = set(labels)
    while True:
        try:
            user_in = input("Please enter a column ({}-{}): ".format(labels[0], labels[-1])).strip()
        except EOFError:
            # End input gracefully
            print("\nInput closed. Exiting game.")
            sys.exit(0)

        if len(user_in) != 1:
            print("Invalid input. Enter a single letter from {} to {}.".format(labels[0], labels[-1]))
            continue
        ch = user_in.upper()
        if ch not in valid_set:
            print("Invalid column. Choose a letter from {} to {}.".format(labels[0], labels[-1]))
            continue
        return labels.index(ch)


def place_checker(board, col, checker):
    rows = len(board)
    # Start from bottom row up
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return (r, col)
    return None  # Column full


def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    n = WIN_LENGTH

    # Directions: right, down, diag down-right, diag up-right
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker and count < n:
                    count += 1
                    rr += dr
                    cc += dc
                if count >= n:
                    return True
    return False


def setup_and_validate():
    # Validate configuration
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if COLS < 1 or COLS > 26:
        print("COLS must be between 1 and 26.")
        sys.exit(1)
    if ROWS < 1:
        print("ROWS must be at least 1.")
        sys.exit(1)


def main():
    setup_and_validate()

    rows, cols = ROWS, COLS
    board = create_board(rows, cols)

    players = CHECKERS[:NUM_PLAYERS]
    current = random.randint(0, NUM_PLAYERS - 1)

    # Initial display
    print_board(board)

    # Game loop
    while True:
        player_symbol = players[current]
        print(f"Player {player_symbol}, please enter a column:")

        col = input_column(cols)

        placed = place_checker(board, col, player_symbol)
        if placed is None:
            # Column full: turn is invalid and player loses the turn
            print_board(board)
            label = col_labels(cols)[col]
            print(f"Column {label} is full. Player {player_symbol} loses the turn.")
            # Check for draw even if turn lost (board could be full)
            if board_full(board):
                print("It's a draw!")
                break
            current = (current + 1) % NUM_PLAYERS
            continue

        # After placing, print updated board
        print_board(board)

        # Check for win
        if check_win(board, player_symbol):
            print(f"Player {player_symbol} won!")
            break

        # Check for draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current = (current + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
