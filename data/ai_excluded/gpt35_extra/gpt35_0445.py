import os, random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear(): os.system('clear')

def create_board():
    return [[' ']*COLS for _ in range(ROWS)]

def print_board(board):
    clear()
    print('  ' + '   '.join(chr(ord('A')+i) for i in range(COLS)))
    print('+---'*COLS + '+')
    for row in board:
        print('|' + '|'.join(f' {c} ' for c in row) + '|')
        print('+---'*COLS + '+')

def valid_column(c):
    return len(c) == 1 and 'A' <= c <= chr(ord('A')+COLS-1)

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = checker
            return r
    return -1

def check_win(board, r, c, checker):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for d in [1,-1]:
            nr, nc = r, c
            while True:
                nr += dr*d
                nc += dc*d
                if 0<=nr<ROWS and 0<=nc<COLS and board[nr][nc] == checker:
                    count += 1
                else: break
        if count>=4: return True
    return False

def full_board(board):
    return all(cell != ' ' for row in board for cell in row)

board = create_board()
players = CHECKERS[:PLAYERS]
current = random.randint(0, PLAYERS-1)
print_board(board)

while True:
    checker = players[current]
    col_input = input(f'Player {checker}, please enter a column: ').strip().upper()
    if not valid_column(col_input):
        continue
    col = ord(col_input) - ord('A')
    r = place_checker(board, col, checker)
    if r == -1:
        current = (current + 1) % PLAYERS
        print_board(board)
        continue
    print_board(board)
    if check_win(board, r, col, checker):
        print(f'Player {checker} won!')
        break
    if full_board(board):
        print('Draw!')
        break
    current = (current + 1) % PLAYERS
