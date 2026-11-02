import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    for row in board:
        print('+' + '---+' * COLS)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+' + '---+' * COLS)

def is_valid_column(col, board):
    if not col or len(col) != 1:
        return False
    col = col.upper()
    if not 'A' <= col <= chr(65 + COLS - 1):
        return False
    col_idx = ord(col) - ord('A')
    return board[0][col_idx] == ' '

def place_checker(board, col, symbol):
    col_idx = ord(col.upper()) - ord('A')
    for row in reversed(range(ROWS)):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = symbol
            return row, col_idx
    return None

def check_win(board, row, col):
    symbol = board[row][col]
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        for step in [1, -1]:
            r, c = row, col
            for _ in range(3):
                r += dr * step
                c += dc * step
                if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = initialize_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)
    
    while True:
        symbol = PLAYER_SYMBOLS[current_player]
        print(f"Player {symbol}, please enter a column: ", end='')
        col = input().strip().upper()
        
        if not is_valid_column(col, board):
            print("Invalid input. Try again.")
            continue
        
        pos = place_checker(board, col, symbol)
        print_board(board)
        
        if check_win(board, pos[0], pos[1]):
            print(f"Player {symbol} won!")
            break
        
        if is_draw(board):
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
