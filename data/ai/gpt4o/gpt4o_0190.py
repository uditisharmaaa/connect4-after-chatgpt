import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

# Initialize the board
board = [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board():
    os.system('clear')
    print('  ' + '   '.join([chr(ord('A') + i) for i in range(COLUMNS)]))
    print('+---' * COLUMNS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * COLUMNS + '+')

def is_valid_column(column):
    return len(column) == 1 and column.isalpha() and 'A' <= column <= chr(ord('A') + COLUMNS - 1)

def get_column_index(column):
    return ord(column) - ord('A')

def is_column_full(column_index):
    return board[0][column_index] != ' '

def place_checker(column_index, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column_index] == ' ':
            board[row][column_index] = checker
            return

def check_win(checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3] == checker:
                return True
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] == checker:
                return True
    # Check diagonal (\)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == checker:
                return True
    # Check diagonal (/)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] == checker:
                return True
    return False

def check_draw():
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    current_player = random.randint(0, PLAYERS - 1)
    print_board()
    
    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        while True:
            column = input().strip().upper()
            if not is_valid_column(column):
                print("Invalid column. Try again.")
            else:
                column_index = get_column_index(column)
                if is_column_full(column_index):
                    print("Column full. Turn lost.")
                    break
                place_checker(column_index, CHECKERS[current_player])
                break

        print_board()

        if check_win(CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break

        if check_draw():
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

main()
