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
    
    # Print column labels (A, B, C, ...)
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    
    # Print the board rows with separators
    for row in board:
        print('+' + '---+' * COLS)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    
    # Print the bottom border
    print('+' + '---+' * COLS)

def get_valid_column(board):
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col) != 1 or not col.isalpha():
            print("Invalid input. Please enter a single letter from A to", chr(65 + COLS - 1))
            continue
        col_num = ord(col) - ord('A')
        if col_num < 0 or col_num >= COLS:
            print("Column out of range. Please enter a letter from A to", chr(65 + COLS - 1))
            continue
        if board[0][col_num] != ' ':
            print("Column is full. Choose another column.")
            continue
        return col_num

def place_checker(board, col, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1

def check_win(board, row, col, player):
    # Check horizontal
    count = 0
    for c in range(max(0, col - 3), min(COLS, col + 4)):
        if board[row][c] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(max(0, row - 3), min(ROWS, row + 4)):
        if board[r][col] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    for i in range(-3, 4):
        r = row + i
        c = col + i
        if 0 <= r < ROWS and 0 <= c < COLS:
            if board[r][c] == player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    
    # Check diagonal (top-right to bottom-left)
    count = 0
    for i in range(-3, 4):
        r = row + i
        c = col - i
        if 0 <= r < ROWS and 0 <= c < COLS:
            if board[r][c] == player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    
    return False

def check_draw(board):
    return all(cell != ' ' for cell in board[0])

# Initialize the game
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
    
    if check_draw(board):
        print("Game ended in a draw!")
        break
    
    # Switch players
    current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]
