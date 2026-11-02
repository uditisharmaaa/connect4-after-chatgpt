import os
import random
import sys

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def clear_screen():
    os.system('clear')

def print_board(board):
    # Print column headers
    header = '  ' + '   '.join(chr(65 + i) for i in range(BOARD_COLS))
    print(header)
    
    # Print board rows
    border = '+' + ('---+' * BOARD_COLS)
    for row in board:
        print(border)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print(border)

def get_column_index(col):
    if len(col) != 1:
        return -1
    col = col.upper()
    return ord(col) - ord('A')

def is_valid_column(board, col_index):
    if col_index < 0 or col_index >= BOARD_COLS:
        return False
    return board[0][col_index] == ' '

def place_checker(board, col_index, checker):
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(BOARD_ROWS - 3):
        for col in range(3, BOARD_COLS):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True
    
    return False

def is_board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = initialize_board()
    current_player = random.choice(range(NUM_PLAYERS))
    clear_screen()
    print_board(board)
    
    while True:
        player_checker = PLAYERS[current_player]
        print(f"Player {player_checker}, please enter a column: ")
        col_input = input().strip().upper()
        col_index = get_column_index(col_input)
        
        if col_index == -1 or not is_valid_column(board, col_index):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        place_checker(board, col_index, player_checker)
        clear_screen()
        print_board(board)
        
        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break
        
        if is_board_full(board):
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
