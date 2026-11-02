import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board
def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')
    print('  ' + ' '.join(chr(65+i) for i in range(COLUMNS)))
    for row in board:
        print('+---' * COLUMNS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLUMNS + '+')

# Validate user input
def validate_input(col):
    if not col.isalpha():
        return False
    col = ord(col) - 65
    if col < 0 or col >= COLUMNS:
        return False
    return True

# Place a checker
def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return

# Check for a win
def check_win(board, checker):
    # Horizontal
    for row in board:
        for i in range(COLUMNS - 3):
            if row[i] == checker and row[i+1] == checker and row[i+2] == checker and row[i+3] == checker:
                return True

    # Vertical
    for col in range(COLUMNS):
        for i in range(ROWS - 3):
            if board[i][col] == checker and board[i+1][col] == checker and board[i+2][col] == checker and board[i+3][col] == checker:
                return True

    # Diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True

    # Diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row-1][col+1] == checker and board[row-2][col+2] == checker and board[row-3][col+3] == checker:
                return True

    return False

# Main game loop
def game():
    board = create_board(ROWS, COLUMNS)
    players = [CHECKERS[i] for i in range(PLAYERS)]
    current_player = random.choice(players)
    while True:
        print_board(board)
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if not validate_input(col):
            print("Invalid input. Please try again.")
            continue
        col = ord(col) - 65
        if board[0][col]!= ' ':
            print("Column is full. Please try again.")
            continue
        place_checker(board, col, current_player)
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        current_player = players[(players.index(current_player) + 1) % PLAYERS]

game()
