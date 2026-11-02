import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(len(board[0]))))
    print('+---' * len(board[0]) + '+')
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+---' * len(board[0]) + '+')

def get_next_open_row(board, col):
    for r in range(len(board)-1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None

def winning_move(board, checker):
    # Check horizontal locations for win
    for r in range(ROWS):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    
    # Check vertical locations for win
    for r in range(ROWS-3):
        for c in range(COLS):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True

    # Check positively sloped diagonals
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True

    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True
                
    return False

def is_draw(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == ' ':
                return False
    return True

def main():
    board = create_board(ROWS, COLS)
    print_board(board)
    current_player = random.randint(0, PLAYERS-1)
    
    while True:
        print(f'Player {CHECKERS[current_player]}, please enter a column:')
        col_input = input().strip().upper()
        
        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input. Please enter a valid column letter.")
            continue

        col = ord(col_input) - 65

        if col < 0 or col >= COLS:
            print("Invalid column. Please enter a valid column letter.")
            continue

        row = get_next_open_row(board, col)
        if row is None:
            print("Column full. Try another column.")
            continue
        
        board[row][col] = CHECKERS[current_player]
        print_board(board)
        
        if winning_move(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

main()
