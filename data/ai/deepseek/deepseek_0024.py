import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    # Print column headers
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    # Print board rows
    for row in range(ROWS):
        print('+' + '---+' * COLS)
        print('|' + '|'.join([f' {board[row][col]} ' for col in range(COLS)]) + '|')
    print('+' + '---+' * COLS)

def is_valid_column(column):
    if len(column) != 1:
        return False
    col = ord(column.upper()) - ord('A')
    return 0 <= col < COLS

def drop_checker(board, col, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col+i] == checker for i in range(4)):
                return True
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row+i][col] == checker for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = create_board()
    current_player = random.randint(0, PLAYERS-1)
    
    while True:
        print_board(board)
        print(f"Player {CHECKERS[current_player]}, please enter a column: ", end='')
        col_input = input().strip().upper()
        
        if not is_valid_column(col_input):
            continue
        
        col = ord(col_input) - ord('A')
        if not drop_checker(board, col, CHECKERS[current_player]):
            continue
        
        if check_win(board, CHECKERS[current_player]):
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
