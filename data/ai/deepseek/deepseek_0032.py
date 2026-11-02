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
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    
    # Print the board
    for row in board:
        print('+---' * COLS + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---' * COLS + '+')

def is_valid_column(col):
    return len(col) == 1 and col.isupper() and ord(col) - 65 >= 0 and ord(col) - 65 < COLS

def get_column_index(col):
    return ord(col) - 65

def find_empty_row(board, col_index):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            return row
    return -1  # Column is full

def place_checker(board, col_index, player):
    row = find_empty_row(board, col_index)
    if row != -1:
        board[row][col_index] = player
    return row != -1

def check_win(board, row, col, player):
    # Directions: horizontal, vertical, diagonal down, diagonal up
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    
    for dr, dc in directions:
        count = 1
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def play_game():
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    print_board(board)
    
    while True:
        print(f"Player {current_player}, please enter a column: ")
        col = input().strip().upper()
        
        if not is_valid_column(col):
            print("Invalid input. Please enter a valid column letter (e.g., A, B, ..., G).")
            continue
        
        col_index = get_column_index(col)
        if not place_checker(board, col_index, current_player):
            print("Column is full. Try another column.")
            continue
        
        print_board(board)
        
        # Check for win
        row = find_empty_row(board, col_index) + 1  # The just placed row
        if check_win(board, row, col_index, current_player):
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if is_draw(board):
            print("The game is a draw!")
            break
        
        # Switch player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
