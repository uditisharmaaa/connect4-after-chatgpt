import os
import random

ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    header = '  '.join(ALPHABET[:len(board[0])])
    print("  " + header)
    print('+---' * len(board[0]) + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * len(row) + '+')

def get_valid_column(board):
    while True:
        column_letter = input(f"Player {CHECKERS[current_player]}, please enter a column: ").upper()
        if column_letter in ALPHABET[:len(board[0])]:
            column_index = ALPHABET.index(column_letter)
            if board[0][column_index] == ' ':
                return column_index
            else:
                print("Column is full!")
        else:
            print("Invalid input!")

def place_checker(board, column_index, checker):
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = checker
            break

def check_win(board, checker):
    for row in range(ROWS):
        for col in range(COLUMNS):
            if check_line(board, row, col, checker, 1, 0) or \
               check_line(board, row, col, checker, 0, 1) or \
               check_line(board, row, col, checker, 1, 1) or \
               check_line(board, row, col, checker, 1, -1):
                return True
    return False

def check_line(board, r, c, checker, dr, dc):
    for i in range(4):
        if not (0 <= r + dr*i < ROWS and 0 <= c + dc*i < COLUMNS) or board[r + dr*i][c + dc*i] != checker:
            return False
    return True

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

board = create_board(ROWS, COLUMNS)
current_player = random.randint(0, MAX_PLAYERS - 1)
print_board(board)

while True:
    column_index = get_valid_column(board)
    place_checker(board, column_index, CHECKERS[current_player])
    print_board(board)
    
    if check_win(board, CHECKERS[current_player]):
        print(f"Player {CHECKERS[current_player]} won!")
        break
    if check_draw(board):
        print("The game is a draw!")
        break

    current_player = (current_player + 1) % MAX_PLAYERS
