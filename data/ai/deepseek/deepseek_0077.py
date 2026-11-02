import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear' if os.name == 'posix' else 'cls')
    # Print column headers
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    # Print board rows
    for row in board:
        print('+---' * COLS + '+')
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+---' * COLS + '+')

def get_valid_column(board):
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col) != 1 or not 'A' <= col <= chr(65 + COLS - 1):
            print(f"Invalid column. Please enter a letter from A to {chr(65 + COLS - 1)}.")
            continue
        col_index = ord(col) - ord('A')
        if board[0][col_index] != ' ':
            print("Column is full. Please choose another column.")
            continue
        return col_index

def drop_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    return -1, -1

def check_win(board, row, col):
    checker = board[row][col]
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        for step in (1, -1):
            r, c = row + dr * step, col + dc * step
            while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
                count += 1
                r += dr * step
                c += dc * step
                if count == 4:
                    return True
    return False

def is_draw(board):
    return all(cell != ' ' for cell in board[0])

board = create_board()
current_player = random.randint(0, PLAYERS - 1)

while True:
    print_board(board)
    col = get_valid_column(board)
    row, _ = drop_checker(board, col, CHECKERS[current_player])
    
    if check_win(board, row, col):
        print_board(board)
        print(f"Player {CHECKERS[current_player]} won!")
        break
    if is_draw(board):
        print_board(board)
        print("Game ended in a draw!")
        break
    
    current_player = (current_player + 1) % PLAYERS
