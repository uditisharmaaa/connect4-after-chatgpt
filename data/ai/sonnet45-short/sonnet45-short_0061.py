import os
import random

ROWS, COLS = 6, 7
PLAYERS = ['X', 'O']  # Change to ['X', 'O', 'V', 'H'] for more players

def print_board(board):
    os.system('clear')
    print('  A B C D E F G')
    for r in range(ROWS):
        print(r + 1, ' '.join(board[r]))
    print()

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
                # Diagonal down-right
                if r <= ROWS - 4 and c <= COLS - 4 and all(board[r+i][c+i] == player for i in range(4)):
                    return True
                # Diagonal up-right
                if r >= 3 and c <= COLS - 4 and all(board[r-i][c+i] == player for i in range(4)):
                    return True
    return False

def drop_piece(board, col, player):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == '.':
            board[r][col] = player
            return True
    return False

def play():
    board = [['.' for _ in range(COLS)] for _ in range(ROWS)]
    turn = random.randint(0, len(PLAYERS) - 1)
    moves = 0
    
    while True:
        print_board(board)
        player = PLAYERS[turn]
        print(f"Player {player}'s turn")
        
        col_input = input("Enter column (A-G): ").upper()
        if col_input not in 'ABCDEFG':
            print("Invalid column!")
            input("Press Enter...")
            continue
        
        col = ord(col_input) - ord('A')
        
        if not drop_piece(board, col, player):
            print("Column full!")
            input("Press Enter...")
            continue
        
        moves += 1
        
        if check_win(board, player):
            print_board(board)
            print(f"Player {player} wins!")
            break
        
        if moves == ROWS * COLS:
            print_board(board)
            print("Draw!")
            break
        
        turn = (turn + 1) % len(PLAYERS)

play()
