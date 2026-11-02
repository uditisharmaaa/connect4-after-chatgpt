import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2 
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    column_labels = '  '.join([chr(i) for i in range(ord('A'), ord('A') + COLUMNS)])
    print(f"  {column_labels}")
    print('+---' * COLUMNS + '+')
    for row in board:
        print('|' + '|'.join(f" {cell} " for cell in row) + '|')
        print('+---' * COLUMNS + '+')

def get_valid_column():
    while True:
        column_input = input("Please enter a column: ").strip().upper()
        if len(column_input) == 1 and ord('A') <= ord(column_input) <= ord('A') + COLUMNS - 1:
            column_index = ord(column_input) - ord('A')
            if board[0][column_index] == ' ':
                return column_index
            else:
                print("Column is full. Try a different one.")
        else:
            print("Invalid input. Enter a letter corresponding to a column.")

def place_checker(board, column_index, player_checker):
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = player_checker
            break

def check_for_winner(board, player_checker):
    # Check horizontally
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col:col + 4] == [player_checker] * 4:
                return True

    # Check vertically
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[r][col] == player_checker for r in range(row, row + 4)):
                return True

    # Check diagonally (\ direction)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player_checker for i in range(4)):
                return True

    # Check diagonally (/ direction)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player_checker for i in range(4)):
                return True

    return False

def check_for_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Initialize the game
board = initialize_board()
current_player_index = random.randint(0, PLAYERS - 1)

print_board(board)

while True:
    current_player_checker = CHECKERS[current_player_index]
    print(f"Player {current_player_checker}, it's your turn.")
    
    column_index = get_valid_column()
    place_checker(board, column_index, current_player_checker)
    print_board(board)

    if check_for_winner(board, current_player_checker):
        print(f"Player {current_player_checker} won!")
        break

    if check_for_draw(board):
        print("It's a draw!")
        break

    current_player_index = (current_player_index + 1) % PLAYERS
