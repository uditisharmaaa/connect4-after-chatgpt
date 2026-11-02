import os
import random
import string

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty board with the given dimensions"""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Print the current state of the board"""
    os.system('clear')
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---' * NUM_COLS + '+')
        print('|   ' * NUM_COLS + '|')
        print('| ' + ' | '.join(row) + ' |')
        print('|   ' * NUM_COLS + '|')
        print('+---' * NUM_COLS + '+')
    print()

def is_valid_input(column):
    """Check if the input column is valid"""
    return column in string.ascii_uppercase[:NUM_COLS]

def get_valid_input():
    """Get a valid input from the user"""
    while True:
        column = input("Player {}, please enter a column: ".format(CHECKERS[turn % NUM_PLAYERS]))
        if is_valid_input(column):
            return ord(column) - ord('A')

def is_column_full(board, column):
    """Check if the given column is full"""
    return board[0][column]!= ' '

def place_checker(board, column, checker):
    """Place the checker in the given column"""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            return

def check_win(board, checker):
    """Check if the given player has won"""
    # Check horizontal wins
    for row in board:
        for i in range(NUM_COLS - 3):
            if all([cell == checker for cell in row[i:i+4]]):
                return True

    # Check vertical wins
    for col in range(NUM_COLS):
        for i in range(NUM_ROWS - 3):
            if all([board[row][col] == checker for row in range(i, i+4)]):
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if all([board[row+i][col+i] == checker for i in range(4)]):
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all([board[row-i][col+i] == checker for i in range(4)]):
                return True

    return False

def check_draw(board):
    """Check if the game is a draw"""
    return all([all([cell!= ' ' for cell in row]) for row in board])

# Initialize the game
board = create_board()
turn = random.randint(0, NUM_PLAYERS - 1)

# Game loop
while True:
    print_board(board)
    column = get_valid_input()
    if is_column_full(board, column):
        print("Column is full, try again.")
        continue
    place_checker(board, column, CHECKERS[turn % NUM_PLAYERS])
    if check_win(board, CHECKERS[turn % NUM_PLAYERS]):
        print_board(board)
        print("Player {} won!".format(CHECKERS[turn % NUM_PLAYERS]))
        break
    elif check_draw(board):
        print_board(board)
        print("It's a draw!")
        break
    turn += 1
