import os
import random

ROWS, COLS = 6, 7
PLAYERS = ['X', 'O']  # Change to ['X', 'O', 'V', 'H', 'M'] for more players

def print_board(board):
    os.system('clear')
    print('  A B C D E F G')
    for i, row in enumerate(board):
        print(f"{i+1} {' '.join(row)}")

def check_win(board, player):
    # Horizontal, vertical, diagonal checks
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player:
                # Horizontal
                if c <= COLS - 4 and all(board[r][c+i] == player for i in range(4)):
                    return True
                # Vertical
                if r <= ROWS - 4 and all(board[r+i][c] == player for i in range(4)):
                    return True
                # Diagonal /
                if r <= ROWS - 4 and c <= COLS - 4 and all(board[r+i][c+i] == player for i in range(4)):
                    return True
                # Diagonal \
                if r >= 3 and c <= COLS - 4 and all(board[r-i][c+i] == player for i in range(4)):
                    return True
    return False

def drop_piece(board, col, player):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == '.':
            board[r][col] = player
            return True
    return False

board = [['.' for _ in range(COLS)] for _ in range(ROWS)]
random.shuffle(PLAYERS)

while True:
    for player in PLAYERS:
        print_board(board)
        while True:
            move = input(f"Player {player}, choose column (A-G): ").upper()
            if move in 'ABCDEFG' and drop_piece(board, ord(move) - ord('A'), player):
                break
            print("Invalid move!")
        
        if check_win(board, player):
            print_board(board)
            print(f"Player {player} wins!")
            exit()
        
        if all(board[0][c] != '.' for c in range(COLS)):
            print_board(board)
            print("Draw!")
            exit()
