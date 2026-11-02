import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board
board = [[' ']*BOARD_COLS for _ in range(BOARD_ROWS)]

# Randomly select the first player
current_player = random.randint(0, NUM_PLAYERS-1)

def print_board():
    os.system('clear')
    print('  ' + ' '.join([chr(65+i) for i in range(BOARD_COLS)]))
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * BOARD_COLS + '+')

def is_valid_input(column):
    return column.isalpha() and len(column) == 1 and ord(column) >= 65 and ord(column) < 65+BOARD_COLS

def is_valid_move(column):
    return board[0][ord(column)-65] == ' '

def make_move(column):
    for row in range(BOARD_ROWS-1, -1, -1):
        if board[row][ord(column)-65] == ' ':
            board[row][ord(column)-65] = CHECKERS[current_player]
            return

def check_win():
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS-3):
            if board[row][col]!= ' ' and board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3]:
                return True

    # Check vertical
    for row in range(BOARD_ROWS-3):
        for col in range(BOARD_COLS):
            if board[row][col]!= ' ' and board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col]:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS-3):
        for col in range(BOARD_COLS-3):
            if board[row][col]!= ' ' and board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3]:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS-3):
            if board[row][col]!= ' ' and board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3]:
                return True

    return False

def check_draw():
    return all([all([cell!= ' ' for cell in row]) for row in board])

while True:
    print_board()
    print("Player", CHECKERS[current_player], "please enter a column:")
    column = input().upper()
    while not is_valid_input(column) or not is_valid_move(column):
        if not is_valid_input(column):
            print("Invalid input. Please enter a letter from A to", chr(64+BOARD_COLS))
        else:
            print("Invalid move. Column is full. Please choose another column.")
        column = input().upper()
    make_move(column)
    if check_win():
        print_board()
        print("Player", CHECKERS[current_player], "won!")
        break
    elif check_draw():
        print_board()
        print("It's a draw!")
        break
    current_player = (current_player + 1) % NUM_PLAYERS
