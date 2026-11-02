import os
import random

# Global constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    header = "  " + " ".join(chr(65 + i) for i in range(len(board[0])))
    print(header)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")
        
def is_valid_input(input_char, columns):
    return input_char.isalpha() and ord(input_char.upper()) - ord('A') < columns

def is_column_full(board, col_index):
    return all(row[col_index] != ' ' for row in board)

def place_checker(board, col_index, checker):
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = checker
            break

def check_for_win(board, checker):
    # Check horizontal, vertical, diagonal (both directions)
    for row in range(ROWS):
        for col in range(COLUMNS - 3):  # horizontal
            if all(board[row][c] == checker for c in range(col, col + 4)):
                return True
            
    for row in range(ROWS - 3):  # vertical
        for col in range(COLUMNS):
            if all(board[r][col] == checker for r in range(row, row + 4)):
                return True
            
    for row in range(ROWS - 3):  # diagonal /
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    for row in range(3, ROWS):  # diagonal \
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    return False

def check_for_draw(board):
    return all(all(cell != ' ' for cell in row) for row in board)

def play_game():
    board = initialize_board(ROWS, COLUMNS)
    print_board(board)
    current_player = random.randint(0, PLAYERS - 1)
    
    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        user_input = input().strip().upper()
        
        if not is_valid_input(user_input, COLUMNS):
            print("Invalid input. Please enter a valid column.")
            continue
        
        col_index = ord(user_input) - ord('A')
        
        if is_column_full(board, col_index):
            print("Column is full, you lose your turn.")
        else:
            place_checker(board, col_index, CHECKERS[current_player])
            print_board(board)
            
            if check_for_win(board, CHECKERS[current_player]):
                print(f"Player {CHECKERS[current_player]} won!")
                break
                
            if check_for_draw(board):
                print("The game is a draw!")
                break
                
            current_player = (current_player + 1) % PLAYERS

# Set the board dimensions and number of players to defaults for submission
ROWS = 6
COLUMNS = 7
PLAYERS = 2

play_game()
