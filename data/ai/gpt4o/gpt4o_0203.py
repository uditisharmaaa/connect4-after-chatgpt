import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:COLUMNS]

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print('  ' + '   '.join(COLUMN_LABELS[:COLUMNS]))
    print('+---' * COLUMNS + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * COLUMNS + '+')

def select_starting_player():
    return random.randint(0, PLAYERS - 1)

def is_valid_input(column_input):
    return column_input in COLUMN_LABELS[:COLUMNS]

def get_lowest_row(board, col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            return row
    return None

def place_checker(board, col, checker):
    row = get_lowest_row(board, col)
    if row is not None:
        board[row][col] = checker
        return True
    return False

def has_winner(board, player_checker):
    # Check horizontal, vertical, and diagonal conditions
    for row in range(ROWS):
        for col in range(COLUMNS):
            if check_horizontal(board, row, col, player_checker) or \
               check_vertical(board, row, col, player_checker) or \
               check_diagonal(board, row, col, player_checker):
                return True
    return False

def check_horizontal(board, row, col, checker):
    if col <= COLUMNS - 4 and all(board[row][col + i] == checker for i in range(4)):
        return True
    return False

def check_vertical(board, row, col, checker):
    if row <= ROWS - 4 and all(board[row + i][col] == checker for i in range(4)):
        return True
    return False

def check_diagonal(board, row, col, checker):
    if col <= COLUMNS - 4 and row <= ROWS - 4 and all(board[row + i][col + i] == checker for i in range(4)):
        return True
    if col >= 3 and row <= ROWS - 4 and all(board[row + i][col - i] == checker for i in range(4)):
        return True
    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    board = create_board()
    current_player = select_starting_player()
    print_board(board)

    while True:
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column:")
        column_input = input().strip().upper()

        if not is_valid_input(column_input):
            print("Invalid input. Try again.")
            continue

        col = COLUMN_LABELS.index(column_input)
        if not place_checker(board, col, checker):
            print("Column is full. Turn lost.")
        else:
            print_board(board)
            if has_winner(board, checker):
                print(f"Player {checker} won!")
                break
            if is_draw(board):
                print("It's a draw!")
                break

        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
