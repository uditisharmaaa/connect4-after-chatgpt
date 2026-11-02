import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        row = []
        for _ in range(COLS):
            row.append(' ')
        board.append(row)
    return board

def print_board(board):
    clear_screen()
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    print(' ', end=' ')
    for i in range(COLS):
        print(letters[i], end='   ')
    print()
    print('+' + '---+' * COLS)
    for r in range(ROWS):
        print('|', end='')
        for c in range(COLS):
            print(' ' + board[r][c] + ' |', end='')
        print()
        print('+' + '---+' * COLS)

def valid_input(inp):
    if len(inp) != 1:
        return False
    if inp < 'A' or inp > chr(ord('A') + COLS - 1):
        return False
    return True

def get_column(inp):
    return ord(inp) - ord('A')

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = checker
            return r, col
    return -1, -1

def check_win(board, r, c, checker):
    # check horizontal
    count = 0
    for col in range(max(c-3,0), min(c+4,COLS)):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # check vertical
    count = 0
    for row in range(max(r-3,0), min(r+4,ROWS)):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # check diagonal \
    count = 0
    start_row = r - min(3, r, c)
    start_col = c - min(3, r, c)
    while start_row < ROWS and start_col < COLS:
        if board[start_row][start_col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        start_row += 1
        start_col += 1
    # check diagonal /
    count = 0
    start_row = r + min(3, ROWS - 1 - r, c)
    start_col = c - min(3, ROWS - 1 - r, c)
    while start_row >= 0 and start_col < COLS:
        if board[start_row][start_col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        start_row -= 1
        start_col += 1

    return False

def board_full(board):
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True

def main():
    board = create_board()
    checkers = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS - 1)
    while True:
        print_board(board)
        print('Player ' + checkers[current] + ', please enter a column:')
        inp = input().strip().upper()
        if not valid_input(inp):
            continue
        col = get_column(inp)
        r, c = place_checker(board, col, checkers[current])
        if r == -1:
            # column full, lose turn
            current = (current + 1) % PLAYERS
            continue
        if check_win(board, r, c, checkers[current]):
            print_board(board)
            print('Player ' + checkers[current] + ' won!')
            break
        if board_full(board):
            print_board(board)
            print('The game is a draw!')
            break
        current = (current + 1) % PLAYERS

if __name__ == '__main__':
    main()
