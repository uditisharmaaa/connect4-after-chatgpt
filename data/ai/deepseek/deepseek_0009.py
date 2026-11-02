import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Clear the screen
    os.system('clear')
    
    # Print column headers
    header = '  ' + '   '.join([chr(65 + i) for i in range(COLS)])
    print(header)
    
    # Print each row with borders
    border = '+' + ('---+' * COLS)
    for row in board:
        print(border)
        print('|' + '|'.join([' ' + cell + ' ' for cell in row]) + '|')
    print(border)

def get_player_checkers(num_players):
    checkers = ['X', 'O', 'V', 'H', 'M']
    return checkers[:num_players]

def get_random_player(players):
    return random.choice(players)

def is_valid_column(column):
    if len(column) != 1:
        return False
    col_char = column.upper()
    return col_char >= 'A' and col_char < chr(65 + COLS)

def get_column_index(column):
    return ord(column.upper()) - ord('A')

def place_checker(board, column, checker):
    col_index = get_column_index(column)
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontally
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Check vertically
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonally (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Check diagonally (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    return False

def is_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    board = initialize_board()
    players = get_player_checkers(PLAYERS)
    current_player = get_random_player(players)
    
    print_board(board)
    
    while True:
        column = input(f"Player {current_player}, please enter a column: ").strip()
        
        if not is_valid_column(column):
            print("Invalid column. Please enter a valid column letter (A to G).")
            continue
        
        col_index = get_column_index(column)
        
        if col_index < 0 or col_index >= COLS:
            print("Column is out of bounds. Please try again.")
            continue
        
        if not place_checker(board, column, current_player):
            print("Column is full. Please choose another column.")
            continue
        
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print("Game is a draw!")
            break
        
        # Switch to next player
        current_player = players[(players.index(current_player) + 1) % PLAYERS]

if __name__ == "__main__":
    main()
