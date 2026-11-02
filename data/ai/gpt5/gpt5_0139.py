import os
import random
import string
import sys
import time

# ====== Configuration (Submission should use ROWS=6, COLS=7, PLAYERS=2) ======
NUM_ROWS = 6
NUM_COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]

# ====== Validation of configuration ======
if NUM_COLS < 1 or NUM_COLS > 26:
    print("Error: NUM_COLS must be between 1 and 26.")
    sys.exit(1)
if NUM_ROWS < 1:
    print("Error: NUM_ROWS must be at least 1.")
    sys.exit(1)
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    print("Error: NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

PLAYER_CHECKERS = CHECKERS[:NUM_PLAYERS]
COL_LABELS = list(string.ascii_uppercase[:NUM_COLS])


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    # Header labels
    header = "  " + "   ".join(COL_LABELS)
    sep = "+" + "+".join(["---"] * NUM_COLS) + "+"
    print(header)
    print(sep)
    for r in range(NUM_ROWS):
        row_cells = []
        for c in range(NUM_COLS):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
        print(sep)


def get_valid_column_input():
    while True:
        user_input = input().strip()
        if len(user_input) != 1 or user_input.upper() not in COL_LABELS:
            print("Invalid input. Please enter a single letter for a valid column (e.g., A, B, C):")
            continue
        return COL_LABELS.index(user_input.upper())


def place_checker(board, col, checker):
    # Start from bottom row upwards
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False  # Column full


def in_bounds(r, c):
    return 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS


def check_win(board, checker):
    # Directions: right, down, down-right, down-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r, c
                for _ in range(3):
                    rr += dr
                    cc += dc
                    if in_bounds(rr, cc) and board[rr][cc] == checker:
                        count += 1
                    else:
                        break
                if count == 4:
                    return True
    return False


def board_full(board):
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False
    return True


def main():
    random.seed()
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player = random.randrange(NUM_PLAYERS)

    # Initial print
    clear_screen()
    print_board(board)
    print(f"Player {PLAYER_CHECKERS[current_player]}, please enter a column:")

    while True:
        col_index = get_valid_column_input()

        placed = place_checker(board, col_index, PLAYER_CHECKERS[current_player])

        clear_screen()
        print_board(board)

        if not placed:
            print(f"Column {COL_LABELS[col_index]} is full. Player {PLAYER_CHECKERS[current_player]} loses the turn.")
            time.sleep(1.0)
        else:
            # Check win
            if check_win(board, PLAYER_CHECKERS[current_player]):
                print(f"Player {PLAYER_CHECKERS[current_player]} won!")
                break
            # Check draw
            if board_full(board):
                print("The game is a draw!")
                break

        # Next player
        current_player = (current_player + 1) % NUM_PLAYERS
        print(f"Player {PLAYER_CHECKERS[current_player]}, please enter a column:")


if __name__ == "__main__":
    main()
