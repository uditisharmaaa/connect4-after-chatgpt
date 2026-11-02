import os
import random

# Global Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
MAX_COLUMNS = 26
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')  # Clear the screen
    print('  ' + '   '.join(chr(ord('A') + i) for i in range(len(board[0]))))
    for row in board:
        print('+---' * len(row) + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * len(board[0]) + '+')

def get_valid_column(prompt, columns):
    while True:
        try:
            input_column = input(prompt).strip().upper()
            if len(input_column) != 1 or not ('A' <= input_column < chr(ord('A') + columns)):
                raise ValueError("Invalid column")
            return input_column
        except ValueError:
            print("Invalid column. Please try again.")

def drop_checker(board, column, checker):
    col_index = ord(column) - ord('A')
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = checker
            return True
    return False

def check_for_win(board, checker):
    # Horizontal check
    for row in board:
        for col in range(COLUMN_COUNT - 3):
            if all(cell == checker for cell in row[col:col + 4]):
                return True

    # Vertical check
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT - 3):
            if all(board[row+i][col] == checker for i in range(4)):
                return True

    # Diagonal (\) check
    for row in range(ROW_COUNT - 3):
        for col in range(COLUMN_COUNT - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True

    # Diagonal (/) check
    for row in range(3, ROW_COUNT):
        for col in range(COLUMN_COUNT - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True

    return False

def check_for_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = create_board(ROW_COUNT, COLUMN_COUNT)
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        column = get_valid_column(f"Player {CHECKERS[current_player]}, please enter a column: ", COLUMN_COUNT)
        if drop_checker(board, column, CHECKERS[current_player]):
            print_board(board)
            if check_for_win(board, CHECKERS[current_player]):
                print(f"Player {CHECKERS[current_player]} won!")
                break
            if check_for_draw(board):
                print("The game is a draw!")
                break
            current_player = (current_player + 1) % PLAYERS
        else:
            print("Column is full, you lost your turn.")

play_game()
