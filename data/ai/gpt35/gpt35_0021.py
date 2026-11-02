import os, random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear(): os.system('clear')

def create_board():
    return [[' ']*COLS for _ in range(ROWS)]

def print_board(b):
    clear()
    print('  ' + '   '.join(chr(65+i) for i in range(COLS)))
    print('+---'*COLS + '+')
    for row in b:
        print('|' + '|'.join(f' {c} ' for c in row) + '|')
        print('+---'*COLS + '+')

def valid_column(col):
    return col.isalpha() and col.upper() >= 'A' and col.upper() < chr(65+COLS)

def place_checker(b, col, checker):
    c = ord(col.upper()) - 65
    for r in range(ROWS-1, -1, -1):
        if b[r][c] == ' ':
            b[r][c] = checker
            return r, c
    return -1, -1  # column full

def check_win(b, r, c, checker):
    directions = [(1,0),(0,1),(1,1),(1,-1)]
    for dr,dc in directions:
        count = 1
        for d in [1,-1]:
            nr, nc = r, c
            while True:
                nr += dr*d
                nc += dc*d
                if 0 <= nr < ROWS and 0 <= nc < COLS and b[nr][nc] == checker:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def board_full(b):
    return all(b[0][c] != ' ' for c in range(COLS))

board = create_board()
players = CHECKERS[:PLAYERS]
current = random.randint(0, PLAYERS-1)
print_board(board)

while True:
    player = players[current]
    inp = input(f'Player {player}, please enter a column: ').strip()
    if not valid_column(inp):
        print('Invalid input, try again.')
        continue
    row, col = place_checker(board, inp, player)
    if row == -1:
        current = (current+1) % PLAYERS  # lose turn
        continue
    print_board(board)
    if check_win(board, row, col, player):
        print(f'Player {player} won!')
        break
    if board_full(board):
        print('Game is a draw!')
        break
    current = (current+1) % PLAYERS
