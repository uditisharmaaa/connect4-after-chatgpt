import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    for row in board:
        print('+---' * COLS + '+')
        print('|' + '|'.join(f' {col} ' for col in row) + '|')
    print('+---' * COLS + '+')

def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False

def check_win(board, checker):
    for r in range(ROWS):
        for c in range(COLS):
            if c <= COLS - 4 and all(board[r][c + i] == checker for i in range(4)):
                return True
            if r <= ROWS - 4 and all(board[r + i][c] == checker for i in range(4)):
                return True
            if r <= ROWS - 4 and c <= COLS - 4 and all(board[r + i][c + i] == checker for i in range(4)):
                return True
            if r >= 3 and c <= COLS - 4 and all(board[r - i][c + i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(col != ' ' for row in board for col in row)

def valid_column(column):
    return len(column) == 1 and column.isalpha() and 'A' <= column <= 'G'

def main():
    board = create_board(ROWS, COLS)
    print_board(board)
    current_player = random.randint(0, PLAYERS - 1)
    
    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        column = input().strip().upper()
        
        if not valid_column(column):
            print("Invalid input. Try again.")
            continue
        
        col_idx = ord(column) - ord('A')
        
        if not drop_checker(board, col_idx, CHECKERS[current_player]):
            print("Column full. Turn lost.")
        else:
            print_board(board)
            
            if check_win(board, CHECKERS[current_player]):
                print(f"Player {CHECKERS[current_player]} won!")
                break
            
            if check_draw(board):
                print("The game is a draw!")
                break
            
            current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
