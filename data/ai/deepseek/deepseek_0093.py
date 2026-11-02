import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print(' ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    border = '+' + ('---+' * COLS)
    print(border)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print(border)

def is_valid_column(col, board):
    if len(col) != 1 or not col.isalpha():
        return False
    idx = ord(col.upper()) - ord('A')
    return 0 <= idx < COLS and board[0][idx] == ' '

def place_checker(board, col, symbol):
    idx = ord(col.upper()) - ord('A')
    for row in reversed(range(ROWS)):
        if board[row][idx] == ' ':
            board[row][idx] = symbol
            return row, idx
    return None

def check_win(board, row, col):
    symbol = board[row][col]
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        for step in [1, -1]:
            r, c = row + step * dr, col + step * dc
            while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
                count += 1
                r += step * dr
                c += step * dc
                if count == 4:
                    return True
    return False

def is_draw(board):
    return all(cell != ' ' for cell in board[0])

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    symbols = PLAYER_SYMBOLS[:PLAYERS]
    print_board(board)
    
    while True:
        symbol = symbols[current_player]
        col = input(f"Player {symbol}, please enter a column: ").upper()
        
        if not is_valid_column(col, board):
            continue
            
        pos = place_checker(board, col, symbol)
        print_board(board)
        
        if pos and check_win(board, pos[0], pos[1]):
            print(f"Player {symbol} won!")
            break
        elif is_draw(board):
            print("Game ended in a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
