import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    # Clear the screen
    os.system('clear')
    
    # Print column headers
    print('  ' + '   '.join(chr(65 + i) for i in range(BOARD_COLS)))
    
    # Print the board
    for row in board:
        print('+---+' * BOARD_COLS)
        print('| ' + ' | '.join(row) + ' |')
    print('+---+' * BOARD_COLS)

def is_valid_column(col):
    if len(col) != 1:
        return False
    col = col.upper()
    return col >= 'A' and col <= chr(65 + BOARD_COLS - 1)

def drop_checker(board, col, checker):
    col_idx = ord(col.upper()) - ord('A')
    for row_idx in range(BOARD_ROWS - 1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == checker and 
                board[row][col+1] == checker and 
                board[row][col+2] == checker and 
                board[row][col+3] == checker):
                return True
    
    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if (board[row][col] == checker and 
                board[row+1][col] == checker and 
                board[row+2][col] == checker and 
                board[row+3][col] == checker):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == checker and 
                board[row+1][col+1] == checker and 
                board[row+2][col+2] == checker and 
                board[row+3][col+3] == checker):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(BOARD_ROWS - 3):
        for col in range(3, BOARD_COLS):
            if (board[row][col] == checker and 
                board[row+1][col-1] == checker and 
                board[row+2][col-2] == checker and 
                board[row+3][col-3] == checker):
                return True
    
    return False

def is_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    print_board(board)
    
    while True:
        # Get player input
        col = input(f"Player {current_player}, please enter a column: ")
        
        # Validate input
        if not is_valid_column(col):
            print("Invalid column. Please enter a valid column (A-{}).".format(chr(65 + BOARD_COLS - 1)))
            continue
        
        col = col.upper()
        col_idx = ord(col) - ord('A')
        
        # Check if column is full
        if board[0][col_idx] != ' ':
            print("Column is full. Please choose another column.")
            continue
        
        # Drop checker
        if not drop_checker(board, col, current_player):
            continue
        
        # Check for win
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if is_draw(board):
            print_board(board)
            print("Game ended in a draw.")
            break
        
        # Switch player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]
        print_board(board)

if __name__ == "__main__":
    main()
