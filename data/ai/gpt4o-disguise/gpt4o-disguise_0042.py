import random
import os

COLS = 7
ROWS = 6
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(cols, rows):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    columns = '  '.join(chr(65+i) for i in range(len(board[0])))
    print(columns)
    print('+' + '---+' * len(board[0]))
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * len(board[0]))
        
def valid_input(input, cols):
    return len(input) == 1 and input.isalpha() and 65 <= ord(input) < 65 + cols

def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return True
    return False

def check_win(board, checker):
    for r in range(ROWS):
        for c in range(COLS):
            if c <= COLS - 4 and all(board[r][c+i] == checker for i in range(4)):
                return True
            if r <= ROWS - 4 and all(board[r+i][c] == checker for i in range(4)):
                return True
            if r <= ROWS - 4 and c <= COLS - 4 and all(board[r+i][c+i] == checker for i in range(4)):
                return True
            if r >= 3 and c <= COLS - 4 and all(board[r-i][c+i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(COLS, ROWS)
    print_board(board)
    current_player = random.choice(range(PLAYERS))
    
    while True:
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column:")
        while True:
            user_input = input().strip().upper()
            if valid_input(user_input, COLS):
                col = ord(user_input) - 65
                if drop_checker(board, col, checker):
                    break
                else:
                    print("Column full. Try another.")
            else:
                print("Invalid input. Try again.")
        
        print_board(board)
        
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS
        
main()
