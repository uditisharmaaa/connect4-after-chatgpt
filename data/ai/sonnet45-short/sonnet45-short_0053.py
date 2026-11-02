import os
import random

ROWS, COLS = 6, 7
PLAYERS = ['X', 'O']  # Change to ['X', 'O', 'V'] for 3 players, etc.

def print_board(board):
    os.system('clear')
    print('  A B C D E F G')
    for i, row in enumerate(board):
        print(f"{i+1} {' '.join(row)}")

def drop(board, col, player):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == '.':
            board[r][col] = player
            return r
    return -1

def check_win(board, r, c, player):
    dirs = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in dirs:
        count = 1
        for d in [1, -1]:
            nr, nc = r + dr*d, c + dc*d
            while 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == player:
                count += 1
                nr, nc = nr + dr*d, nc + dc*d
        if count >= 4:
            return True
    return False

board = [['.' for _ in range(COLS)] for _ in range(ROWS)]
current = random.choice(PLAYERS)

for turn in range(ROWS * COLS):
    print_board(board)
    print(f"Player {current}'s turn")
    
    col_input = input("Choose column (A-G): ").upper()
    if col_input not in 'ABCDEFG':
        print("Invalid input!"); input("Press Enter..."); continue
    
    col = ord(col_input) - ord('A')
    row = drop(board, col, current)
    
    if row == -1:
        print("Column full!"); input("Press Enter..."); continue
    
    if check_win(board, row, col, current):
        print_board(board)
        print(f"Player {current} wins!")
        break
    
    current = PLAYERS[(PLAYERS.index(current) + 1) % len(PLAYERS)]
else:
    print_board(board)
    print("It's a draw!")
