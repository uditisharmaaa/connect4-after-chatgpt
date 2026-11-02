import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def initialize_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Print column headers
    headers = [chr(65 + i) for i in range(COLS)]
    print('  ' + '   '.join(headers))
    
    # Print board rows
    border = '+' + ('---+' * COLS)
    for row in board:
        print(border)
        print('| ' + ' | '.join(row) + ' |')
    print(border)

def get_valid_column(board):
    while True:
        col = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col) != 1 or not col.isalpha() or ord(col) - 65 >= COLS:
            print("Invalid column. Please enter a valid column letter.")
            continue
        col_idx = ord(col) - 65
        if board[0][col_idx] != ' ':
            print("Column is full. Choose another column.")
            continue
        return col_idx

def drop_checker(board, col_idx, checker):
    for row in reversed(range(ROWS)):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return row
    return -1

def check_win(board, row, col):
    directions = [
        (0, 1),  # horizontal
        (1, 0),  # vertical
        (1, 1),  # diagonal down-right
        (1, -1), # diagonal down-left
    ]
    checker = board[row][col]
    for dr, dc in directions:
        count = 1
        for step in [1, -1]:
            r, c = row, col
            for _ in range(3):
                r += dr * step
                c += dc * step
                if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(cell != ' ' for cell in board[0])

def main():
    global current_player
    board = initialize_board()
    current_player = random.randint(0, PLAYERS - 1)
    clear_screen()
    print_board(board)
    
    while True:
        col_idx = get_valid_column(board)
        row = drop_checker(board, col_idx, CHECKERS[current_player])
        clear_screen()
        print_board(board)
        
        if check_win(board, row, col_idx):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        if is_draw(board):
            print("Game ended in a draw!")
            break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
