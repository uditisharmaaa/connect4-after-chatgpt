import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Players' checkers

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    column_labels = ' '.join(chr(ord('A') + i) for i in range(len(board[0])))
    print(f"  {column_labels}")
    for row in board:
        print('+---' * len(row) + '+')
        print('|' + '|'.join(f" {cell} " for cell in row) + '|')
    print('+---' * len(board[0]) + '+')

def get_column_input(columns):
    while True:
        col_input = input("Please enter a column (A-G): ").strip().upper()
        if len(col_input) == 1 and 'A' <= col_input < chr(ord('A') + columns):
            return ord(col_input) - ord('A')
        print("Invalid input. Try again.")

def place_checker(board, column, player_checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player_checker
            return True
    return False

def check_winner(board, player_checker):
    rows, cols = len(board), len(board[0])
    ranges = range(4)
    
    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == player_checker for i in ranges):
                return True
    
    # Check vertical
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r + i][c] == player_checker for i in ranges):
                return True
    
    # Check diagonal (down-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == player_checker for i in ranges):
                return True
    
    # Check diagonal (down-left)
    for r in range(rows - 3):
        for c in range(3, cols):
            if all(board[r + i][c - i] == player_checker for i in ranges):
                return True
    
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def connect4_game():
    board = create_board(ROWS, COLUMNS)
    current_player_idx = random.randint(0, PLAYERS - 1)
    
    while True:
        print_board(board)
        print(f"Player {CHECKERS[current_player_idx]}, it's your turn.")
        col = get_column_input(COLUMNS)
        
        if place_checker(board, col, CHECKERS[current_player_idx]):
            if check_winner(board, CHECKERS[current_player_idx]):
                print_board(board)
                print(f"Player {CHECKERS[current_player_idx]} won!")
                break
            if check_draw(board):
                print_board(board)
                print("The game is a draw!")
                break
            current_player_idx = (current_player_idx + 1) % PLAYERS
        else:
            print("Column is full. Turn lost.")

connect4_game()
