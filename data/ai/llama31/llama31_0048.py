import os
import random
import string

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board with empty cells
board = [[' ' for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

def print_board():
    os.system('clear')
    print('  ' + ' '.join(string.ascii_uppercase[:BOARD_WIDTH]))
    for row in board:
        print('+---' * BOARD_WIDTH + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * BOARD_WIDTH + '+')

def get_player_checker(player):
    return CHECKERS[player - 1]

def is_valid_column(column):
    return 'A' <= column <= chr(65 + BOARD_WIDTH - 1)

def is_valid_input(input_str):
    return input_str.isalpha() and len(input_str) == 1

def get_column_index(column):
    return ord(column.upper()) - 65

def is_column_full(column_index):
    return board[0][column_index]!= ' '

def get_next_available_row(column_index):
    for row in range(BOARD_HEIGHT - 1, -1, -1):
        if board[row][column_index] == ' ':
            return row
    return -1

def place_checker(player, column_index):
    row = get_next_available_row(column_index)
    if row == -1:
        print("Column is full. Please choose another column.")
        return False
    board[row][column_index] = get_player_checker(player)
    return True

def check_win(player):
    checker = get_player_checker(player)
    # Check horizontal
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertical
    for row in range(BOARD_HEIGHT - 3):
        for col in range(BOARD_WIDTH):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_HEIGHT - 3):
        for col in range(BOARD_WIDTH - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_HEIGHT):
        for col in range(BOARD_WIDTH - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def is_draw():
    return all(all(cell!= ' ' for cell in row) for row in board)

def game():
    current_player = random.randint(1, NUM_PLAYERS)
    while True:
        print_board()
        print("Player", get_player_checker(current_player), "turn.")
        while True:
            column = input("Please enter a column (A-{}): ".format(chr(65 + BOARD_WIDTH - 1)))
            if is_valid_input(column) and is_valid_column(column):
                column_index = get_column_index(column)
                if not is_column_full(column_index):
                    if place_checker(current_player, column_index):
                        break
                else:
                    print("Column is full. Please choose another column.")
            else:
                print("Invalid input. Please enter a valid column.")
        if check_win(current_player):
            print_board()
            print("Player", get_player_checker(current_player), "won!")
            break
        elif is_draw():
            print_board()
            print("It's a draw!")
            break
        current_player = (current_player % NUM_PLAYERS) + 1

game()
