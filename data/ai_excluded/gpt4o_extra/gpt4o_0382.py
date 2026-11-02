import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    header = '  ' + '   '.join(chr(ord('A') + i) for i in range(COLUMNS))
    print(header)
    print('+---' * COLUMNS + '+')
    for row in board:
        print('|' + '|'.join(f' {col} ' for col in row) + '|')
        print('+---' * COLUMNS + '+')

def is_valid_column(column, board):
    if column < 0 or column >= COLUMNS:
        return False
    return board[0][column] == ' '

def get_column_input():
    while True:
        try:
            input_val = input("Please enter a column: ").strip().upper()
            index = ord(input_val) - ord('A')
            if index >= 0 and index < COLUMNS:
                return index
        except:
            pass
        print("Invalid input, please try again.")

def place_checker(column, symbol, board):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = symbol
            return

def check_winner(board, symbol):
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if all(row[col+i] == symbol for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == symbol for i in range(4)):
                return True

    # Check diagonal /
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == symbol for i in range(4)):
                return True

    # Check diagonal \
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == symbol for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def game():
    board = create_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, PLAYERS - 1)

    while True:
        print_board(board)
        current_symbol = PLAYER_SYMBOLS[current_player_index]
        print(f"Player {current_symbol}'s turn.")
        
        column_index = get_column_input()
        
        if not is_valid_column(column_index, board):
            print("Column full or invalid, lose turn.")
        else:
            place_checker(column_index, current_symbol, board)

            if check_winner(board, current_symbol):
                print_board(board)
                print(f"Player {current_symbol} won!")
                break

            if check_draw(board):
                print_board(board)
                print("Game is a draw!")
                break

            current_player_index = (current_player_index + 1) % PLAYERS

game()
