import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    separator = '+' + ('---+' * COLS)
    print(separator)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print(separator)

def get_valid_column(board):
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col) != 1 or not ('A' <= col <= chr(65 + COLS - 1)):
            print(f"Invalid column. Please enter a letter from A to {chr(65 + COLS - 1)}.")
            continue
        col_index = ord(col) - ord('A')
        if board[0][col_index] != ' ':
            print("Column is full. Please choose another column.")
            continue
        return col_index

def place_checker(board, col, player):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row

def check_win(board, row, col):
    directions = [
        (0, 1),  # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down
        (1, -1)   # diagonal up
    ]
    player = board[row][col]
    for dr, dc in directions:
        count = 1
        for step in [1, -1]:
            r, c = row + step*dr, col + step*dc
            while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                count += 1
                r += step*dr
                c += step*dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(cell != ' ' for cell in board[0])

board = initialize_board()
current_player = random.choice(CHECKERS)
print_board(board)

while True:
    col = get_valid_column(board)
    row = place_checker(board, col, current_player)
    print_board(board)
    
    if check_win(board, row, col):
        print(f"Player {current_player} won!")
        break
    if is_draw(board):
        print("Game ended in a draw!")
        break
    
    current_player = CHECKERS[(CHECKERS.index(current_player) + 1) % PLAYERS]
