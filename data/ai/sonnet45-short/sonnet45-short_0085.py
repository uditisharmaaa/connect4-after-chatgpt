import os
import random

ROWS, COLS = 6, 7
PLAYERS = ['X', 'O']  # Change to ['X', 'O', 'V', 'H', 'M'] for more players

def print_board(board):
    os.system('clear')
    print('  A B C D E F G')
    for r in range(ROWS):
        print(r + 1, ' '.join(board[r]))
    print()

def drop_piece(board, col, player):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == '.':
            board[r][col] = player
            return r
    return -1

def check_win(board, r, c, player):
    def check_line(dr, dc):
        count = 0
        for i in range(-3, 4):
            nr, nc = r + i * dr, c + i * dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
        return False
    
    return any(check_line(dr, dc) for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)])

def is_draw(board):
    return all(board[0][c] != '.' for c in range(COLS))

def main():
    board = [['.' for _ in range(COLS)] for _ in range(ROWS)]
    current = random.choice(PLAYERS)
    
    while True:
        print_board(board)
        print(f"Player {current}'s turn")
        col_input = input("Enter column (A-G): ").strip().upper()
        
        if len(col_input) != 1 or col_input not in 'ABCDEFG':
            print("Invalid input! Press Enter...")
            input()
            continue
        
        col = ord(col_input) - ord('A')
        row = drop_piece(board, col, current)
        
        if row == -1:
            print("Column full! Press Enter...")
            input()
            continue
        
        if check_win(board, row, col, current):
            print_board(board)
            print(f"Player {current} wins!")
            break
        
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        current = PLAYERS[(PLAYERS.index(current) + 1) % len(PLAYERS)]

if __name__ == '__main__':
    main()
