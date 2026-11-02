import os
import random
import string

# Constants (you can change these for testing, but submit with these values)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

# Player checkers in order
ALL_CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Header with column letters
    letters = string.ascii_uppercase[:cols]
    header = "  " + "   ".join(letters)
    print(header)

    # Separator line
    sep = "+" + ("---+" * cols)

    # Rows (top to bottom)
    for r in range(rows):
        print(sep)
        line = "|"
        for c in range(cols):
            line += " " + board[r][c] + " |"
        print(line)
    print(sep)

def get_column_index(input_str, cols):
    if len(input_str) != 1:
        return -1
    ch = input_str.upper()
    letters = string.ascii_uppercase[:cols]
    if ch in letters:
        return letters.index(ch)
    return -1

def get_valid_input(cols, current_checker):
    while True:
        user_input = input(f"Player {current_checker}, please enter a column: ").strip()
        col_idx = get_column_index(user_input, cols)
        if col_idx == -1:
            print("Invalid input. Please enter a single letter within the board columns.")
            continue
        return col_idx

def drop_checker(board, col_idx, checker):
    rows = len(board)
    # Start from bottom row
    for r in range(rows - 1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return True
    return False  # Column full

def check_direction(board, start_r, start_c, dr, dc, checker):
    rows = len(board)
    cols = len(board[0])
    for i in range(4):
        r = start_r + dr * i
        c = start_c + dc * i
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if board[r][c] != checker:
            return False
    return True

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            # Check right, down, diag down-right, diag down-left
            if check_direction(board, r, c, 0, 1, checker):
                return True
            if check_direction(board, r, c, 1, 0, checker):
                return True
            if check_direction(board, r, c, 1, 1, checker):
                return True
            if check_direction(board, r, c, 1, -1, checker):
                return True
    return False

def board_full(board):
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == " ":
                return False
    return True

def main():
    # Basic validations for constants
    if COLS < 1 or COLS > 26:
        print("Invalid COLS value. Must be between 1 and 26.")
        return
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Invalid NUM_PLAYERS. Must be between 2 and 5.")
        return

    # Prepare players
    checkers = ALL_CHECKERS[:NUM_PLAYERS]

    # Create board
    board = create_board(ROWS, COLS)

    # Randomly select starting player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Show initial empty board
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        current_checker = checkers[current_player_idx]

        # Get a valid column letter (within board)
        col_idx = get_valid_input(COLS, current_checker)

        # Try to drop the checker
        success = drop_checker(board, col_idx, current_checker)

        # Always clear and print updated board before checking outcomes
        clear_screen()
        print_board(board)

        if not success:
            # Column full: turn is invalid and player loses the turn
            col_letter = string.ascii_uppercase[col_idx]
            print(f"Column {col_letter} is full. Turn lost.")
            # Next player's turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if board_full(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
