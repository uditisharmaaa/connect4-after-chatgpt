import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    print('+' + '---+' * COLS)
    for row in board:
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
        print('+' + '---+' * COLS)

def is_valid_column(col, board):
    if not col or len(col) != 1 or not col.isalpha():
        return False
    col_idx = ord(col.upper()) - ord('A')
    return 0 <= col_idx < COLS and board[0][col_idx] == ' '

def place_checker(col, board, checker):
    col_idx = ord(col.upper()) - ord('A')
    for row in range(ROWS-1, -1, -1):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return row, col_idx
    return None

def check_win(board, row, col):
    directions = [
        (0, 1),  # horizontal
        (1, 0),  # vertical
        (1, 1),  # diagonal down
        (1, -1)   # diagonal up
    ]
    checker = board[row][col]
    for dr, dc in directions:
        count = 1
        for step in [1, -1]:
            r, c = row + dr * step, col + dc * step
            while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
                count += 1
                r += dr * step
                c += dc * step
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        print_board(board)
        checker = PLAYERS[current_player]
        print(f"Player {checker}, please enter a column: ", end='')
        col = input().strip()
        
        if not is_valid_column(col, board):
            continue
        
        pos = place_checker(col, board, checker)
        if pos is None:
            continue
        
        if check_win(board, *pos):
            print_board(board)
            print(f"Player {checker} won!")
            break
        elif is_draw(board):
            print_board(board)
            print("Game is a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
