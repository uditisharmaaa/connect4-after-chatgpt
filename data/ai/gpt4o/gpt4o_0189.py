import random
import os

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join([chr(65 + i) for i in range(COLUMNS)]))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print("+" + "---+" * COLUMNS)

def get_valid_column_input(board):
    while True:
        user_input = input(f'Player {current_player}, please enter a column: ').upper()
        if len(user_input) != 1 or not ('A' <= user_input <= chr(65 + COLUMNS - 1)):
            print("Invalid input. Please enter a letter corresponding to a column.")
        else:
            col_index = ord(user_input) - 65
            if board[0][col_index] != ' ':
                print("Column is full. Choose another.")
            else:
                return col_index

def place_checker(board, col_index, checker):
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = checker
            return

def check_winner(board, current_checker):
    # Horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col+i] == current_checker for i in range(4)):
                return True
    
    # Vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == current_checker for i in range(4)):
                return True
    
    # Diagonal (\)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == current_checker for i in range(4)):
                return True
    
    # Diagonal (/)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == current_checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Initialization
board = create_board()
current_player_index = random.randint(0, NUM_PLAYERS - 1)
players = CHECKERS[:NUM_PLAYERS]

while True:
    print_board(board)
    current_player = players[current_player_index]
    
    column = get_valid_column_input(board)
    place_checker(board, column, current_player)

    if check_winner(board, current_player):
        print_board(board)
        print(f"Player {current_player} won!")
        break

    if check_draw(board):
        print_board(board)
        print("It's a draw!")
        break

    current_player_index = (current_player_index + 1) % NUM_PLAYERS
