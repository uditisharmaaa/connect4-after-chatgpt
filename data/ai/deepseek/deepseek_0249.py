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
    # Print column headers
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    
    # Print the board rows
    for row in board:
        print('+' + '---+' * COLS)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    
    print('+' + '---+' * COLS)

def is_valid_column(column):
    if len(column) != 1:
        return False
    col = ord(column.upper()) - ord('A')
    return 0 <= col < COLS

def place_checker(board, col, player):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False

def check_win(board, player):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == player for i in range(4)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True
    
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        os.system('clear')
        print_board(board)
        
        print(f"Player {current_player}, please enter a column: ")
        column_input = input().strip().upper()
        
        if not is_valid_column(column_input):
            print("Invalid input. Please enter a valid column letter (A-G).")
            input("Press Enter to continue...")
            continue
        
        col = ord(column_input) - ord('A')
        
        if not place_checker(board, col, current_player):
            print("Column is full. Please choose another column.")
            input("Press Enter to continue...")
            continue
        
        if check_win(board, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break
        
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
