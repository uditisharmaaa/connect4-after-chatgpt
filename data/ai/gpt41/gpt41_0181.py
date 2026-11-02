import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_COLS = 26
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Board setup
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def clear_screen():
    os.system('clear')

def print_board(board):
    col_labels = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(col_labels))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_valid_column_input(board, current_checker):
    while True:
        col = input(f"Player {current_checker}, please enter a column: ").strip().upper()
        if len(col) != 1 or not col.isalpha():
            print("Invalid input. Enter a single letter (A to {}).".format(chr(ord('A') + COLS - 1)))
            continue
        col_idx = ord(col) - ord('A')
        if not 0 <= col_idx < COLS:
            print("Column out of range.")
            continue
        # Check if the column is full
        if board[0][col_idx] != ' ':
            print("Column is full. You lose your turn!")
            return None
        return col_idx

def drop_checker(board, col, checker):
    for i in reversed(range(ROWS)):
        if board[i][col] == ' ':
            board[i][col] = checker
            return i, col

def check_winner(board, checker):
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True
    # Vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True
    # Diagonal /
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True
    # Diagonal \
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for cell in board[0])

def main():
    board = create_board()
    player_checkers = CHECKERS[:NUM_PLAYERS]
    current_player = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print("Starting player:", player_checkers[current_player])
    print_board(board)

    while True:
        checker = player_checkers[current_player]
        col_idx = get_valid_column_input(board, checker)
        clear_screen()
        if col_idx is not None:
            row, col = drop_checker(board, col_idx, checker)
            print_board(board)
            if check_winner(board, checker):
                print(f"Player {checker} won!")
                break
            elif is_draw(board):
                print("It's a draw!")
                break
        else:
            print_board(board)
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
