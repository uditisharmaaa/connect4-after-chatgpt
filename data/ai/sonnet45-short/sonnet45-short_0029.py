import os
import random

ROWS, COLS = 6, 7
PLAYERS = ['X', 'O']  # Change to ['X', 'O', 'V'] for 3 players, etc.

def print_board(board):
    os.system('clear')
    print('  A B C D E F G')
    for r in range(ROWS):
        print(r+1, ' '.join(board[r]))
    print()

def check_win(board, player):
    # Horizontal, vertical, diagonal
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != player:
                continue
            if c <= COLS-4 and all(board[r][c+i] == player for i in range(4)):
                return True
            if r <= ROWS-4 and all(board[r+i][c] == player for i in range(4)):
                return True
            if r <= ROWS-4 and c <= COLS-4 and all(board[r+i][c+i] == player for i in range(4)):
                return True
            if r <= ROWS-4 and c >= 3 and all(board[r+i][c-i] == player for i in range(4)):
                return True
    return False

def drop_piece(board, col, player):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == '.':
            board[r][col] = player
            return True
    return False

board = [['.' for _ in range(COLS)] for _ in range(ROWS)]
current = random.choice(range(len(PLAYERS)))

while True:
    print_board(board)
    player = PLAYERS[current]
    col_input = input(f"Player {player}, choose column (A-G): ").upper()
    
    if col_input not in 'ABCDEFG':
        continue
    col = ord(col_input) - ord('A')
    
    if not drop_piece(board, col, player):
        continue
    
    if check_win(board, player):
        print_board(board)
        print(f"Player {player} wins!")
        break
    
    if all(board[0][c] != '.' for c in range(COLS)):
        print_board(board)
        print("Draw!")
        break
    
    current = (current + 1) % len(PLAYERS)
