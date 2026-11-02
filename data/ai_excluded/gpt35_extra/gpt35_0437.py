import os, random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X','O','V','H','M']
WIN = 4

def clear(): os.system('clear')

def create_board():
    return [[' ']*COLS for _ in range(ROWS)]

def print_board(board):
    clear()
    print('  ' + '   '.join(chr(ord('A')+i) for i in range(COLS)))
    print('+' + '---+'*COLS)
    for row in board:
        print('|' + '|'.join(f' {c} ' for c in row) + '|')
        print('+' + '---+'*COLS)

def input_column(player_char):
    while True:
        col = input(f"Player {player_char}, please enter a column: ").strip().upper()
        if len(col)!=1 or not ('A' <= col <= chr(ord('A')+COLS-1)):
            continue
        idx = ord(col)-ord('A')
        if board[0][idx] != ' ':  # column full, lose turn
            return -1
        return idx

def place_checker(board, col, checker):
    for r in range(ROWS-1,-1,-1):
        if board[r][col] == ' ':
            board[r][col] = checker
            return r, col

def check_win(board, r, c, checker):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        count = 1
        for sign in (1,-1):
            nr, nc = r, c
            while True:
                nr += dr*sign
                nc += dc*sign
                if 0<=nr<ROWS and 0<=nc<COLS and board[nr][nc]==checker:
                    count +=1
                else:
                    break
            if count>=WIN: return True
    return False

def full_board(board):
    return all(board[0][c]!=' ' for c in range(COLS))

board = create_board()
players = CHECKERS[:PLAYERS]
current = random.randint(0,PLAYERS-1)
print_board(board)

while True:
    checker = players[current]
    col = input_column(checker)
    if col == -1:
        current = (current+1)%PLAYERS
        continue
    r,c = place_checker(board,col,checker)
    print_board(board)
    if check_win(board,r,c,checker):
        print(f"Player {checker} won!")
        break
    if full_board(board):
        print("Draw!")
        break
    current = (current+1)%PLAYERS
