import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Print column headers
    print('  ' + '   '.join(chr(ord('A') + i) for i in range(COLS)))
    # Print board rows
    for row in board:
        print('+' + '---+' * COLS)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+' + '---+' * COLS)

def is_valid_column(col):
    if len(col) != 1:
        return False
    col = col.upper()
    return 'A' <= col <= chr(ord('A') + COLS - 1)

def place_checker(board, col, checker):
    col_index = ord(col.upper()) - ord('A')
    for row in range(ROWS-1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def play_game():
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        clear_screen()
        print_board(board)
        
        checker = PLAYERS[current_player]
        print(f"Player {checker}, please enter a column: ")
        col = input().strip()
        
        if not is_valid_column(col):
            print("Invalid column. Please enter a valid column (A-G).")
            continue
        
        col = col.upper()
        if not place_checker(board, col, checker):
            print("Column is full. You lose your turn.")
        else:
            if check_win(board, checker):
                clear_screen()
                print_board(board)
                print(f"Player {checker} won!")
                break
            if is_draw(board):
                clear_screen()
                print_board(board)
                print("The game is a draw!")
                break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
