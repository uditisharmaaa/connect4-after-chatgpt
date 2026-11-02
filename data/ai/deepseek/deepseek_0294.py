import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Clear the screen
    os.system('clear')
    
    # Print column headers
    header = '  ' + '   '.join([chr(65 + i) for i in range(COLS)])
    print(header)
    
    # Print each row with borders
    for row in board:
        line = '+---' * COLS + '+'
        print(line)
        print('| ' + ' | '.join(row) + ' |')
    
    # Print bottom border
    print('+---' * COLS + '+')

def get_valid_column(board):
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col) != 1 or not col.isalpha():
            print("Invalid input. Please enter a single letter.")
            continue
        col_idx = ord(col) - ord('A')
        if col_idx < 0 or col_idx >= COLS:
            print(f"Column must be between A and {chr(65 + COLS - 1)}.")
            continue
        if board[0][col_idx] != ' ':
            print("Column is full. Choose another column.")
            continue
        return col_idx

def place_checker(board, col, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row][col+1] == checker and 
                board[row][col+2] == checker and 
                board[row][col+3] == checker):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == checker and 
                board[row+1][col] == checker and 
                board[row+2][col] == checker and 
                board[row+3][col] == checker):
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row+1][col+1] == checker and 
                board[row+2][col+2] == checker and 
                board[row+3][col+3] == checker):
                return True
    
    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row-1][col+1] == checker and 
                board[row-2][col+2] == checker and 
                board[row-3][col+3] == checker):
                return True
    
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Initialize game
board = create_board()
player_checkers = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]
current_player = random.randint(0, PLAYERS - 1)
print_board(board)

# Game loop
while True:
    col = get_valid_column(board)
    place_checker(board, col, player_checkers[current_player])
    print_board(board)
    
    if check_win(board, player_checkers[current_player]):
        print(f"Player {player_checkers[current_player]} won!")
        break
    
    if is_draw(board):
        print("Game ended in a draw!")
        break
    
    # Switch player
    current_player = (current_player + 1) % PLAYERS
