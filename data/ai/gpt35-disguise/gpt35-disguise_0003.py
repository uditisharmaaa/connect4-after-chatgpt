import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(' ')
        board.append(row)
    return board

def print_board(board):
    clear_screen()
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print('  ' + '   '.join(letters))
    print('+' + '---+' * COLS)
    for r in range(ROWS):
        row_str = '|'
        for c in range(COLS):
            row_str += ' ' + board[r][c] + ' |'
        print(row_str)
        print('+' + '---+' * COLS)

def get_column_index(col_str):
    if len(col_str) != 1:
        return -1
    if col_str < 'A' or col_str > chr(ord('A') + COLS -1):
        return -1
    return ord(col_str) - ord('A')

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = checker
            return r
    return -1

def check_win(board, row, col, checker):
    # horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # diagonal top-left to bottom-right
    start_r = row
    start_c = col
    while start_r > 0 and start_c > 0:
        start_r -=1
        start_c -=1
    count = 0
    while start_r < ROWS and start_c < COLS:
        if board[start_r][start_c] == checker:
            count +=1
            if count == 4:
                return True
        else:
            count = 0
        start_r +=1
        start_c +=1
    # diagonal bottom-left to top-right
    start_r = row
    start_c = col
    while start_r < ROWS -1 and start_c > 0:
        start_r +=1
        start_c -=1
    count = 0
    while start_r >=0 and start_c < COLS:
        if board[start_r][start_c] == checker:
            count +=1
            if count == 4:
                return True
        else:
            count = 0
        start_r -=1
        start_c +=1
    return False

def board_full(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == ' ':
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.randint(0, NUM_PLAYERS -1)
    print_board(board)
    while True:
        print('Player {}, please enter a column:'.format(players[current_player]))
        col_str = input().strip().upper()
        col = get_column_index(col_str)
        if col == -1:
            continue
        row = place_checker(board, col, players[current_player])
        if row == -1:
            # column full, lose turn
            current_player = (current_player +1) % NUM_PLAYERS
            print_board(board)
            continue
        print_board(board)
        if check_win(board, row, col, players[current_player]):
            print('Player {} won!'.format(players[current_player]))
            break
        if board_full(board):
            print('Draw!')
            break
        current_player = (current_player +1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
