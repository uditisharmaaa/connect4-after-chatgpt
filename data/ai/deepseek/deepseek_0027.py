import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def initialize_board():
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    clear_screen()
    # Print column headers
    print('  ' + '   '.join([chr(65 + i) for i in range(BOARD_COLS)]))
    # Print board rows
    for row in board:
        print('+---' * BOARD_COLS + '+')
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
    print('+---' * BOARD_COLS + '+')

def get_random_first_player():
    return random.choice(PLAYERS)

def is_valid_column(column):
    if len(column) != 1:
        return False
    char = column.upper()
    return 'A' <= char <= chr(65 + BOARD_COLS - 1)

def get_column_index(column):
    return ord(column.upper()) - ord('A')

def is_column_full(board, col):
    return board[0][col] != ' '

def place_checker(board, col, checker):
    for row in range(BOARD_ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if all(board[row][col+i] == checker for i in range(4)):
                return True
    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if all(board[row+i][col] == checker for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True
    # Check diagonal (top-right to bottom-left)
    for row in range(BOARD_ROWS - 3):
        for col in range(3, BOARD_COLS):
            if all(board[row+i][col-i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = initialize_board()
    current_player = get_random_first_player()
    print_board(board)
    
    while True:
        print(f"Player {current_player}, please enter a column: ", end='')
        column = input().strip()
        
        if not is_valid_column(column):
            print("Invalid input. Please enter a valid column letter (A-G).")
            continue
        
        col_index = get_column_index(column)
        
        if is_column_full(board, col_index):
            print("Column is full. Please choose another column.")
            continue
        
        place_checker(board, col_index, current_player)
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
