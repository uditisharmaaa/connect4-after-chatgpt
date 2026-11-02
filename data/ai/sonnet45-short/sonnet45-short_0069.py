import os
import random

ROWS, COLS = 6, 7
PLAYERS = ['X', 'O']  # Change to ['X', 'O', 'V'] for 3 players, etc.

def print_board(board):
    os.system('clear')
    print('  A B C D E F G')
    for r in range(ROWS):
        print(r + 1, ' '.join(board[r]))
    print()

def drop(board, col, player):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == '.':
            board[r][col] = player
            return r
    return -1

def check_win(board, r, c, player):
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        count = 1
        for sign in [1, -1]:
            nr, nc = r + dr * sign, c + dc * sign
            while 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == player:
                count += 1
                nr, nc = nr + dr * sign, nc + dc * sign
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(board[0][c] != '.' for c in range(COLS))

board = [['.' for _ in range(COLS)] for _ in range(ROWS)]
current = random.choice(range(len(PLAYERS)))

while True:
    print_board(board)
    player = PLAYERS[current]
    move = input(f"Player {player}, enter column (A-G): ").upper()
    
    if move not in 'ABCDEFG':
        print("Invalid! Press Enter...")
        input()
        continue
    
    col = ord(move) - ord('A')
    r = drop(board, col, player)
    
    if r == -1:
        print("Column full! Press Enter...")
        input()
        continue
    
    if check_win(board, r, col, player):
        print_board(board)
        print(f"Player {player} wins!")
        break
    
    if is_draw(board):
        print_board(board)
        print("Draw!")
        break
    
    current = (current + 1) % len(PLAYERS)
