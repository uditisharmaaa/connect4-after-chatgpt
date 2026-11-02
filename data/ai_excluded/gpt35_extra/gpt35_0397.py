import os, random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear(): os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear()
    print('  ' + '   '.join(chr(ord('A')+i) for i in range(COLS)))
    print('+' + '---+'*COLS)
    for row in board:
        print('|' + '|'.join(f' {c} ' for c in row) + '|')
        print('+' + '---+'*COLS)

def valid_input(s):
    return len(s) == 1 and 'A' <= s <= chr(ord('A')+COLS-1)

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = checker
            return r, col
    return -1, -1

def check_win(board, r, c, ch):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for sign in [1,-1]:
            nr, nc = r, c
            while True:
                nr += dr*sign
                nc += dc*sign
                if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == ch:
                    count +=1
                else:
                    break
        if count >=4:
            return True
    return False

def full_board(board):
    return all(board[0][c] != ' ' for c in range(COLS))

board = create_board()
players = CHECKERS[:PLAYERS]
current = random.randrange(PLAYERS)
print_board(board)

while True:
    ch = players[current]
    while True:
        col_input = input(f'Player {ch}, please enter a column: ').upper()
        if not valid_input(col_input):
            continue
        col = ord(col_input) - ord('A')
        r, c = place_checker(board, col, ch)
        if r == -1:
            current = (current +1) % PLAYERS  # lose turn
            break
        print_board(board)
        if check_win(board, r, c, ch):
            print(f'Player {ch} won!')
            exit()
        if full_board(board):
            print('Draw!')
            exit()
        current = (current +1) % PLAYERS
        break
