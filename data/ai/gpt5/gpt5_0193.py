import os
import random
import string

# Constants (adjustable)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Column labels
    labels = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(labels)
    # Horizontal line
    line = "+" + ("---+" * cols)
    for r in range(rows):
        print(line)
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print(line)

def get_valid_input(cols, current_checker):
    while True:
        try:
            user_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            # Treat as invalid input and continue prompting
            print("Invalid input. Please enter a valid column letter.")
            continue

        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        if user_input < 'A' or user_input >= chr(ord('A') + cols):
            print("Invalid column. Please enter a letter within the board range.")
            continue
        return ord(user_input) - ord('A')

def drop_checker(board, col, checker):
    rows = len(board)
    # Start from bottom row upwards
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return None  # Column is full

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - 3):
            if (board[r][c] == checker and
                board[r][c+1] == checker and
                board[r][c+2] == checker and
                board[r][c+3] == checker):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - 3):
            if (board[r][c] == checker and
                board[r+1][c] == checker and
                board[r+2][c] == checker and
                board[r+3][c] == checker):
                return True

    # Diagonal down-right
    for r in range(rows - 3):
        for c in range(cols - 3):
            if (board[r][c] == checker and
                board[r+1][c+1] == checker and
                board[r+2][c+2] == checker and
                board[r+3][c+3] == checker):
                return True

    # Diagonal up-right
    for r in range(3, rows):
        for c in range(cols - 3):
            if (board[r][c] == checker and
                board[r-1][c+1] == checker and
                board[r-2][c+2] == checker and
                board[r-3][c+3] == checker):
                return True

    return False

def check_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    # Basic validations for constants
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        return
    if not (1 <= COLS <= 26):
        print("COLS must be between 1 and 26.")
        return
    if ROWS < 1:
        print("ROWS must be at least 1.")
        return

    players = CHECKERS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    # Randomly select first player
    current_index = random.randint(0, NUM_PLAYERS - 1)

    # Initial board print
    clear_screen()
    print_board(board)

    while True:
        current_checker = players[current_index]
        col = get_valid_input(COLS, current_checker)

        row_placed = drop_checker(board, col, current_checker)

        clear_screen()
        print_board(board)

        if row_placed is None:
            print("Column is full. Turn lost.")
        else:
            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                break
            if check_draw(board):
                print("It's a draw!")
                break

        # Next player's turn
        current_index = (current_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
