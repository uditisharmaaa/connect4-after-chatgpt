import os
import random

ROWS, COLS = 6, 7
PLAYERS = ['X', 'O']  # Change to ['X', 'O', 'V', 'H', 'M'] for more players
board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board():
    os.system('clear')
    print(' A B C D E F G')
    for row in board:
        print('|' + '|'.join(row) + '|')
    print('-' * 15)

def drop(col, player):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = player
            return r
    return -1

def check_win(r, c, player):
    # Check horizontal, vertical, and both diagonals
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

def is_draw():
    return all(board[0][c] != ' ' for c in range(COLS))

random.shuffle(PLAYERS)
turn = 0

while True:
    print_board()
    player = PLAYERS[turn % len(PLAYERS)]
    col = input(f"Player {player}, pick column (A-G): ").upper()
    
    if col not in 'ABCDEFG':
        continue
    
    c = ord(col) - ord('A')
    r = drop(c, player)
    
    if r == -1:
        continue
    
    if check_win(r, c, player):
        print_board()
        print(f"Player {player} wins!")
        break
    
    if is_draw():
        print_board()
        print("Draw!")
        break
    
    turn += 1
