import os
import random

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize board
board = [[' ' for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

def print_board():
    os.system('clear')
    print('  A', end='')
    for i in range(1, BOARD_WIDTH):
        print(' B', end='')
    print()
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            print(f'| {board[i][j]}', end='')
        print('|')
        if i < BOARD_HEIGHT - 1:
            print('+---' * BOARD_WIDTH + '+')

def is_valid_input(column):
    if not column.isalpha():
        return False
    if column.lower() not in 'abcdefghijklmnopqrstuvwxyz'[:BOARD_WIDTH]:
        return False
    column_index = ord(column.lower()) - 97
    for i in range(BOARD_HEIGHT - 1, -1, -1):
        if board[i][column_index] == ' ':
            return True
    return False

def drop_checker(column, player):
    column_index = ord(column.lower()) - 97
    for i in range(BOARD_HEIGHT - 1, -1, -1):
        if board[i][column_index] == ' ':
            board[i][column_index] = player
            return

def check_win(player):
    # Check horizontal
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH - 3):
            if board[i][j] == player and board[i][j + 1] == player and board[i][j + 2] == player and board[i][j + 3] == player:
                return True
    # Check vertical
    for i in range(BOARD_HEIGHT - 3):
        for j in range(BOARD_WIDTH):
            if board[i][j] == player and board[i + 1][j] == player and board[i + 2][j] == player and board[i + 3][j] == player:
                return True
    # Check diagonal (top-left to bottom-right)
    for i in range(BOARD_HEIGHT - 3):
        for j in range(BOARD_WIDTH - 3):
            if board[i][j] == player and board[i + 1][j + 1] == player and board[i + 2][j + 2] == player and board[i + 3][j + 3] == player:
                return True
    # Check diagonal (bottom-left to top-right)
    for i in range(3, BOARD_HEIGHT):
        for j in range(BOARD_WIDTH - 3):
            if board[i][j] == player and board[i - 1][j + 1] == player and board[i - 2][j + 2] == player and board[i - 3][j + 3] == player:
                return True
    return False

def check_draw():
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            if board[i][j] == ' ':
                return False
    return True

def game():
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    print_board()
    while True:
        current_player = players[current_player_index]
        print(f'Player {current_player}, please enter a column:')
        column = input().upper()
        while not is_valid_input(column):
            print('Invalid input. Please enter a valid column.')
            column = input().upper()
        drop_checker(column, current_player)
        print_board()
        if check_win(current_player):
            print(f'Player {current_player} won!')
            break
        elif check_draw():
            print('It\'s a draw!')
            break
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

game()
