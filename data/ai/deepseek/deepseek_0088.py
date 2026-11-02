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
    # Clear the screen
    os.system('clear')
    
    # Print column headers
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    
    # Print board rows
    for i in range(ROWS):
        print('+---+' * COLS)
        print('|' + '|'.join(f' {board[i][j]} ' for j in range(COLS)) + '|')
    print('+---+' * COLS)

def get_valid_column(board):
    while True:
        column = input(f"Player {current_player}, please enter a column: ").upper()
        if len(column) != 1 or not column.isalpha():
            print("Invalid input. Please enter a single letter (A-{}).".format(chr(65 + COLS - 1)))
            continue
        
        col_index = ord(column) - ord('A')
        if col_index < 0 or col_index >= COLS:
            print("Column out of range. Please enter a letter between A and {}.".format(chr(65 + COLS - 1)))
            continue
        
        if board[0][col_index] != ' ':
            print("Column is full. Please choose another column.")
            continue
        
        return col_index

def place_checker(board, col, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1

def check_win(board, row, col, player):
    # Check horizontal
    count = 1
    left = col - 1
    while left >= 0 and board[row][left] == player:
        count += 1
        left -= 1
    right = col + 1
    while right < COLS and board[row][right] == player:
        count += 1
        right += 1
    if count >= 4:
        return True

    # Check vertical
    count = 1
    up = row - 1
    while up >= 0 and board[up][col] == player:
        count += 1
        up -= 1
    down = row + 1
    while down < ROWS and board[down][col] == player:
        count += 1
        down += 1
    if count >= 4:
        return True

    # Check diagonal (top-left to bottom-right)
    count = 1
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0 and board[i][j] == player:
        count += 1
        i -= 1
        j -= 1
    i, j = row + 1, col + 1
    while i < ROWS and j < COLS and board[i][j] == player:
        count += 1
        i += 1
        j += 1
    if count >= 4:
        return True

    # Check diagonal (bottom-left to top-right)
    count = 1
    i, j = row + 1, col - 1
    while i < ROWS and j >= 0 and board[i][j] == player:
        count += 1
        i += 1
        j -= 1
    i, j = row - 1, col + 1
    while i >= 0 and j < COLS and board[i][j] == player:
        count += 1
        i -= 1
        j += 1
    if count >= 4:
        return True

    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

# Initialize game
board = initialize_board()
current_player = random.choice(PLAYERS)
print_board(board)

# Game loop
while True:
    col = get_valid_column(board)
    row = place_checker(board, col, current_player)
    print_board(board)
    
    if check_win(board, row, col, current_player):
        print(f"Player {current_player} won!")
        break
    
    if is_draw(board):
        print("Game ended in a draw!")
        break
    
    # Switch to next player
    current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]
