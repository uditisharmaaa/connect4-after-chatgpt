import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    # Print column headers
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    # Print board rows
    for row in board:
        print('+---' * COLS + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---' * COLS + '+')

def is_valid_column(column):
    if len(column) != 1 or not column.isalpha():
        return False
    col = ord(column.upper()) - ord('A')
    return 0 <= col < COLS

def get_empty_row(board, col):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            return row
    return -1

def place_checker(board, col, symbol):
    row = get_empty_row(board, col)
    if row == -1:
        return False
    board[row][col] = symbol
    return True

def check_win(board, symbol):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col+i] == symbol for i in range(4)):
                return True
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row+i][col] == symbol for i in range(4)):
                return True
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row+i][col+i] == symbol for i in range(4)):
                return True
    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row-i][col+i] == symbol for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = initialize_board()
    current_player = random.randint(0, PLAYERS-1)
    
    while True:
        print_board(board)
        symbol = PLAYER_SYMBOLS[current_player]
        print(f"Player {symbol}, please enter a column: ")
        
        while True:
            column = input().strip().upper()
            if is_valid_column(column):
                col = ord(column) - ord('A')
                if get_empty_row(board, col) != -1:
                    break
                print("Column is full. Try another column: ")
            else:
                print("Invalid input. Please enter a valid column (A-" + chr(65 + COLS - 1) + "): ")
        
        place_checker(board, col, symbol)
        
        if check_win(board, symbol):
            print_board(board)
            print(f"Player {symbol} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
