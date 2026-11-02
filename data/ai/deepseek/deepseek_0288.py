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
    os.system('clear')
    # Print column headers
    header = '  ' + '   '.join([chr(ord('A') + i) for i in range(BOARD_COLS)])
    print(header)
    
    # Print board rows
    for row in board:
        line = '+'.join(['---'] * BOARD_COLS)
        print(f"+{line}+")
        print("| " + " | ".join(row) + " |")
    
    # Print bottom border
    line = '+'.join(['---'] * BOARD_COLS)
    print(f"+{line}+")

def is_valid_column(col):
    if len(col) != 1:
        return False
    col = col.upper()
    if col < 'A' or col > chr(ord('A') + BOARD_COLS - 1):
        return False
    return True

def get_column_index(col):
    return ord(col.upper()) - ord('A')

def place_checker(board, col, checker):
    col_idx = get_column_index(col)
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
    
    # Check diagonal (down-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == checker and 
                board[row+1][col+1] == checker and 
                board[row+2][col+2] == checker and 
                board[row+3][col+3] == checker):
                return True
    
    # Check diagonal (up-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == checker and 
                board[row-1][col+1] == checker and 
                board[row-2][col+2] == checker and 
                board[row-3][col+3] == checker):
                return True
    
    return False

def is_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    
    while True:
        checker = PLAYERS[current_player]
        print(f"Player {checker}, please enter a column: ", end='')
        col_input = input().strip().upper()
        
        if not is_valid_column(col_input):
            print("Invalid input. Please enter a valid column letter (A-{}).".format(chr(ord('A') + BOARD_COLS - 1)))
            continue
        
        col = col_input[0]
        if not place_checker(board, col, checker):
            print("Column is full. Please choose another column.")
            continue
        
        print_board(board)
        
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        if is_draw(board):
            print("Game ended in a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
