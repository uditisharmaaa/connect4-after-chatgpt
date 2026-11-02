import os, random

ROWS, COLS = 6, 7
PLAYERS = ['X', 'O']

def clear(): os.system('clear')

def create_board():
    return [[' ']*COLS for _ in range(ROWS)]

def print_board(board):
    clear()
    print('  ' + '   '.join(chr(65+i) for i in range(COLS)))
    print('+' + '---+'*COLS)
    for row in board:
        print('|' + '|'.join(f' {c} ' for c in row) + '|')
        print('+' + '---+'*COLS)

def valid_col(c):
    return 0 <= c < COLS

def get_col_input(player):
    while True:
        col = input(f'Player {player}, please enter a column: ').strip().upper()
        if len(col)==1 and 'A' <= col <= chr(64+COLS):
            c = ord(col)-65
            return c
        print('Invalid input.')

def place_checker(board, col, checker):
    for r in reversed(range(ROWS)):
        if board[r][col] == ' ':
            board[r][col] = checker
            return r
    return -1

def check_win(board, r, c, checker):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        cnt = 1
        for s in [1,-1]:
            nr, nc = r, c
            while True:
                nr += s*dr
                nc += s*dc
                if 0<=nr<ROWS and 0<=nc<COLS and board[nr][nc]==checker:
                    cnt +=1
                else:
                    break
        if cnt>=4: return True
    return False

def full_board(board):
    return all(board[0][c]!=' ' for c in range(COLS))

def main():
    board = create_board()
    current = random.randint(0,len(PLAYERS)-1)
    print_board(board)
    while True:
        c = get_col_input(PLAYERS[current])
        r = place_checker(board, c, PLAYERS[current])
        if r == -1:
            # column full → lose turn
            current = (current+1)%len(PLAYERS)
            print_board(board)
            continue
        print_board(board)
        if check_win(board, r, c, PLAYERS[current]):
            print(f'Player {PLAYERS[current]} won!')
            break
        if full_board(board):
            print('Draw!')
            break
        current = (current+1)%len(PLAYERS)

if __name__=="__main__":
    main()
