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
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    # Print board rows
    for row in board:
        print('+---+' * COLS)
        print('| ' + ' | '.join(cell for cell in row) + ' |')
    print('+---+' * COLS)

def drop_checker(board, col, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    # Horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col+i] == checker for i in range(4)):
                return True
    # Vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row+i][col] == checker for i in range(4)):
                return True
    # Diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True
    # Diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)
    
    while True:
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column: ", end='')
        col_input = input().strip().upper()
        
        if not col_input or ord(col_input) - 65 not in range(COLS):
            print("Invalid column! Please try again.")
            continue
        
        col = ord(col_input) - 65
        if not drop_checker(board, col, checker):
            print("Column is full! You lose your turn.")
        else:
            print_board(board)
            if check_win(board, checker):
                print(f"Player {checker} won!")
                break
            if is_draw(board):
                print("It's a draw!")
                break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
