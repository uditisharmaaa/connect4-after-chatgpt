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

def input_column(player):
    while True:
        col = input(f"Player {CHECKERS[player]}, please enter a column: ").strip().upper()
        if len(col) != 1 or not('A' <= col <= chr(ord('A')+COLS-1)):
            continue
        col_idx = ord(col) - ord('A')
        # check if column full
        if all(board[r][col_idx] != ' ' for r in range(ROWS)):
            return None
        return col_idx

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = checker
            return r, col

def check_line(board, r, c, dr, dc):
    start = board[r][c]
    for i in range(1,4):
        nr, nc = r+dr*i, c+dc*i
        if nr<0 or nr>=ROWS or nc<0 or nc>=COLS or board[nr][nc] != start:
            return False
    return True

def check_win(board, r, c):
    if board[r][c] == ' ':
        return False
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    return any(check_line(board, r, c, dr, dc) for dr, dc in dirs)

def full_board(board):
    return all(board[0][c] != ' ' for c in range(COLS))

board = create_board()
current = random.randint(0, PLAYERS-1)
print_board(board)

while True:
    col = input_column(current)
    if col is None:
        current = (current +1) % PLAYERS
        continue
    r,c = place_checker(board, col, CHECKERS[current])
    print_board(board)
    if check_win(board, r, c):
        print(f"Player {CHECKERS[current]} won!")
        break
    if full_board(board):
        print("Game is a draw!")
        break
    current = (current +1) % PLAYERS
