import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def init_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clears the screen
    # Print column headers
    header = '  ' + '   '.join([chr(65 + i) for i in range(COLS)])
    print(header)
    # Print board rows
    for row in board:
        line = '+'.join(['---'] * COLS)
        print(f'+{line}+')
        print('| ' + ' | '.join(row) + ' |')
    # Print bottom border
    line = '+'.join(['---'] * COLS)
    print(f'+{line}+')

def is_valid_column(col):
    if len(col) != 1:
        return False
    col = col.upper()
    return col >= 'A' and col <= chr(65 + COLS - 1)

def get_column_index(col):
    return ord(col.upper()) - 65

def drop_checker(board, col, checker):
    col_idx = get_column_index(col)
    for row_idx in range(ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    # Check horizontal
    for row in board:
        for i in range(COLS - 3):
            if all(cell == checker for cell in row[i:i+4]):
                return True
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + j][col] == checker for j in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + k][col + k] == checker for k in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - k][col + k] == checker for k in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = init_board()
    current_player = random.choice(PLAYERS)
    print_board(board)
    
    while True:
        column = input(f"Player {current_player}, please enter a column: ")
        if not is_valid_column(column):
            print("Invalid column. Please try again.")
            continue
        
        col_idx = get_column_index(column)
        if col_idx < 0 or col_idx >= COLS:
            print("Invalid column. Please try again.")
            continue
        
        if not drop_checker(board, column, current_player):
            print("Column is full. Please try another column.")
            continue
        
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print("It's a draw!")
            break
        
        # Switch player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
