import random
import os

# Constants
ROWS = 6
COLS = 7
PLAYERS_COUNT = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS_COUNT]

def initialize_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    col_labels = " ".join([chr(i) for i in range(ord('A'), ord('A') + len(board[0]))])
    print(f"  {col_labels}")
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def is_valid_input(input_str, cols):
    return input_str in [chr(i) for i in range(ord('A'), ord('A') + cols)]

def place_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontally
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Check vertically
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonally \
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Check diagonally /
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def connect_four():
    board = initialize_board(ROWS, COLS)
    current_player = random.choice(range(PLAYERS_COUNT))
    
    while True:
        print_board(board)
        current_checker = CHECKERS[current_player]
        print(f"Player {current_checker}, please enter a column:")
        player_input = input().strip().upper()
        
        if not is_valid_input(player_input, COLS):
            print("Invalid input, please enter a valid column!")
            continue
        
        col_index = ord(player_input) - ord('A')
        
        if not place_checker(board, col_index, current_checker):
            print("Column is full, you lose your turn!")
            current_player = (current_player + 1) % PLAYERS_COUNT
            continue
        
        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS_COUNT

connect_four()
