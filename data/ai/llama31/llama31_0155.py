import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Create the board
def create_board():
    board = [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board

# Print the board
def print_board(board, current_player):
    os.system('clear')
    print('  A', end='')
    for i in range(1, COLUMNS):
        print('   ' + chr(ord('A') + i), end='')
    print('\n' + '+' + '---+' * COLUMNS)
    for row in board:
        print('|', end='')
        for cell in row:
            print('   ' + cell + ' |', end='')
        print('\n' + '+' + '---+' * COLUMNS)
    print('Player', CHECKERS[current_player - 1], ', please enter a column:')

# Validate user input
def validate_input(column):
    if len(column)!= 1:
        return False
    if not column.isalpha():
        return False
    if ord(column) < ord('A') or ord(column) > ord('A') + COLUMNS - 1:
        return False
    return True

# Place checker
def place_checker(board, column, player):
    column_index = ord(column) - ord('A')
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = CHECKERS[player - 1]
            return True
    return False

# Check for win
def check_win(board, player):
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == row[i + 1] == row[i + 2] == row[i + 3] == CHECKERS[player - 1]:
                return True
    # Check vertical
    for col in range(COLUMNS):
        for i in range(len(board) - 3):
            if board[i][col] == board[i + 1][col] == board[i + 2][col] == board[i + 3][col] == CHECKERS[player - 1]:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == CHECKERS[player - 1]:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] == CHECKERS[player - 1]:
                return True
    return False

# Check for draw
def check_draw(board):
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

# Main game loop
def game():
    board = create_board()
    current_player = random.randint(1, PLAYERS)
    while True:
        print_board(board, current_player)
        column = input().upper()
        while not validate_input(column):
            print('Invalid input. Please try again.')
            column = input().upper()
        if not place_checker(board, column, current_player):
            print('Column is full. Please try again.')
            continue
        if check_win(board, current_player):
            print_board(board, current_player)
            print('Player', CHECKERS[current_player - 1], 'won!')
            break
        if check_draw(board):
            print_board(board, current_player)
            print('It\'s a draw!')
            break
        current_player = (current_player % PLAYERS) + 1

game()
