import os
import random

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board
def create_board(width, height):
    return [[' ' for _ in range(width)] for _ in range(height)]

# Print the board
def print_board(board):
    print('  A   B   C   D   E   F   G')
    for row in board:
        print('+---+---+---+---+---+---+---+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---+---+---+---+---+---+---+')

# Validate user input
def validate_input(column):
    if len(column)!= 1:
        return False
    if column.upper() not in 'ABCDEFG':
        return False
    column_index = ord(column.upper()) - ord('A')
    if column_index < 0 or column_index >= BOARD_WIDTH:
        return False
    return True

# Place a checker on the board
def place_checker(board, player, column):
    column_index = ord(column.upper()) - ord('A')
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = CHECKERS[player]
            break

# Check for a win
def check_win(board, player):
    checker = CHECKERS[player]
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if all([cell == checker for cell in row[i:i+4]]):
                return True
    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if all([row[col] == checker for row in board[i:i+4]]):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all([board[row+i][col+i] == checker for i in range(4)]):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all([board[row-i][col+i] == checker for i in range(4)]):
                return True
    return False

# Check for a draw
def check_draw(board):
    return all([all([cell!= ' ' for cell in row]) for row in board])

# Main game loop
def play_game():
    board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    players = list(range(PLAYERS))
    random.shuffle(players)
    current_player = players[0]
    while True:
        os.system('clear')
        print_board(board)
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        column = input().upper()
        if not validate_input(column):
            print("Invalid input. Please try again.")
            continue
        place_checker(board, current_player, column)
        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break
        current_player = (current_player + 1) % PLAYERS

play_game()
