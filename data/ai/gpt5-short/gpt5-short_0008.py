#!/usr/bin/env python3
import os
import random
import sys

# =========================
# Configuration constants
# =========================
ROWS = 6
COLS = 7
COLUMN_LABELS = "ABCDEFG"

# Choose how many players (2 to 5)
NUM_PLAYERS = 2  # Change to 2, 3, 4, or 5

# Player tokens in order (will use first NUM_PLAYERS)
TOKENS = "XOVHM"

assert 2 <= NUM_PLAYERS <= 5, "NUM_PLAYERS must be between 2 and 5"
assert len(TOKENS) >= NUM_PLAYERS, "Not enough tokens provided for NUM_PLAYERS"


# =========================
# Game logic
# =========================
def clear_screen():
    # As requested, use 'clear' (works on most UNIX-like systems)
    os.system('clear')


def create_board(rows=ROWS, cols=COLS):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    # Header
    print("  " + " ".join(COLUMN_LABELS))
    # Rows
    for r in range(len(board)):
        print("| " + " ".join(board[r]) + " |")
    print("+" + "--" * COLS + "+")
    print("Enter column letter (A-G). Ctrl-C or Ctrl-D to quit.")


def drop_piece(board, col, token):
    # Attempt to drop a piece in the specified column (0-based).
    # Returns the row index it landed on, or None if the column is full.
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r
    return None


def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS


def check_win(board, token):
    # Check 4 directions: right, down, down-right, down-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while count < 4 and in_bounds(rr, cc) and board[rr][cc] == token:
                    count += 1
                    rr += dr
                    cc += dc
                if count == 4:
                    return True
    return False


def check_draw(board):
    # Draw if no spaces left in the top row (or anywhere)
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True


def get_column_input(board, token):
    while True:
        try:
            choice = input(f"Player {token}, choose a column (A-G): ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting game.")
            sys.exit(0)

        if len(choice) != 1 or choice not in COLUMN_LABELS:
            print("Invalid input. Please enter a single letter A-G.")
            continue

        col = COLUMN_LABELS.index(choice)
        if board[0][col] != " ":
            print("That column is full. Choose another.")
            continue

        return col


def main():
    board = create_board()
    players = list(TOKENS[:NUM_PLAYERS])

    # Choose a random starting player index
    current_index = random.randrange(len(players))

    while True:
        print_board(board)
        token = players[current_index]

        col = get_column_input(board, token)
        row = drop_piece(board, col, token)

        # drop_piece should never return None here due to prior validation, but be safe:
        if row is None:
            print("Unexpected: column is full. Try again.")
            continue

        # Reprint after move
        print_board(board)

        if check_win(board, token):
            print(f"Player {token} wins!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_index = (current_index + 1) % len(players)


if __name__ == "__main__":
    main()
