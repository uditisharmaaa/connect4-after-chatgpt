import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2

# Initialize the board
board = [[' ']*BOARD_COLS for _ in range(BOARD_ROWS)]

def print_board():
    os.system('clear')
    print('  A   B   C   D   E   F   G')
    for row in range(BOARD_ROWS):
        print('+---+---+---+---+---+---+---+')
        print('|', end='')
        for col in range(BOARD_COLS):
            print(' ' + board[row][col] + ' |', end='')
        print()
    print('+---+---+---+---+---+---+---+')

def get_player_checker(player_num):
    return CHECKERS[player_num - 1]

def get_valid_move(player_num):
    while True:
        move = input(f"Player {get_player_checker(player_num)}, please enter a column: ").upper()
        if move < 'A' or move > 'G':
            print("Invalid input. Please enter a column between A and G.")
        elif move not in 'ABCDEFG':
            print("Invalid input. Please enter a letter between A and G.")
        else:
            col = ord(move) - ord('A')
            for row in range(BOARD_ROWS-1, -1, -1):
                if board[row][col] == ' ':
                    board[row][col] = get_player_checker(player_num)
                    return

def check_win(player_num):
    checker = get_player_checker(player_num)
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS-3):
            if board[row][col] == checker and board[row][col+1] == checker and board[row][col+2] == checker and board[row][col+3] == checker:
                return True
    # Check vertical
    for row in range(BOARD_ROWS-3):
        for col in range(BOARD_COLS):
            if board[row][col] == checker and board[row+1][col] == checker and board[row+2][col] == checker and board[row+3][col] == checker:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS-3):
        for col in range(BOARD_COLS-3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS-3):
            if board[row][col] == checker and board[row-1][col+1] == checker and board[row-2][col+2] == checker and board[row-3][col+3] == checker:
                return True
    return False

def check_draw():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == ' ':
                return False
    return True

# Randomly select the first player
current_player = random.randint(1, NUM_PLAYERS)

print_board()

while True:
    print_board()
    get_valid_move(current_player)
    if check_win(current_player):
        print_board()
        print(f"Player {get_player_checker(current_player)} won!")
        break
    elif check_draw():
        print_board()
        print("It's a draw!")
        break
    current_player = (current_player % NUM_PLAYERS) + 1
