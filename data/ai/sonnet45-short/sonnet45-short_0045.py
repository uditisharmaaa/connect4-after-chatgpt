import os
import random

ROWS, COLS = 6, 7
PLAYERS = ['X', 'O']  # Change to ['X', 'O', 'V'] for 3 players, etc.

board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def show():
    os.system('clear')
    print(' A B C D E F G')
    for row in board:
        print('|' + '|'.join(row) + '|')
    print('-' * (COLS * 2 + 1))

def drop(col, player):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = player
            return r
    return -1

def check_win(r, c, player):
    def line(dr, dc):
        count = 0
        for i in range(-3, 4):
            nr, nc = r + dr * i, c + dc * i
            if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
        return False
    return line(0, 1) or line(1, 0) or line(1, 1) or line(1, -1)

def is_draw():
    return all(board[0][c] != ' ' for c in range(COLS))

random.shuffle(PLAYERS)
turn = 0

while True:
    show()
    player = PLAYERS[turn % len(PLAYERS)]
    col = input(f"Player {player}, enter column (A-G): ").upper()
    
    if col not in 'ABCDEFG':
        continue
    
    col_idx = ord(col) - ord('A')
    row = drop(col_idx, player)
    
    if row == -1:
        continue
    
    if check_win(row, col_idx, player):
        show()
        print(f"Player {player} wins!")
        break
    
    if is_draw():
        show()
        print("Draw!")
        break
    
    turn += 1
