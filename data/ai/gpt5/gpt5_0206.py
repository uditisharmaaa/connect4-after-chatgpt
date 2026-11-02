import os
import random
import sys

# Constants (you can change ROWS, COLS, NUM_PLAYERS for testing; keep as below for submission)
ROWS = 6
COLS = 7   # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
WIN_LENGTH = 4
CHECKERS_AVAILABLE = ["X", "O", "V", "H", "M"]

# Ensure constraints
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if COLS < 1 or COLS > 26:
    print("COLS must be between 1 and 26.")
    sys.exit(1)
if ROWS < 1:
    print("ROWS must be at least 1.")
    sys.exit(1)

CHECKERS = CHECKERS_AVAILABLE[:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Header with letters A, B, C, ...
    letters = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(letters))
    # Separator line
    sep = "+" + "+".join(["---"] * len(board[0])) + "+"
    for r in range(len(board)):
        print(sep)
        row_cells = "|" + "|".join(f" {board[r][c]} " for c in range(len(board[0]))) + "|"
        print(row_cells)
    print(sep)

def get_column_index_from_input(user_input):
    user_input = user_input.strip().upper()
    if len(user_input) != 1:
        return None
    if not ('A' <= user_input <= 'Z'):
        return None
    idx = ord(user_input) - ord('A')
    if 0 <= idx < COLS:
        return idx
    return None

def find_row_for_col(board, col_idx):
    # Return the lowest available row index in the column, or None if full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col_idx] == " ":
            return r
    return None

def is_board_full(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def check_win_from_cell(board, start_r, start_c, dr, dc, checker):
    # Check WIN_LENGTH from (start_r, start_c) in direction (dr, dc)
    for k in range(WIN_LENGTH):
        r = start_r + dr * k
        c = start_c + dc * k
        if r < 0 or r >= ROWS or c < 0 or c >= COLS:
            return False
        if board[r][c] != checker:
            return False
    return True

def check_win(board, checker):
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (-1, 1),  # diagonal up-right
    ]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                if check_win_from_cell(board, r, c, dr, dc, checker):
                    return True
    return False

def main():
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        print(f"Player {CHECKERS[current_player]}, please enter a column:")

        # Get valid input (letters and range). Keep prompting until valid letter in range.
        # Note: If the selected column is full, the player loses the turn (no re-prompt).
        col_idx = None
        while col_idx is None:
            user_in = input("> ")
            col_idx = get_column_index_from_input(user_in)
            if col_idx is None:
                print("Invalid input. Please enter a single letter for a valid column (e.g., A, B, C).")

        # Try to place the checker
        row_idx = find_row_for_col(board, col_idx)
        if row_idx is None:
            print("That column is full. Turn lost!")
            input("Press Enter to continue...")
            # Advance to next player
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        # Place checker
        checker = CHECKERS[current_player]
        board[row_idx][col_idx] = checker

        # Check for win
        if check_win(board, checker):
            clear_screen()
            print_board(board)
            print(f"Player {checker} won!")
            break

        # Check for draw
        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("Game is a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    # Show initial empty board before the game starts
    # Random player already selected inside main (as per spec)
    main()
