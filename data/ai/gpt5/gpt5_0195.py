import os
import random
import string
import sys

# -------------------- Configuration (adjustable) --------------------
ROWS = 6                  # Number of rows (height)
COLS = 7                  # Number of columns (width), max 26
NUM_PLAYERS = 2           # Between 2 and 5 inclusive
WIN_COUNT = 4             # Number of checkers in a row to win (always 4)
CHECKER_ORDER = ["X", "O", "V", "H", "M"]  # In order for players 1..5
# -------------------------------------------------------------------

def clear_screen():
    os.system('clear')

def validate_config():
    if not (2 <= NUM_PLAYERS <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    if not (1 <= COLS <= 26):
        raise ValueError("COLS must be between 1 and 26 (max 26).")
    if ROWS < 1:
        raise ValueError("ROWS must be at least 1.")

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def column_labels(cols):
    return [string.ascii_uppercase[i] for i in range(cols)]

def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    labels = column_labels(cols)
    # Header with column labels
    header = "  " + "   ".join(labels)
    print(header)

    # Horizontal separator line for the grid
    sep = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)

def get_valid_column_input(cols):
    labels = column_labels(cols)
    valid_set = set(labels)
    while True:
        user_in = input("Player, please enter a column: ").strip().upper()
        if len(user_in) != 1 or user_in not in valid_set:
            print(f"Invalid input. Please enter a single letter between A and {labels[-1]}.")
            continue
        return labels.index(user_in)

def drop_checker(board, col, checker):
    # Place the checker in the lowest available row in the given column.
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return None  # Column full

def count_in_direction(board, start_r, start_c, dr, dc, checker):
    rows = len(board)
    cols = len(board[0])
    r, c = start_r + dr, start_c + dc
    count = 0
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count

def is_winning_move(board, row, col, checker):
    # Check four directions: horizontal, vertical, diag down-right, diag up-right
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        total = 1  # include the placed checker
        total += count_in_direction(board, row, col, dr, dc, checker)
        total += count_in_direction(board, row, col, -dr, -dc, checker)
        if total >= WIN_COUNT:
            return True
    return False

def is_draw(board):
    # Draw if no empty spaces remain
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    validate_config()
    players = CHECKER_ORDER[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    # Choose random starting player
    current_idx = random.randrange(NUM_PLAYERS)

    # Initial print before game starts
    print_board(board)
    print(f"Player {players[current_idx]}, please enter a column:")

    while True:
        # Before each turn, check for draw (in case board is filled)
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Prompt input (validated)
        col = get_valid_column_input(COLS)

        current_checker = players[current_idx]
        placed_row = drop_checker(board, col, current_checker)

        if placed_row is None:
            # Column full, turn is invalid and player loses the turn
            print_board(board)
            col_label = column_labels(COLS)[col]
            print(f"Column {col_label} is full. Player {current_checker} loses the turn.")
            # Next player's turn
            current_idx = (current_idx + 1) % NUM_PLAYERS
            print(f"Player {players[current_idx]}, please enter a column:")
            continue

        # After a successful placement: print, check win/draw
        print_board(board)

        if is_winning_move(board, placed_row, col, current_checker):
            print(f"Player {current_checker} won!")
            break

        if is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS
        print(f"Player {players[current_idx]}, please enter a column:")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
