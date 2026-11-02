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
    headers = ['  ' + chr(ord('A') + i) + '  ' for i in range(COLS)]
    print(''.join(headers))
    # Print top border
    print('+' + ('---+' * COLS))
    # Print each row
    for row in board:
        row_str = '|'
        for cell in row:
            row_str += ' ' + cell + ' |'
        print(row_str)
        print('+' + ('---+' * COLS))

def get_column_index(col_input):
    if len(col_input) != 1:
        return -1
    col_char = col_input.upper()
    if not col_char.isalpha():
        return -1
    col_idx = ord(col_char) - ord('A')
    if col_idx < 0 or col_idx >= COLS:
        return -1
    return col_idx

def is_valid_move(board, col_idx):
    if col_idx == -1:
        return False
    return board[0][col_idx] == ' '

def drop_checker(board, col_idx, player):
    for row in range(ROWS-1, -1, -1):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = player
            return True
    return False

def check_win(board, player):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == player and 
                board[row][col+1] == player and 
                board[row][col+2] == player and 
                board[row][col+3] == player):
                return True
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == player and 
                board[row+1][col] == player and 
                board[row+2][col] == player and 
                board[row+3][col] == player):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == player and 
                board[row+1][col+1] == player and 
                board[row+2][col+2] == player and 
                board[row+3][col+3] == player):
                return True
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if (board[row][col] == player and 
                board[row+1][col-1] == player and 
                board[row+2][col-2] == player and 
                board[row+3][col-3] == player):
                return True
    return False

def is_board_full(board):
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def play_game():
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column: ", end='')
        col_input = input().strip()
        col_idx = get_column_index(col_input)
        
        if not is_valid_move(board, col_idx):
            continue
        
        drop_checker(board, col_idx, current_player)
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_board_full(board):
            print_board(board)
            print("Game is a draw!")
            break
        
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
