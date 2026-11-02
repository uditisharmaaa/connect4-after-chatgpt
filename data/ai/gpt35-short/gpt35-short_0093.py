import os, random

ROWS, COLS = 6, 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # up to 5
COL_LABELS = 'ABCDEFG'

def clear(): os.system('clear')

def create_board():
    return [[' ']*COLS for _ in range(ROWS)]

def print_board(b):
    print('  ' + ' '.join(COL_LABELS))
    for row in b:
        print('|'+ '|'.join(row) + '|')
    print('+'.join(['-']*(COLS*2+1)))

def get_move(player, playerset):
    while True:
        move = input(f"Player {player}'s turn [{','.join(playerset)}] (A-G): ").upper()
        if move in COL_LABELS:
            c = COL_LABELS.index(move)
            if board[0][c] == ' ':
                return c
            else:
                print("Column full! Try again.")
        else:
            print("Invalid input! Choose A-G.")

def drop_piece(board, col, player):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = player
            return r, col

def check_win(b, r, c):
    p = b[r][c]
    directions = [(1,0), (0,1), (1,1), (1,-1)]
    for dr, dc in directions:
        count = 1
        for d in (1, -1):
            nr, nc = r, c
            while True:
                nr += dr*d
                nc += dc*d
                if 0 <= nr < ROWS and 0 <= nc < COLS and b[nr][nc] == p:
                    count +=1
                else:
                    break
        if count >= 4:
            return True
    return False

def check_draw(b):
    return all(b[0][c] != ' ' for c in range(COLS))

# --- Game setup ---
num_players = 0
while num_players < 2 or num_players > 5:
    try:
        num_players = int(input("Number of players (2-5): "))
    except:
        continue
playerset = PLAYERS[:num_players]
board = create_board()
current = random.choice(playerset)

# --- Game loop ---
clear()
while True:
    print_board(board)
    col = get_move(current, playerset)
    r, c = drop_piece(board, col, current)
    clear()
    if check_win(board, r, c):
        print_board(board)
        print(f"Player {current} wins!")
        break
    if check_draw(board):
        print_board(board)
        print("Game is a draw!")
        break
    current = playerset[(playerset.index(current)+1)%num_players]
