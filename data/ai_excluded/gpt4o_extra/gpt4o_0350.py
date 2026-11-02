import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Set to 2 for submission as per assignment requirements

# Helper functions
def clear_screen():
    os.system('clear')

def initialize_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    print('  ' + '   '.join(chr(ord('A') + i) for i in range(COLUMNS)))
    print('+---' * COLUMNS + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * COLUMNS + '+')

def get_column_index(column):
    if column.isalpha() and ord(column) >= ord('A') and ord(column) < ord('A') + COLUMNS:
        return ord(column) - ord('A')
    return -1

def drop_checker(board, column_index, checker):
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = checker
            return True
    return False

def is_win(board, checker):
    # Check horizontal, vertical, diagonal winning condition
    for r in range(ROWS):
        for c in range(COLUMNS):
            if (c + 3 < COLUMNS and all(board[r][c + i] == checker for i in range(4))):
                return True
            if (r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4))):
                return True
            if (r + 3 < ROWS and c + 3 < COLUMNS and all(board[r + i][c + i] == checker for i in range(4))):
                return True
            if (r + 3 < ROWS and c - 3 >= 0 and all(board[r + i][c - i] == checker for i in range(4))):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Main game loop
def connect4():
    board = initialize_board(ROWS, COLUMNS)
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        checker = players[current_player_index]
        print(f"Player {checker}, please enter a column:")
        column_input = input().strip().upper()
        
        column_index = get_column_index(column_input)
        
        if column_index == -1:
            print("Invalid input! Please enter a valid column letter.")
            continue
        
        if not drop_checker(board, column_index, checker):
            print("Column is full! Choose another column.")
            continue
        
        print_board(board)
        
        if is_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Run the game
if __name__ == "__main__":
    connect4()
