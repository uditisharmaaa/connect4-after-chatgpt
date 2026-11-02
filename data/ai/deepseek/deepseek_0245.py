import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    for row in board:
        print('+---' * COLS + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---' * COLS + '+')

def is_valid_move(col, board):
    return 0 <= col < COLS and board[0][col] == ' '

def place_checker(col, board, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS-3):
            if all(board[row][col+i] == checker for i in range(4)):
                return True
    # Check vertical
    for row in range(ROWS-3):
        for col in range(COLS):
            if all(board[row+i][col] == checker for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS-3):
        for col in range(COLS-3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS-3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = initialize_board()
    current_player = random.randint(0, PLAYERS-1)
    checkers = CHECKERS[:PLAYERS]
    
    while True:
        print_board(board)
        print(f"Player {checkers[current_player]}, please enter a column: ")
        move = input().upper()
        
        if len(move) != 1 or not move.isalpha():
            continue
        
        col = ord(move) - ord('A')
        if not is_valid_move(col, board):
            continue
        
        if place_checker(col, board, checkers[current_player]):
            if check_win(board, checkers[current_player]):
                print_board(board)
                print(f"Player {checkers[current_player]} won!")
                break
            if is_draw(board):
                print_board(board)
                print("Game ended in a draw!")
                break
            current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
