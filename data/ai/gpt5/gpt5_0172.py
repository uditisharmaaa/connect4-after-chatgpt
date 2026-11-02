import os
import random
import string
import sys

# Configuration (submission requires 6 rows, 7 columns, 2 players)
ROWS = 6
COLS = 7  # must be <= 26
NUM_PLAYERS = 2  # allowed 2..5
WIN_LENGTH = 4

CHECKERS = ["X", "O", "V", "H", "M"]  # up to 5 players


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    # Labels A.. up to 26 columns
    return list(string.ascii_uppercase[:cols])


def print_board(board):
    labels = column_labels(len(board[0]))
    # Header
    header = "  " + "   ".join(labels)
    sep = "+" + "+".join(["---"] * len(labels)) + "+"
    print(header)
    print(sep)
    for r in range(len(board)):
        row_cells = []
        for c in range(len(board[0])):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
        print(sep)


def get_valid_input(cols):
    labels = column_labels(cols)
    valid_set = set(labels)
    while True:
        user_in = input("Please enter a column: ").strip().upper()
        if len(user_in) != 1 or user_in not in valid_set:
            print(f"Invalid input. Enter a single letter between {labels[0]} and {labels[-1]}.")
            continue
        return labels.index(user_in)


def find_drop_row(board, col_idx):
    # Return the row index where the checker will land, or None if column full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_idx] == " ":
            return r
    return None


def drop_checker(board, col_idx, checker):
    row = find_drop_row(board, col_idx)
    if row is None:
        return None
    board[row][col_idx] = checker
    return row


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while in_bounds(nr, nc, rows, cols) and board[nr][nc] == checker:
                    count += 1
                    if count >= WIN_LENGTH:
                        return True
                    nr += dr
                    nc += dc
    return False


def board_full(board):
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True


def play_game():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("NUM_PLAYERS must be between 2 and 5.")
        return
    if COLS < 1 or COLS > 26:
        print("COLS must be between 1 and 26.")
        return
    if ROWS < 1:
        print("ROWS must be at least 1.")
        return

    players = CHECKERS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    current_idx = random.randrange(NUM_PLAYERS)

    # Initial board print before the game starts
    clear_screen()
    print_board(board)

    while True:
        checker = players[current_idx]
        print(f"Player {checker}, it's your turn.")
        # Prompt and validate input (invalid inputs re-prompt; turn not lost)
        col_idx = get_valid_input(COLS)

        # Attempt to place; if column full, turn is lost
        drop_row = find_drop_row(board, col_idx)
        if drop_row is None:
            print(f"Column {column_labels(COLS)[col_idx]} is full. Turn lost.")
            input("Press Enter to continue...")
            current_idx = (current_idx + 1) % NUM_PLAYERS
            clear_screen()
            print_board(board)
            continue

        # Place checker
        drop_checker(board, col_idx, checker)

        # Clear and print updated board
        clear_screen()
        print_board(board)

        # Check win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break

        # Check draw
        if board_full(board):
            print("The game is a draw.")
            break

        # Next player
        current_idx = (current_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\nGame interrupted.")
        sys.exit(0)
