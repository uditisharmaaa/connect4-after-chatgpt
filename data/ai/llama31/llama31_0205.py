import os
import random
import string

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = 'XOVHM'

# Initialize board
board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board():
    os.system('clear')
    print('  A B C D E F G')
    for row in board:
        print('+---' * COLS + '+')
        print('| {} |'.format(' | '.join(row)))
    print('+---' * COLS + '+')

def get_player_checker(player):
    return CHECKERS[player % len(CHECKERS)]

def is_valid_input(column):
    return column in string.ascii_uppercase[:COLS]

def is_valid_move(column):
    return board[0][ord(column) - ord('A')] == ' '

def get_next_open_row(column):
    for row in reversed(board):
        if row[ord(column) - ord('A')] == ' ':
            return row
    return None

def drop_checker(checker, column):
    row = get_next_open_row(column)
    if row:
        row[ord(column) - ord('A')] = checker
        return True
    return False

def check_win(checker):
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == checker and row[i + 1] == checker and row[i + 2] == checker and row[i + 3] == checker:
                return True

    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col] == checker and board[i + 1][col] == checker and board[i + 2][col] == checker and board[i + 3][col] == checker:
                return True

    # Check diagonal
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True
            if board[row][col + 3] == checker and board[row + 1][col + 2] == checker and board[row + 2][col + 1] == checker and board[row + 3][col] == checker:
                return True

    return False

def check_draw():
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

# Initialize game
current_player = random.randint(0, PLAYERS - 1)

while True:
    print_board()
    checker = get_player_checker(current_player)
    print('Player {}, please enter a column:'.format(checker))
    column = input().upper()
    while not is_valid_input(column) or not is_valid_move(column):
        print('Invalid input, please try again.')
        column = input().upper()

    if drop_checker(checker, column):
        if check_win(checker):
            print_board()
            print('Player {} won!'.format(checker))
            break
        elif check_draw():
            print_board()
            print('It\'s a draw!')
            break
        current_player = (current_player + 1) % PLAYERS
    else:
        print('Column is full, please try again.')
