import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    header = '  ' + '   '.join(chr(65 + i) for i in range(COLS)) + '  '
    border = '+' + ('---+' * COLS)
    print(header)
    print(border)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print(border)

def is_valid_column(col):
    return len(col) == 1 and 'A' <= col <= chr(65 + COLS - 1)

def place_checker(board, col, checker):
    col_idx = ord(col) - 65
    for row_idx in range(ROWS-1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return row_idx, col_idx
    return None

def check_win(board, row, col, checker):
    directions = [
        (0, 1),  # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1)    # Diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        for step in [1, -1]:
            r, c = row + step * dr, col + step * dc
            while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
                count += 1
                r += step * dr
                c += step * dc
                if count == 4:
                    return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)
    
    while True:
        checker = CHECKERS[current_player]
        col = input(f"Player {checker}, please enter a column: ").upper()
        
        if not is_valid_column(col):
            continue
        
        result = place_checker(board, col, checker)
        if not result:
            continue
        
        print_board(board)
        row, col = result
        
        if check_win(board, row, col, checker):
            print(f"Player {checker} won!")
            break
        
        if is_draw(board):
            print("Game ended in a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
