import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # Change to ['X', 'O', 'V', 'H'] for 4 players, etc.

def print_board(board):
    os.system('clear')
    print(' A B C D E F G')
    for row in board:
        print('|' + '|'.join(row) + '|')
    print('-' * 15)

def make_move(board, col, player):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1

def check_win(board, row, col, player):
    # Check horizontal, vertical, and both diagonals
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        count = 1
        for d in [1, -1]:
            r, c = row + dr*d, col + dc*d
            while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                count += 1
                r, c = r + dr*d, c + dc*d
        if count >= 4:
            return True
    return False

def is_full(board):
    return all(board[0][c] != ' ' for c in range(COLS))

# Initialize
board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
current = random.choice(PLAYERS)

# Game loop
while True:
    print_board(board)
    col_input = input(f"Player {current}, choose column (A-G): ").upper()
    
    if col_input not in 'ABCDEFG':
        print("Invalid input!")
        input("Press Enter...")
        continue
    
    col = ord(col_input) - ord('A')
    row = make_move(board, col, current)
    
    if row == -1:
        print("Column full!")
        input("Press Enter...")
        continue
    
    if check_win(board, row, col, current):
        print_board(board)
        print(f"Player {current} wins!")
        break
    
    if is_full(board):
        print_board(board)
        print("Draw!")
        break
    
    current = PLAYERS[(PLAYERS.index(current) + 1) % len(PLAYERS)]
