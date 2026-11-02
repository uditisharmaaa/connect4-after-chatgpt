import os
import random

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board
board = [[' ' for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

# Function to print the board
def print_board():
    os.system('clear')
    print('  A   B   C   D   E   F   G')
    print('+---+---+---+---+---+---+---+')
    for row in board:
        print('| {} | {} | {} | {} | {} | {} | {} |'.format(*row))
        print('+---+---+---+---+---+---+---+')

# Function to validate user input
def validate_input(player, column):
    if not column.isalpha():
        print('Invalid input. Please enter a letter.')
        return False
    if column.upper() not in 'ABCDEFG':
        print('Invalid input. Please enter a letter between A and G.')
        return False
    column_index = ord(column.upper()) - ord('A')
    if board[0][column_index]!= ' ':
        print('Invalid input. Column is full.')
        return False
    return True

# Function to place a checker
def place_checker(player, column):
    column_index = ord(column.upper()) - ord('A')
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = player
            return

# Function to check for a win
def check_win(player):
    # Check horizontal
    for row in board:
        for i in range(BOARD_WIDTH - 3):
            if row[i] == player and row[i+1] == player and row[i+2] == player and row[i+3] == player:
                return True
    # Check vertical
    for col in range(BOARD_WIDTH):
        for i in range(BOARD_HEIGHT - 3):
            if board[i][col] == player and board[i+1][col] == player and board[i+2][col] == player and board[i+3][col] == player:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_HEIGHT - 3):
        for col in range(BOARD_WIDTH - 3):
            if board[row][col] == player and board[row+1][col+1] == player and board[row+2][col+2] == player and board[row+3][col+3] == player:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_HEIGHT):
        for col in range(BOARD_WIDTH - 3):
            if board[row][col] == player and board[row-1][col+1] == player and board[row-2][col+2] == player and board[row-3][col+3] == player:
                return True
    return False

# Function to check for a draw
def check_draw():
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

# Main game loop
num_players = 2
players = CHECKERS[:num_players]
current_player_index = random.randint(0, num_players - 1)
print_board()

while True:
    current_player = players[current_player_index]
    print('Player {}, please enter a column:'.format(current_player))
    column = input().upper()
    while not validate_input(current_player, column):
        column = input().upper()
    place_checker(current_player, column)
    print_board()
    if check_win(current_player):
        print('Player {} won!'.format(current_player))
        break
    if check_draw():
        print('It\'s a draw!')
        break
    current_player_index = (current_player_index + 1) % num_players
