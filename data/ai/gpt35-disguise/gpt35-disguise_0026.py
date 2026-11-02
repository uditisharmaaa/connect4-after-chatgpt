import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2

CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear():
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
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print('  ' + '   '.join(letters))
    line = '+---' * COLS + '+'
    for r in range(ROWS):
        print(line)
        row_str = '|'
        for c in range(COLS):
            row_str += ' ' + board[r][c] + ' |'
        print(row_str)
    print(line)

def valid_column(inp, board):
    if len(inp) != 1:
        return False
    if not ('A' <= inp <= chr(ord('A') + COLS -1)):
        return False
    col = ord(inp) - ord('A')
    if board[0][col] != ' ':
        return False
    return True

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = checker
            return r, col
    return -1, -1

def check_win(board, r, c, checker):
    # horizontal
    count = 0
    for col in range(max(0, c-3), min(COLS, c+4)):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # vertical
    count = 0
    for row in range(max(0, r-3), min(ROWS, r+4)):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # diagonal /
    count = 0
    for i in range(-3,4):
        rr = r + i
        cc = c - i
        if 0 <= rr < ROWS and 0 <= cc < COLS:
            if board[rr][cc] == checker:
                count +=1
                if count ==4:
                    return True
            else:
                count =0
        else:
            count=0
    # diagonal \
    count = 0
    for i in range(-3,4):
        rr = r + i
        cc = c + i
        if 0 <= rr < ROWS and 0 <= cc < COLS:
            if board[rr][cc] == checker:
                count +=1
                if count ==4:
                    return True
            else:
                count =0
        else:
            count=0
    return False

def full_board(board):
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)

    while True:
        clear()
        print_board(board)
        print('Player ' + players[current] + ', please enter a column:')
        inp = input().strip().upper()
        if not valid_column(inp, board):
            print('Invalid column, try again.')
            input('Press enter to continue...')
            continue
        col = ord(inp) - ord('A')
        row, col_placed = place_checker(board, col, players[current])
        if row == -1:
            # column full - turn lost
            current = (current + 1) % PLAYERS
            continue
        if check_win(board, row, col_placed, players[current]):
            clear()
            print_board(board)
            print('Player ' + players[current] + ' won!')
            break
        if full_board(board):
            clear()
            print_board(board)
            print('Draw!')
            break
        current = (current + 1) % PLAYERS

main()
