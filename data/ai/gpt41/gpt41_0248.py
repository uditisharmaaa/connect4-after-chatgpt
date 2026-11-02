import os
import random
import string
import sys

# ----------- Global Constants -----------
NUM_ROWS = 6                  # Number of rows
NUM_COLS = 7                  # Number of columns (max 26 for column letters)
PLAYER_CHECKERS = ["X", "O"]  # List for 2 players; extend for more players
NUM_PLAYERS = len(PLAYER_CHECKERS)

EMPTY_CELL = " "
WIN_COUNT = 4

# ----------- Board Functions -----------

def create_board(rows, cols):
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear' if os.name == 'posix' else 'cls')
    col_labels = [string.ascii_uppercase[i] for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

# ----------- Game Logic Functions -----------

def is_column_full(board, col):
    return board[0][col] != EMPTY_CELL

def find_next_open_row(board, col):
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == EMPTY_CELL:
            return row
    return None

def place_checker(board, col, checker):
    row = find_next_open_row(board, col)
    if row is not None:
        board[row][col] = checker
        return row
    else:
        return None

def input_to_col(input_str, num_cols):
    if len(input_str) != 1:
        return None
    if input_str not in string.ascii_uppercase[:num_cols]:
        return None
    return string.ascii_uppercase.index(input_str)

def is_board_full(board):
    return all(board[0][c] != EMPTY_CELL for c in range(len(board[0])))

def check_for_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Horizontal check
    for r in range(rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r][c+i] == checker for i in range(WIN_COUNT)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - WIN_COUNT + 1):
            if all(board[r+i][c] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal (top-left to bottom-right) check
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r+i][c+i] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal (bottom-left to top-right) check
    for r in range(WIN_COUNT-1, rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r-i][c+i] == checker for i in range(WIN_COUNT)):
                return True

    return False

def get_valid_input(board):
    num_cols = len(board[0])
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        if user_input == "EXIT":
            print("Exiting game.")
            sys.exit(0)
        col = input_to_col(user_input, num_cols)
        if col is None:
            print(f"Invalid input. Please enter a letter (A-{string.ascii_uppercase[num_cols-1]}).")
            continue
        if is_column_full(board, col):
            print("This column is full. You lose your turn.")
            return None  # Lose turn
        return col

# ----------- Main Game Loop -----------

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player = random.randint(0, NUM_PLAYERS-1)
    print_board(board)
    print(f"Player {PLAYER_CHECKERS[current_player]} will start!\n")

    move_count = 0
    while True:
        print_board(board)
        print(f"Player {PLAYER_CHECKERS[current_player]}, ", end='')
        col = get_valid_input(board)
        if col is None:
            # Lose turn, next player's turn
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        row = place_checker(board, col, PLAYER_CHECKERS[current_player])
        move_count += 1
        if check_for_win(board, PLAYER_CHECKERS[current_player]):
            print_board(board)
            print(f"Player {PLAYER_CHECKERS[current_player]} won!")
            break
        if is_board_full(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
