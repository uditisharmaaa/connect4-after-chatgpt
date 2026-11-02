import os
import random

# Constant variables
BOARD_COLUMNS = 7
BOARD_ROWS = 6
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']
PLAYERS = 2

# Function to create the board
def create_board():
    board = [[' ' for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]
    return board

# Function to print the board
def print_board(board):
    os.system('clear')
    print('  A', 'B', 'C', 'D', 'E', 'F', 'G', sep='   ')
    for i in range(BOARD_ROWS):
        print('+---' * BOARD_COLUMNS + '+')
        print('|', end='')
        for j in range(BOARD_COLUMNS):
            print(' ' + board[i][j] + ' |', end='')
        print()
    print('+---' * BOARD_COLUMNS + '+')

# Function to check for invalid input
def check_input(input_str, board):
    if not input_str.isalpha():
        return False
    input_col = ord(input_str.upper()) - ord('A')
    if input_col < 0 or input_col >= BOARD_COLUMNS:
        return False
    if board[0][input_col]!= ' ':
        return False
    return True

# Function to place the checker at the correct location
def place_checker(board, player, column):
    for i in range(BOARD_ROWS - 1, -1, -1):
        if board[i][column] == ' ':
            board[i][column] = player
            break

# Function to check for a win
def check_win(board, player):
    # Check horizontal
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLUMNS - 3):
            if board[i][j] == player and board[i][j + 1] == player and board[i][j + 2] == player and board[i][j + 3] == player:
                return True

    # Check vertical
    for i in range(BOARD_ROWS - 3):
        for j in range(BOARD_COLUMNS):
            if board[i][j] == player and board[i + 1][j] == player and board[i + 2][j] == player and board[i + 3][j] == player:
                return True

    # Check diagonal
    for i in range(BOARD_ROWS - 3):
        for j in range(BOARD_COLUMNS - 3):
            if board[i][j] == player and board[i + 1][j + 1] == player and board[i + 2][j + 2] == player and board[i + 3][j + 3] == player:
                return True
            if board[i + 3][j] == player and board[i + 2][j + 1] == player and board[i + 1][j + 2] == player and board[i][j + 3] == player:
                return True

    return False

# Function to check for a draw
def check_draw(board):
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLUMNS):
            if board[i][j] == ' ':
                return False
    return True

# Main game loop
def game():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)
    print('Player', current_player, 'will go first.')
    while True:
        print_board(board)
        print('Player', current_player, 'please enter a column:')
        input_str = input().strip()
        if not check_input(input_str, board):
            print('Invalid input. Please enter a valid column.')
            continue
        input_col = ord(input_str.upper()) - ord('A')
        place_checker(board, current_player, input_col)
        if check_win(board, current_player):
            print_board(board)
            print('Player', current_player, 'won!')
            break
        if check_draw(board):
            print_board(board)
            print('It\'s a draw!')
            break
        current_player = players[(players.index(current_player) + 1) % PLAYERS]

# Start the game
game()
