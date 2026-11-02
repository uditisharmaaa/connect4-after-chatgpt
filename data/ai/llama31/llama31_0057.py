import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board
board = [[' ']*COLS for _ in range(ROWS)]

def print_board():
    os.system('clear')
    print('  A', end='')
    for col in range(1, COLS):
        print('  {}'.format(chr(ord('A') + col)), end='')
    print('\n+---' + '+---'*COLS)
    for row in range(ROWS):
        print('|', end='')
        for col in range(COLS):
            print('  {}  |'.format(board[row][col]), end='')
        print('\n+---' + '+---'*COLS)

def is_valid_input(col):
    if col < 'A' or col > chr(ord('A') + COLS - 1):
        return False
    col_index = ord(col) - ord('A')
    return board[0][col_index] == ' '

def get_player_checker(player):
    return CHECKERS[player]

def drop_checker(player, col):
    col_index = ord(col) - ord('A')
    for row in range(ROWS-1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = get_player_checker(player)
            return

def check_win(player):
    checker = get_player_checker(player)
    # Check horizontal locations for win
    for row in range(ROWS):
        for col in range(COLS-3):
            if board[row][col] == checker and board[row][col+1] == checker and board[row][col+2] == checker and board[row][col+3] == checker:
                return True
    # Check vertical locations for win
    for col in range(COLS):
        for row in range(ROWS-3):
            if board[row][col] == checker and board[row+1][col] == checker and board[row+2][col] == checker and board[row+3][col] == checker:
                return True
    # Check positively sloped diagonals
    for row in range(ROWS-3):
        for col in range(COLS-3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True
    # Check negatively sloped diagonals
    for row in range(3, ROWS):
        for col in range(COLS-3):
            if board[row][col] == checker and board[row-1][col+1] == checker and board[row-2][col+2] == checker and board[row-3][col+3] == checker:
                return True
    return False

def is_draw():
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == ' ':
                return False
    return True

def play_game():
    current_player = random.randint(0, PLAYERS-1)
    while True:
        print_board()
        col = input("Player {}, please enter a column: ".format(get_player_checker(current_player))).upper()
        if not is_valid_input(col):
            print("Invalid input, please try again.")
            continue
        drop_checker(current_player, col)
        if check_win(current_player):
            print_board()
            print("Player {} won!".format(get_player_checker(current_player)))
            break
        elif is_draw():
            print_board()
            print("It's a draw!")
            break
        current_player = (current_player + 1) % PLAYERS

play_game()
