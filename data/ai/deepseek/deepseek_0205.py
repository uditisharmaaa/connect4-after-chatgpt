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
    headers = [chr(65 + i) for i in range(COLS)]
    print('  ' + '   '.join(headers))
    for row in board:
        line = '+'.join(['---'] * COLS)
        print('+' + line + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+' + '+'.join(['---'] * COLS) + '+')

def is_valid_column(col):
    return len(col) == 1 and col.isupper() and 'A' <= col <= chr(65 + COLS - 1)

def place_checker(board, col, checker):
    col_idx = ord(col) - ord('A')
    for row in reversed(range(ROWS)):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    
    while True:
        os.system('clear')
        print_board(board)
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column: ")
        
        while True:
            col = input().upper()
            if not is_valid_column(col):
                print("Invalid input. Try again: ", end='')
                continue
            if place_checker(board, col, checker):
                break
            print("Column full. Try another column: ", end='')
        
        if check_win(board, checker):
            os.system('clear')
            print_board(board)
            print(f"Player {checker} won!")
            break
        
        if is_draw(board):
            os.system('clear')
            print_board(board)
            print("Game ended in a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
