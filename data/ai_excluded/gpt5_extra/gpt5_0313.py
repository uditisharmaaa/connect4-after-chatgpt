import os
import random

# Constants (you can change these for testing; submission must be ROWS=6, COLS=7, NUM_PLAYERS=2)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_LENGTH = 4

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    os.system('clear')

def print_board(board):
    clear_screen()
    cols = len(board[0])
    # Header with letters
    letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(letters))
    # Board body
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(len(board)):
        print(sep)
        row_cells = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row_cells)
    print(sep)

def get_valid_column_input(max_cols, player_checker):
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Please enter a single letter.")
            continue
        col_index = ord(user_input) - ord('A')
        if col_index < 0 or col_index >= max_cols:
            print("Invalid column. Please enter a valid column letter on the board.")
            continue
        return col_index, user_input

def drop_checker(board, col, checker):
    # Place checker in the lowest available row in the column
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False  # Column full

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    n = WIN_LENGTH

    # Horizontal
    for r in range(rows):
        for c in range(cols - n + 1):
            if all(board[r][c + k] == checker for k in range(n)):
                return True

    # Vertical
    for c in range(cols):
        for r in range(rows - n + 1):
            if all(board[r + k][c] == checker for k in range(n)):
                return True

    # Diagonal down-right
    for r in range(rows - n + 1):
        for c in range(cols - n + 1):
            if all(board[r + k][c + k] == checker for k in range(n)):
                return True

    # Diagonal up-right
    for r in range(n - 1, rows):
        for c in range(cols - n + 1):
            if all(board[r - k][c + k] == checker for k in range(n)):
                return True

    return False

def check_draw(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def main():
    # Basic validations for settings
    if COLS < 1 or COLS > 26:
        print("Error: COLS must be between 1 and 26.")
        return
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        return

    board = create_board(ROWS, COLS)

    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Print starting board
    print_board(board)

    while True:
        checker = CHECKERS[current_player_index]
        col_index, col_letter = get_valid_column_input(COLS, checker)

        placed = drop_checker(board, col_index, checker)
        if not placed:
            # Turn is invalid and lost if column is full
            print_board(board)
            print(f"Column {col_letter} is full. Player {checker} loses the turn.")
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        print_board(board)

        if check_win(board, checker):
            print(f"Player {checker} won!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
