import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    # Print column headers
    print('  ' + '   '.join([chr(ord('A') + i) for i in range(BOARD_COLS)]))
    
    # Print top border
    print('+' + ('---+' * BOARD_COLS))
    
    for row in board:
        # Print row content
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
        # Print row border
        print('+' + ('---+' * BOARD_COLS))

def is_valid_column(col):
    if len(col) != 1:
        return False
    return 'A' <= col <= chr(ord('A') + BOARD_COLS - 1)

def place_checker(board, col, checker):
    col_idx = ord(col) - ord('A')
    for row_idx in range(BOARD_ROWS-1, -1, -1):
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
    
    # Check diagonal down-right
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if (board[row][col] == checker and 
                board[row+1][col+1] == checker and 
                board[row+2][col+2] == checker and 
                board[row+3][col+3] == checker):
                return True
    
    # Check diagonal up-right
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
    board = create_board()
    current_player = random.choice(PLAYERS)
    game_over = False
    
    clear_screen()
    print_board(board)
    
    while not game_over:
        print(f"Player {current_player}, please enter a column: ")
        col_input = input().strip().upper()
        
        if not is_valid_column(col_input):
            print("Invalid input. Please enter a valid column letter (A-G).")
            continue
            
        if not place_checker(board, col_input, current_player):
            print("Column is full. Please choose another column.")
            continue
        
        clear_screen()
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            game_over = True
        elif is_draw(board):
            print("Game is a draw!")
            game_over = True
        else:
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
