import os
import random

# Constants (submission requires 6 rows x 7 columns and 2 players)
ROWS = 6
COLS = 7  # Max 26 (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5

CHECKERS = ["X", "O", "V", "H", "M"]  # In order

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Header letters
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(header)
    # Grid
    sep = "+" + ("---+" * cols)
    for r in range(len(board)):
        print(sep)
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print(sep)

def column_label_to_index(label):
    if len(label) != 1:
        return None
    if not label.isalpha() or not label.isupper():
        return None
    idx = ord(label) - ord('A')
    if 0 <= idx < COLS:
        return idx
    return None

def get_next_open_row(board, col):
    # Return the bottom-most empty row index in this column, or None if full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def drop_checker(board, row, col, checker):
    board[row][col] = checker

def is_board_full(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def check_win(board, checker):
    rows = ROWS
    cols = COLS

    # Horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if (board[r][c] == checker and
                board[r][c+1] == checker and
                board[r][c+2] == checker and
                board[r][c+3] == checker):
                return True

    # Vertical
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

def main():
    # Basic validations for constants
    assert 2 <= NUM_PLAYERS <= 5, "NUM_PLAYERS must be between 2 and 5"
    assert 1 <= ROWS and 1 <= COLS <= 26, "ROWS must be >=1 and COLS must be between 1 and 26"

    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select first player
    current_player_index = random.randrange(NUM_PLAYERS)

    # Initial display
    clear_screen()
    print_board(board)
    # Game loop
    while True:
        current_checker = players[current_player_index]
        print(f"Player {current_checker}, please enter a column:")
        user_input = input().strip()

        # Validate input (must be a single uppercase letter within board)
        while True:
            col_idx = column_label_to_index(user_input)
            if col_idx is None:
                print("Invalid input. Please enter a valid column letter (e.g., A, B, C).")
                user_input = input().strip()
                continue
            break

        # Try to place checker
        row_idx = get_next_open_row(board, col_idx)
        if row_idx is None:
            # Column full, player loses the turn
            clear_screen()
            print_board(board)
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue
        else:
            drop_checker(board, row_idx, col_idx, current_checker)

        # After move, clear and print updated board
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
