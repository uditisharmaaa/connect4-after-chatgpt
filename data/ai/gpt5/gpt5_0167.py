import os
import random
import string
import sys

# ==========================
# Constants (change these to test other configurations)
# ==========================
ROWS = 6
COLS = 7          # Max 26
NUM_PLAYERS = 2   # Between 2 and 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_LENGTH = 4
CLEAR_CMD = 'clear'  # Linux/Unix as required

# ==========================
# Validation of constants
# ==========================
def validate_settings():
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if COLS < 1 or COLS > 26:
        print("Error: COLS must be between 1 and 26.")
        sys.exit(1)
    if ROWS < 1:
        print("Error: ROWS must be at least 1.")
        sys.exit(1)

# ==========================
# Utility functions
# ==========================
def clear_screen():
    # As per assignment, use 'clear' (Linux/Unix terminal)
    os.system(CLEAR_CMD)

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def column_labels(cols):
    # Labels A, B, C, ...
    return [string.ascii_uppercase[i] for i in range(cols)]

def print_board(board):
    cols = len(board[0])
    labels = column_labels(cols)
    # Header labels (e.g., "  A   B   C ...")
    header = '  ' + '   '.join(labels)
    print(header)
    # Horizontal line (e.g., "+---+---+...+")
    sep = '+' + ('---+' * cols)
    for r in range(len(board)):
        print(sep)
        row_str = '|'
        for c in range(cols):
            row_str += f' {board[r][c]} |'
        print(row_str)
    print(sep)

def board_full(board):
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def place_checker(board, col_index, checker):
    # Drop from bottom-most row upwards
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == ' ':
            board[r][col_index] = checker
            return r
    return None  # Column full

def in_bounds(board, r, c):
    return 0 <= r < len(board) and 0 <= c < len(board[0])

def count_in_direction(board, start_r, start_c, dr, dc, checker):
    count = 0
    r, c = start_r, start_c
    while in_bounds(board, r, c) and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count

def check_win_from_cell(board, r, c, checker):
    # Check 4 directions: horizontal, vertical, diag down-right, diag down-left
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count_pos = count_in_direction(board, r, c, dr, dc, checker)
        count_neg = count_in_direction(board, r, c, -dr, -dc, checker)
        # We counted the starting cell twice, subtract 1
        if count_pos + count_neg - 1 >= WIN_LENGTH:
            return True
    return False

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == checker:
                if check_win_from_cell(board, r, c, checker):
                    return True
    return False

def prompt_for_column(cols, prompt_text):
    # Keep prompting until user gives a syntactically valid column label within range
    labels = column_labels(cols)
    valid_set = set(labels)
    while True:
        user_input = input(prompt_text).strip()
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter (e.g., A).")
            continue
        letter = user_input.upper()
        if letter not in valid_set:
            print(f"Invalid column. Please choose one of: {', '.join(labels)}")
            continue
        return ord(letter) - ord('A')

def next_player_index(current_index, num_players):
    return (current_index + 1) % num_players

# ==========================
# Game loop
# ==========================
def main():
    validate_settings()
    # Prepare players (X, O, V, H, M in order)
    players = CHECKERS[:NUM_PLAYERS]

    # Initialize board and starting player
    board = create_board(ROWS, COLS)
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Show initial empty board before game starts
    clear_screen()
    print_board(board)

    # Main game loop
    while True:
        current_checker = players[current_player_idx]
        # Prompt current player
        prompt = f"Player {current_checker}, please enter a column: "
        col_index = prompt_for_column(COLS, prompt)

        # Attempt to place checker
        placed_row = place_checker(board, col_index, current_checker)

        # Clear and print board after (attempted) move
        clear_screen()
        print_board(board)

        if placed_row is None:
            # Column full -> invalid turn, player loses turn
            chosen_col_label = string.ascii_uppercase[col_index]
            print(f"Column {chosen_col_label} is full. Turn lost.")
            # Move to next player
            current_player_idx = next_player_index(current_player_idx, NUM_PLAYERS)
            # Continue to next turn
            # Also check for draw in case entire board becomes full
            if board_full(board):
                print("It's a draw!")
                break
            continue

        # Check for a win by the current player
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = next_player_index(current_player_idx, NUM_PLAYERS)

if __name__ == "__main__":
    main()
