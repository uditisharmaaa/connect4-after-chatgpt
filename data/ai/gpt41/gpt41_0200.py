import os
import random
import string
import sys

# ==============================
# CONSTANTS: (For the assignment, set to 6x7 and 2 players)
BOARD_ROWS = 6
BOARD_COLS = 7   # Must be <= 26 (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5

MAX_COLS = 26

PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_LENGTH = 4

# ==============================
def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    rows = len(board)
    # Column headers A, B, ...
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    sep_line = "+" + "---+" * cols
    print(header)
    print(sep_line)
    for r in range(rows):
        row_str = "| " + " | ".join(board[r]) + " |"
        print(row_str)
        print(sep_line)

def get_valid_columns(board):
    valid_cols = []
    for col in range(len(board[0])):
        if board[0][col] == " ":
            valid_cols.append(col)
    return valid_cols

def get_column_input(board):
    cols = len(board[0])
    col_letters = string.ascii_uppercase[:cols]
    valid_cols = get_valid_columns(board)
    valid_col_letters = [col_letters[c] for c in valid_cols]
    while True:
        user_input = input(f"Please enter a column ({'/'.join(col_letters)}): ").strip().upper()
        if len(user_input) != 1 or user_input not in col_letters:
            print("Invalid input. Try again (must be one of " + "/".join(col_letters) + ").")
            continue
        col_idx = ord(user_input) - ord('A')
        if col_idx not in valid_cols:
            if board[0][col_idx] != " ":
                print("This column is full. You lose your turn.")
                return None
            else:
                # Shouldn't happen
                print("Invalid input. Try again.")
                continue
        return col_idx

def drop_checker(board, col, checker):
    """
    Returns (row, col) of drop or None if column is full (shouldn't happen due to input logic)
    """
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return (row, col)
    return None

def board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0])
    # Horizontal check
    for r in range(rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r][c + i] == symbol for i in range(WIN_LENGTH)):
                return True
    # Vertical check
    for c in range(cols):
        for r in range(rows - WIN_LENGTH + 1):
            if all(board[r + i][c] == symbol for i in range(WIN_LENGTH)):
                return True
    # Diagonal (down-right)
    for r in range(rows - WIN_LENGTH + 1):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == symbol for i in range(WIN_LENGTH)):
                return True
    # Diagonal (up-right)
    for r in range(WIN_LENGTH - 1, rows):
        for c in range(cols - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == symbol for i in range(WIN_LENGTH)):
                return True
    return False

def main():
    board = create_board(BOARD_ROWS, BOARD_COLS)
    col_letters = string.ascii_uppercase[:BOARD_COLS]

    # Randomly select first player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)

    while True:
        checker = PLAYER_SYMBOLS[current_player]
        print(f"Player {checker}, it is your turn.")
        col_idx = None
        while True:
            user_input = input(f"Player {checker}, please enter a column: ").strip().upper()
            if len(user_input) != 1 or user_input not in col_letters:
                print("Invalid input. Try again (must be one of " + "/".join(col_letters) + ").")
                continue
            col_idx = ord(user_input) - ord('A')
            if col_idx < 0 or col_idx >= BOARD_COLS:
                print("Invalid input. Try again.")
                continue
            if board[0][col_idx] != " ":
                print("This column is full. Your turn is skipped!")
                col_idx = None
                break
            break
        if col_idx is None:
            # Turn is lost due to full column
            pass
        else:
            drop_checker(board, col_idx, checker)
        clear_screen()
        print_board(board)
        if col_idx is not None:
            if check_win(board, checker):
                print(f"Player {checker} won!")
                break
        if board_full(board):
            print("It's a draw!")
            break
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
