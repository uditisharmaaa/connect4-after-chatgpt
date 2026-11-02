import os
import random
import sys

# ============================================================
# Configuration (change these constants to try other settings)
# ============================================================

ROWS = 6            # number of rows (e.g., 6)
COLS = 7            # number of columns (max 26, e.g., 7)
NUM_PLAYERS = 2     # number of players (between 2 and 5)

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]

# ============================================================
# Validation of configuration
# ============================================================

def validate_config():
    if not (2 <= NUM_PLAYERS <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    if COLS < 1 or COLS > 26:
        raise ValueError("COLS must be between 1 and 26.")
    if ROWS < 1:
        raise ValueError("ROWS must be at least 1.")

# ============================================================
# Board utilities
# ============================================================

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def column_labels(n):
    # Labels A, B, C, ...
    return [chr(ord('A') + i) for i in range(n)]

def clear_screen():
    # Requirement specifies Linux/Unix: use 'clear'
    os.system('clear')

def print_board(board, labels):
    # Header labels
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

# ============================================================
# Game mechanics
# ============================================================

def find_lowest_empty_row(board, col):
    # Returns the row index where a checker will fall, or None if column is full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def place_checker(board, col, symbol):
    row = find_lowest_empty_row(board, col)
    if row is None:
        return None, None  # Column full
    board[row][col] = symbol
    return row, col

def in_bounds(board, r, c):
    return 0 <= r < len(board) and 0 <= c < len(board[0])

def check_win_from(board, start_r, start_c, symbol):
    # Check 4-in-a-row including position (start_r, start_c)
    # Directions: horizontal, vertical, diag down-right, diag up-right
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        # forward
        r, c = start_r + dr, start_c + dc
        while in_bounds(board, r, c) and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        # backward
        r, c = start_r - dr, start_c - dc
        while in_bounds(board, r, c) and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def board_full(move_count, rows, cols):
    return move_count >= rows * cols

def get_valid_column_input(labels):
    # Keep asking until the input is a single letter within labels
    while True:
        user_input = input().strip()
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Please enter a valid column letter:")
            continue
        col_letter = user_input.upper()
        if col_letter not in labels:
            print("Invalid input. Please enter a valid column letter:")
            continue
        return labels.index(col_letter), col_letter

# ============================================================
# Main game loop
# ============================================================

def main():
    validate_config()
    rows, cols = ROWS, COLS
    labels = column_labels(cols)
    players = CHECKERS[:NUM_PLAYERS]

    board = create_board(rows, cols)
    current_player_index = random.randrange(NUM_PLAYERS)
    move_count = 0

    while True:
        clear_screen()
        print_board(board, labels)
        current_symbol = players[current_player_index]
        print(f"Player {current_symbol}, please enter a column:")

        col_index, col_letter = get_valid_column_input(labels)

        # Try to place checker
        row, col = place_checker(board, col_index, current_symbol)
        if row is None:
            # Column full, turn is lost
            print(f"Column {col_letter} is full. Turn lost. Press Enter to continue.")
            input()
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        move_count += 1

        # Check for win
        if check_win_from(board, row, col, current_symbol):
            clear_screen()
            print_board(board, labels)
            print(f"Player {current_symbol} won!")
            break

        # Check for draw
        if board_full(move_count, rows, cols):
            clear_screen()
            print_board(board, labels)
            print("It's a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
