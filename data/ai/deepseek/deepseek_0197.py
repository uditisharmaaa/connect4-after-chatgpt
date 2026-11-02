import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    header = '  ' + '   '.join([chr(65 + i) for i in range(COLS)])
    border = '+' + ('---+' * COLS)
    print(header)
    print(border)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print(border)

def get_valid_column(board):
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col) != 1 or not 'A' <= col <= chr(65 + COLS - 1):
            print(f"Invalid input. Please enter a letter from A to {chr(65 + COLS - 1)}.")
            continue
        col_idx = ord(col) - ord('A')
        if board[0][col_idx] != ' ':
            print("Column is full. Please choose another column.")
            continue
        return col_idx

def place_checker(board, col_idx, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return True
    return False

def check_win(board, checker):
    # Horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Diagonal /
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    # Diagonal \
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Initialize game
board = initialize_board()
current_player = random.randint(0, PLAYERS - 1)
print_board(board)

# Game loop
while True:
    col_idx = get_valid_column(board)
    place_checker(board, col_idx, CHECKERS[current_player])
    print_board(board)
    
    if check_win(board, CHECKERS[current_player]):
        print(f"Player {CHECKERS[current_player]} won!")
        break
    if is_draw(board):
        print("Game ended in a draw!")
        break
    
    current_player = (current_player + 1) % PLAYERS
