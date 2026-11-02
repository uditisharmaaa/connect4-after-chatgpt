import os
import random
import sys

# Constants (adjustable)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
TOKENS = ['X', 'O', 'V', 'H', 'M']  # In order

# Validations for constraints
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if not (1 <= COLS <= 26):
    print("COLS must be between 1 and 26.")
    sys.exit(1)
if ROWS < 1:
    print("ROWS must be at least 1.")
    sys.exit(1)

PLAYERS = TOKENS[:NUM_PLAYERS]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_letters(cols):
    return [chr(ord('A') + i) for i in range(cols)]


def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    letters = column_letters(cols)
    # Header
    print("  " + "   ".join(letters))
    # Top border
    print("+" + "+".join(["---"] * cols) + "+")
    # Rows
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + "+".join(["---"] * cols) + "+")


def get_valid_input(cols, current_token):
    letters = column_letters(cols)
    valid_set = set(letters)
    while True:
        user_in = input(f"Player {current_token}, please enter a column: ").strip().upper()
        if len(user_in) != 1 or user_in not in valid_set:
            print("Invalid input. Please enter a valid column letter.")
            continue
        return letters.index(user_in)


def drop_checker(board, col, token):
    # Place from bottom-most empty
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return True
    return False  # Column full


def check_win(board, token):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Horizontal, Vertical, Diagonals
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            # Right
            if c + 3 < cols and all(board[r][c + k] == token for k in range(4)):
                return True
            # Down
            if r + 3 < rows and all(board[r + k][c] == token for k in range(4)):
                return True
            # Down-right
            if r + 3 < rows and c + 3 < cols and all(board[r + k][c + k] == token for k in range(4)):
                return True
            # Down-left
            if r + 3 < rows and c - 3 >= 0 and all(board[r + k][c - k] == token for k in range(4)):
                return True
    return False


def is_draw(board):
    for row in board:
        if " " in row:
            return False
    return True


def main():
    board = create_board(ROWS, COLS)
    current_idx = random.randrange(NUM_PLAYERS)

    while True:
        print_board(board)
        current_token = PLAYERS[current_idx]
        col = get_valid_input(COLS, current_token)

        if not drop_checker(board, col, current_token):
            print(f"Column {chr(ord('A') + col)} is full. Player {current_token} loses the turn.")
            current_idx = (current_idx + 1) % NUM_PLAYERS
            continue

        # After a successful drop, check for win/draw
        if check_win(board, current_token):
            print_board(board)
            print(f"Player {current_token} won!")
            break

        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_idx = (current_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
