import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def init_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    print('+' + ('---+' * COLS))
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + ('---+' * COLS))

def get_col(input_char):
    return ord(input_char.upper()) - 65 if input_char else -1

def is_valid_column(col):
    return 0 <= col < COLS

def place_checker(board, col, checker):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                for i in range(1, 4):
                    nr, nc = r + i * dr, c + i * dc
                    if not (0 <= nr < ROWS and 0 <= nc < COLS) or board[nr][nc] != checker:
                        break
                else:
                    return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = init_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)
    
    while True:
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column:")
        col_input = input().upper()
        
        if len(col_input) != 1 or (col := get_col(col_input[0])) == -1 or not is_valid_column(col):
            continue
            
        if not place_checker(board, col, checker):
            continue
            
        print_board(board)
        
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
            
        if is_draw(board):
            print("Draw!")
            break
            
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
