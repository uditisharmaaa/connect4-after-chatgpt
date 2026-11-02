import os
import random
import string

# Constants
ROW_COUNT = 6
COL_COUNT = 7
MAX_COLS = 26
PLAYER_MARKS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2  # set to between 2-5

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    header = '  ' + '   '.join(string.ascii_uppercase[:cols])
    print(header)
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)

def is_valid_input(column, board):
    if len(column) != 1:
        return False
    if column not in string.ascii_uppercase[:len(board[0])]:
        return False
    col_idx = string.ascii_uppercase.index(column)
    return board[0][col_idx] == " "

def get_next_open_row(board, col_idx):
    for r in reversed(range(len(board))):
        if board[r][col_idx] == " ":
            return r
    return None

def drop_checker(board, row, col_idx, checker):
    board[row][col_idx] = checker

def board_full(board):
    return all(board[0][c] != " " for c in range(len(board[0])))

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Vertical check
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Diagonal (\) check
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Diagonal (/) check
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True
    return False

def main():
    board = create_board(ROW_COUNT, COL_COUNT)
    player_markers = PLAYER_MARKS[:NUM_PLAYERS]
    player_names = [f"Player {m}" for m in player_markers]
    current_player = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print_board(board)

    while True:
        marker = player_markers[current_player]
        name = player_names[current_player]
        print(f"{name} ({marker}), please enter a column:")

        column = input().strip().upper()
        if not is_valid_input(column, board):
            print("Invalid input. Try again.")
            continue

        col_idx = string.ascii_uppercase.index(column)
        row = get_next_open_row(board, col_idx)
        # Full column: turn is lost
        if row is None:
            print("Column is full! You lose your turn.")
        else:
            drop_checker(board, row, col_idx, marker)
            clear_screen()
            print_board(board)
            if check_win(board, marker):
                print(f"{name} won!")
                break
            if board_full(board):
                print("The game is a draw!")
                break

        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
