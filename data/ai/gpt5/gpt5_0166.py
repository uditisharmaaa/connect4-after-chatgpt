import os
import random
import sys

# Constants (Submission requires 6 rows x 7 columns and 2 players)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

# Player symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if COLS < 1 or COLS > 26:
    print("COLS must be between 1 and 26.")
    sys.exit(1)

SYMBOLS = PLAYER_SYMBOLS[:NUM_PLAYERS]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Column labels
    labels = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(labels)

    # Horizontal separator
    sep = "+" + ("---+" * cols)

    for r in range(rows):
        print(sep)
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print(sep)


def is_valid_column_input(s):
    if len(s) != 1:
        return False
    ch = s.upper()
    if ch < 'A' or ch >= chr(ord('A') + COLS):
        return False
    return True


def get_player_input(current_symbol):
    while True:
        entry = input(f"Player {current_symbol}, please enter a column: ").strip().upper()
        if is_valid_column_input(entry):
            return ord(entry) - ord('A')
        else:
            print(f"Invalid input. Please enter a column letter between A and {chr(ord('A') + COLS - 1)}.")


def drop_checker(board, col, symbol):
    # Returns (row_index) if placed, or None if column full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return r
    return None  # Column full


def count_in_direction(board, start_r, start_c, dr, dc, symbol):
    r, c = start_r + dr, start_c + dc
    count = 0
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    return count


def check_win(board, r, c, symbol):
    # Check 4 directions: horizontal, vertical, diag down-right, diag up-right
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        total = 1  # include the placed checker
        total += count_in_direction(board, r, c, dr, dc, symbol)
        total += count_in_direction(board, r, c, -dr, -dc, symbol)
        if total >= 4:
            return True
    return False


def board_full(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True


def main():
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        current_symbol = SYMBOLS[current_player]

        col = get_player_input(current_symbol)

        placed_row = drop_checker(board, col, current_symbol)
        if placed_row is None:
            # Column full: turn is invalid and player loses the turn
            # No reprompt; just move to the next player
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        # Check for win
        if check_win(board, placed_row, col, current_symbol):
            clear_screen()
            print_board(board)
            print(f"Player {current_symbol} won!")
            break

        # Check for draw
        if board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
