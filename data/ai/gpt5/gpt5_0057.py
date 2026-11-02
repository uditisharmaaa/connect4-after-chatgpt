import os
import random
import string
import sys

# Constants (you can change ROWS, COLS, and NUM_PLAYERS for testing; submission requires 6x7 and 2 players)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

# Validate constants
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
    rows = len(board)
    cols = len(board[0])

    # Column headers
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    line = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(line)
    for r in range(rows):
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
        print(line)


def get_column_input(cols, current_player):
    valid_letters = string.ascii_uppercase[:cols]
    while True:
        try:
            user_input = input(f"Player {current_player}, please enter a column: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting game.")
            sys.exit(0)

        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter corresponding to a column.")
            continue

        letter = user_input.upper()
        if letter not in valid_letters:
            print(f"Invalid column. Please enter a letter between A and {valid_letters[-1]}.")
            continue

        return ord(letter) - ord('A')


def drop_checker(board, col, checker):
    # Place the checker in the lowest available row in the given column
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return None  # Column is full


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_direction(board, start_r, start_c, dr, dc, checker):
    count = 0
    r, c = start_r, start_c
    rows = len(board)
    cols = len(board[0])

    for _ in range(WIN_LENGTH):
        if not in_bounds(r, c, rows, cols):
            return False
        if board[r][c] != checker:
            return False
        r += dr
        c += dc
        count += 1

    return count == WIN_LENGTH


def check_win(board, last_r, last_c):
    if last_r is None or last_c is None:
        return False
    checker = board[last_r][last_c]
    if checker == " ":
        return False

    directions = [
        (0, 1),    # horizontal right
        (1, 0),    # vertical down
        (1, 1),    # diagonal down-right
        (1, -1),   # diagonal down-left
    ]

    # To catch 4 in any alignment, try starting points that include last placed checker
    # For each direction, shift back up to WIN_LENGTH-1 steps to find possible starts
    for dr, dc in directions:
        for shift in range(WIN_LENGTH):
            start_r = last_r - dr * shift
            start_c = last_c - dc * shift
            if check_direction(board, start_r, start_c, dr, dc, checker):
                return True
    return False


def board_full(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def main():
    board = create_board(ROWS, COLS)
    current_index = random.randint(0, NUM_PLAYERS - 1)

    # Initial display
    clear_screen()
    print_board(board)

    # Game loop
    last_move = (None, None)  # Track last placed position for win check
    while True:
        current_player = PLAYERS[current_index]
        # Print current turn prompt after showing board (as in example)
        try:
            col = get_column_input(COLS, current_player)
        except SystemExit:
            return

        # Try to place checker
        result = drop_checker(board, col, current_player)

        if result is None:
            # Column full, player loses the turn
            clear_screen()
            print_board(board)
            print(f"Column {chr(ord('A') + col)} is full. Player {current_player} loses the turn.")
            # Even though no move was made, we can still check for draw
            if board_full(board):
                print("It's a draw!")
                break
            current_index = (current_index + 1) % NUM_PLAYERS
            continue
        else:
            last_r, last_c = result
            clear_screen()
            print_board(board)

            if check_win(board, last_r, last_c):
                print(f"Player {current_player} won!")
                break

            if board_full(board):
                print("It's a draw!")
                break

            current_index = (current_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
