import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2

def initialize_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')  # Clears the screen
    header = ' '.join(['  ' + chr(65 + i) for i in range(len(board[0]))])
    print(header)
    print('+---' * len(board[0]) + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * len(board[0]) + '+')

def is_valid_input(input_str, cols):
    if len(input_str) != 1:
        return False
    if not ('A' <= input_str <= chr(65 + cols - 1)):
        return False
    return True

def place_checker(board, col, symbol):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = symbol
            return True
    return False

def check_winner(board, symbol):
    # Horizontal check
    for row in board:
        for col in range(len(row) - 3):
            if all([row[col + i] == symbol for i in range(4)]):
                return True
    
    # Vertical check
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if all([board[row + i][col] == symbol for i in range(4)]):
                return True

    # Diagonal checks
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all([board[row + i][col + i] == symbol for i in range(4)]):
                return True
        for col in range(3, len(board[0])):
            if all([board[row + i][col - i] == symbol for i in range(4)]):
                return True

    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = initialize_board(BOARD_ROWS, BOARD_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    while True:
        current_symbol = PLAYER_SYMBOLS[current_player_index]
        print_board(board)
        print(f"Player {current_symbol}, please enter a column:")
        
        while True:
            user_input = input().strip().upper()
            if not is_valid_input(user_input, BOARD_COLS):
                print("Invalid input. Please enter a valid column letter:")
                continue
            
            column_index = ord(user_input) - 65
            if not place_checker(board, column_index, current_symbol):
                print("Column is full. Please choose another column:")
                continue
            
            break
        
        if check_winner(board, current_symbol):
            print_board(board)
            print(f"Player {current_symbol} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
            
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

play_game()
