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
    # Print column headers
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    # Print board rows
    for row in board:
        print('+---+' * COLS)
        print('| ' + ' | '.join(row) + ' |')
    print('+---+' * COLS)

def is_valid_column(col):
    if len(col) != 1:
        return False
    col = col.upper()
    return col.isalpha() and ord(col) - ord('A') < COLS

def drop_checker(board, col, checker):
    col_index = ord(col.upper()) - ord('A')
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if all(cell == checker for cell in row[i:i+4]):
                return True
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal (\) and (/)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
            if all(board[row + i][col + 3 - i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = initialize_board()
    current_player = random.randint(0, PLAYERS - 1)
    
    while True:
        checker = CHECKERS[current_player]
        print_board(board)
        
        # Get valid column input
        while True:
            col = input(f"Player {checker}, please enter a column: ")
            if not is_valid_column(col):
                print("Invalid column. Please choose from A to", chr(65 + COLS - 1))
                continue
            col = col.upper()
            if drop_checker(board, col, checker):
                break
            print("Column is full. Try another column.")
        
        # Check win/draw
        if check_win(board, checker):
            print_board(board)
            print(f"Player {checker} won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        # Next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
