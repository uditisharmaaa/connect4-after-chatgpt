import os
import random
import string
import sys

# -----------------------------
# Configuration (adjustable)
# -----------------------------
ROWS = 6            # number of rows (height)
COLS = 7            # number of columns (width) - max 26
NUM_PLAYERS = 2     # between 2 and 5

# Checker symbols in order
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4      # number in a row required to win (fixed at 4 per assignment)

# -----------------------------
# Validation of configuration
# -----------------------------
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if COLS < 1 or COLS > 26:
    print("COLS must be between 1 and 26.")
    sys.exit(1)

if ROWS < 1:
    print("ROWS must be at least 1.")
    sys.exit(1)

# -----------------------------
# Board utilities
# -----------------------------
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    # Per assignment: use 'clear' for Linux/Unix
    os.system('clear')

def column_labels(n):
    # Labels A, B, C, ... up to n columns
    return list(string.ascii_uppercase[:n])

def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if board else 0
    labels = column_labels(cols)

    # Header with column letters
    print("  " + "   ".join(labels))
    # Top border
    print("+" + "---+" * cols)

    # Rows
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + "---+" * cols)

def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def find_row_for_col(board, col_index):
    # Return the lowest available row index in the given column, or None if full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == " ":
            return r
    return None

def place_checker(board, col_index, checker):
    r = find_row_for_col(board, col_index)
    if r is None:
        return None
    board[r][col_index] = checker
    return r

# -----------------------------
# Input handling
# -----------------------------
def get_valid_column_input(player_checker, num_cols):
    labels = column_labels(num_cols)
    valid_set = set(labels)

    while True:
        try:
            user_in = input(f"Player {player_checker}, please enter a column: ").strip()
        except EOFError:
            # In case of unexpected EOF, treat as invalid and continue
            continue

        if len(user_in) != 1 or not user_in.isalpha():
            print("Invalid input. Please enter a single letter corresponding to a column.")
            continue

        letter = user_in.upper()
        if letter not in valid_set:
            print(f"Invalid column. Please enter a letter between {labels[0]} and {labels[-1]}.")
            continue

        return labels.index(letter)

# -----------------------------
# Win checking
# -----------------------------
def in_bounds(rows, cols, r, c):
    return 0 <= r < rows and 0 <= c < cols

def count_in_direction(board, start_r, start_c, dr, dc, checker):
    rows = len(board)
    cols = len(board[0])
    r, c = start_r + dr, start_c + dc
    count = 0
    while in_bounds(rows, cols, r, c) and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count

def check_winner(board, last_r, last_c, checker):
    # Check all four principal directions: horizontal, vertical, two diagonals
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]
    for dr, dc in directions:
        total = 1  # include the last placed checker
        total += count_in_direction(board, last_r, last_c, dr, dc, checker)
        total += count_in_direction(board, last_r, last_c, -dr, -dc, checker)
        if total >= WIN_LENGTH:
            return True
    return False

# -----------------------------
# Game loop
# -----------------------------
def play_game(rows, cols, num_players):
    board = create_board(rows, cols)
    players = CHECKERS[:num_players]

    # Randomly select first player
    current_index = random.randrange(num_players)

    # Show initial board
    print_board(board)

    # Main loop
    while True:
        current_checker = players[current_index]

        # Get a valid column letter
        col_index = get_valid_column_input(current_checker, cols)

        # Try to place the checker
        row_index = place_checker(board, col_index, current_checker)

        if row_index is None:
            # Column full -> turn is invalid and player loses the turn
            print_board(board)
            labels = column_labels(cols)
            print(f"Column {labels[col_index]} is full. Player {current_checker} loses the turn.")
            # Advance to next player
            current_index = (current_index + 1) % num_players
            continue

        # Successfully placed -> print updated board
        print_board(board)

        # Check for a win
        if check_winner(board, row_index, col_index, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for a draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_index = (current_index + 1) % num_players

def main():
    play_game(ROWS, COLS, NUM_PLAYERS)

if __name__ == "__main__":
    main()
