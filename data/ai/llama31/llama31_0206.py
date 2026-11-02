import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board
board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board():
    os.system('clear')
    print('  A', end='')
    for i in range(1, BOARD_COLS):
        print('   ' + chr(65 + i), end='')
    print()
    print('+---' * BOARD_COLS + '+')
    for row in board:
        print('|', end='')
        for cell in row:
            print('   ' + cell, end='|')
        print()
        print('+---' * BOARD_COLS + '+')

def get_player_checker(player):
    return CHECKERS[player - 1]

def is_valid_input(column):
    if not column.isalpha():
        return False
    if ord(column) < 65 or ord(column) > 64 + BOARD_COLS - 1:
        return False
    column = ord(column) - 65
    for row in reversed(board):
        if row[column] == ' ':
            return True
    return False

def place_checker(column, checker):
    column = ord(column) - 65
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return

def check_win(checker):
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == row[i + 1] == row[i + 2] == row[i + 3] == checker:
                return True

    # Check vertical
    for col in range(BOARD_COLS):
        for i in range(len(board) - 3):
            if board[i][col] == board[i + 1][col] == board[i + 2][col] == board[i + 3][col] == checker:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == checker:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] == checker:
                return True

    return False

def is_draw():
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

# Randomly select the first player
current_player = random.randint(1, PLAYERS)

print_board()
while True:
    print('Player', get_player_checker(current_player), 'please enter a column:')
    column = input().upper()
    while not is_valid_input(column):
        print('Invalid input. Please try again.')
        column = input().upper()
    place_checker(column, get_player_checker(current_player))
    print_board()
    if check_win(get_player_checker(current_player)):
        print('Player', get_player_checker(current_player), 'won!')
        break
    elif is_draw():
        print('It\'s a draw!')
        break
    current_player = (current_player % PLAYERS) + 1
