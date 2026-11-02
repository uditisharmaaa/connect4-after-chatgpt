import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    print('+' + '---+' * COLS)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * COLS)

def is_valid_column(col):
    return 0 <= col < COLS

def is_column_not_full(board, col):
    return board[0][col] == ' '

def drop_checker(board, col, checker):
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = checker
            return

def check_for_win(board, checker):
    def check_direction(start_row, start_col, delta_row, delta_col):
        count = 0
        row, col = start_row, start_col
        while 0 <= row < ROWS and 0 <= col < COLS:
            if board[row][col] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
            row += delta_row
            col += delta_col
        return False

    for r in range(ROWS):
        if check_direction(r, 0, 0, 1):
            return True
    for c in range(COLS):
        if check_direction(0, c, 1, 0):
            return True
    for r in range(ROWS):
        if check_direction(r, 0, -1, 1) or check_direction(r, 0, 1, 1):
            return True
    for c in range(COLS):
        if check_direction(ROWS-1, c, -1, 1) or check_direction(0, c, 1, 1):
            return True
    return False

def check_for_draw(board):
    for c in range(COLS):
        if is_column_not_full(board, c):
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.choice(range(NUM_PLAYERS))
    
    print_board(board)
    
    while True:
        current_checker = players[current_player_index]
        print(f"Player {current_checker}, please enter a column:")
        
        while True:
            try:
                column_input = input().strip()
                column_index = ord(column_input.upper()) - 65
                if is_valid_column(column_index) and is_column_not_full(board, column_index):
                    break
                else:
                    print("Invalid input, please enter a column:")
            except:
                print("Invalid input, please enter a column:")
        
        drop_checker(board, column_index, current_checker)
        print_board(board)
        
        if check_for_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        if check_for_draw(board):
            print("It's a draw!")
            break
        
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

main()
