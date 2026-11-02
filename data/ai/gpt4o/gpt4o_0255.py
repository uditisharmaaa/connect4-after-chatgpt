import os
import random

# Constants for board dimensions and players
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')  # Clear screen
    
    header = '  ' + '   '.join(chr(ord('A') + i) for i in range(COLUMNS))
    print(header)
    print('+---' * COLUMNS + '+')
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+---' * COLUMNS + '+')

def is_valid_input(input_str):
    if len(input_str) != 1:
        return False
    col = input_str.upper()
    return 'A' <= col <= chr(ord('A') + COLUMNS - 1)

def get_column_index(col):
    return ord(col) - ord('A')

def place_checker(board, column, player_symbol):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player_symbol
            return True
    return False

def check_winner(board, player_symbol):
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if all(row[col + i] == player_symbol for i in range(4)):
                return True
    
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player_symbol for i in range(4)):
                return True
    
    # Check diagonal (bottom left to top right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player_symbol for i in range(4)):
                return True
    
    # Check diagonal (top left to bottom right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player_symbol for i in range(4)):
                return True
    
    return False

def is_board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def game():
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player_index = random.choice(range(NUM_PLAYERS))
    
    print_board(board)
    
    while True:
        current_player = players[current_player_index]
        print(f"Player {current_player}, please enter a column:")
        
        while True:
            user_input = input().strip()
            if not is_valid_input(user_input):
                print("Invalid input. Please enter a column letter (A-G).")
                continue
            
            column_index = get_column_index(user_input.upper())
            if place_checker(board, column_index, current_player):
                break
            else:
                print("Column is full. Please choose another column.")
        
        print_board(board)
        
        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    game()
