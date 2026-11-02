import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    # Print column headers
    header = '  ' + '   '.join(chr(65 + i) for i in range(COLS)) + '  '
    print(header)
    
    # Print each row
    for row in board:
        print('+---+' * COLS)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    
    print('+---+' * COLS)

def is_valid_column(col):
    if len(col) != 1:
        return False
    return 'A' <= col <= chr(65 + COLS - 1)

def get_column_index(col):
    return ord(col.upper()) - ord('A')

def drop_checker(board, col, checker):
    col_index = get_column_index(col)
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row][col+1] == checker and board[row][col+2] == checker and board[row][col+3] == checker:
                return True

    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if board[row][col] == checker and board[row+1][col] == checker and board[row+2][col] == checker and board[row+3][col] == checker:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True

    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if board[row][col] == checker and board[row+1][col-1] == checker and board[row+2][col-2] == checker and board[row+3][col-3] == checker:
                return True

    return False

def is_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def play_game():
    board = initialize_board()
    current_player = random.choice(range(NUM_PLAYERS))
    
    while True:
        print_board(board)
        print(f"Player {PLAYERS[current_player]}, please enter a column: ")
        col = input().strip().upper()
        
        if not is_valid_column(col):
            print("Invalid column. Please enter a letter from A to", chr(65 + COLS - 1))
            continue
        
        if not drop_checker(board, col, PLAYERS[current_player]):
            print("Column is full. Try another column.")
            continue
        
        if check_win(board, PLAYERS[current_player]):
            print_board(board)
            print(f"Player {PLAYERS[current_player]} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    play_game()
