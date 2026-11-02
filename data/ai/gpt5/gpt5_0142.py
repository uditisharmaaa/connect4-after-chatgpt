import os
import random
import sys

# Constants (adjustable, but submission requires ROWS=6, COLS=7, NUM_PLAYERS=2)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
WIN_LENGTH = 4

CHECKERS = ["X", "O", "V", "H", "M"]

# Ensure constraints
if COLS > 26:
    COLS = 26
if NUM_PLAYERS < 2:
    NUM_PLAYERS = 2
if NUM_PLAYERS > 5:
    NUM_PLAYERS = 5

PLAYERS = CHECKERS[:NUM_PLAYERS]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    cols = len(board[0])
    # Header with column letters
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(header)
    sep = "+" + ("---+" * cols)
    for r in range(len(board)):
        print(sep)
        row = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row)
    print(sep)


def is_valid_column_input(s, cols):
    if len(s) != 1:
        return False
    if not s.isalpha():
        return False
    idx = ord(s) - ord('A')
    return 0 <= idx < cols


def find_lowest_empty_row(board, col):
    # Returns row index where the checker will land, or None if column is full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def place_checker(board, col, symbol):
    r = find_lowest_empty_row(board, col)
    if r is None:
        return None
    board[r][col] = symbol
    return r


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win_from(board, start_r, start_c, symbol):
    # Check in 4 directions: horizontal, vertical, diagonal down-right, diagonal up-right
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1

        # Check one direction
        r, c = start_r + dr, start_c + dc
        while in_bounds(r, c, rows, cols) and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc

        # Check opposite direction
        r, c = start_r - dr, start_c - dc
        while in_bounds(r, c, rows, cols) and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_LENGTH:
            return True

    return False


def is_board_full(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def main():
    board = create_board(ROWS, COLS)

    # Randomly select starting player
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial board display
    clear_screen()
    print_board(board)

    while True:
        current_player_symbol = PLAYERS[current_player_idx]
        # Prompt until valid input (except when chosen column is full; then turn is lost)
        while True:
            try:
                user_input = input(f"Player {current_player_symbol}, please enter a column:\n").strip().upper()
            except EOFError:
                # If input is closed, exit gracefully
                print()
                sys.exit(0)

            if not is_valid_column_input(user_input, COLS):
                # Invalid input; ask again without losing turn
                continue

            col_idx = ord(user_input) - ord('A')
            row_idx = place_checker(board, col_idx, current_player_symbol)

            clear_screen()
            print_board(board)

            if row_idx is None:
                # Column full: player loses the turn
                # After an invalid (full) move, check for draw (unlikely to change here, but safe)
                if is_board_full(board):
                    print("It's a draw!")
                    return
                # Move to next player
                current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
                break
            else:
                # Successful move: check win
                if check_win_from(board, row_idx, col_idx, current_player_symbol):
                    print(f"Player {current_player_symbol} won!")
                    return

                # Check for draw
                if is_board_full(board):
                    print("It's a draw!")
                    return

                # Move to next player
                current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
                break


if __name__ == "__main__":
    main()
