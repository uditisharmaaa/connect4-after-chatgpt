import os
import random
from itertools import cycle

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def init_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    for row in board:
        print('+---' * COLS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLS + '+')

def is_valid_input(col):
    return len(col) == 1 and 'A' <= col <= chr(65 + COLS - 1)

def place_checker(board, col, checker):
    col_idx = ord(col) - ord('A')
    for row in reversed(range(ROWS)):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return True
    return False

def check_win(board, checker):
    # Horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = init_board()
    players = cycle(CHECKERS[:PLAYERS])
    current_player = next(players)
    print_board(board)
    
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if not is_valid_input(col):
            print("Invalid input! Choose a column from A to", chr(65 + COLS - 1))
            continue
        
        if not place_checker(board, col, current_player):
            print("Column is full! Lost turn.")
            current_player = next(players)
            print_board(board)
            continue
        
        print_board(board)
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if is_draw(board):
            print("Game ended in a draw!")
            break
        
        current_player = next(players)

if __name__ == "__main__":
    play_game()
