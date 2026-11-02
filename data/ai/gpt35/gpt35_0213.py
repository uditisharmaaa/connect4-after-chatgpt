import os, random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear(): os.system('clear')

def create_board(): return [[' ']*COLS for _ in range(ROWS)]

def print_board(board):
    clear()
    print('  ' + '   '.join(chr(ord('A')+i) for i in range(COLS)))
    print('+' + '---+'*COLS)
    for row in board:
        print('|' + '|'.join(f' {c} ' for c in row) + '|')
        print('+' + '---+'*COLS)

def valid_col(c):
    return len(c) == 1 and 'A' <= c <= chr(ord('A')+COLS-1)

def get_column_index(c):
    return ord(c) - ord('A')

def can_place(board, col):
    return board[0][col] == ' '

def place_checker(board, col, checker):
    for r in reversed(range(ROWS)):
        if board[r][col] == ' ':
            board[r][col] = checker
            return r, col

def win_check(board, r, c, checker):
    def count_dir(dr, dc):
        count = 0
        rr, cc = r+dr, c+dc
        while 0 <= rr < ROWS and 0 <= cc < COLS and board[rr][cc] == checker:
            count += 1
            rr += dr
            cc += dc
        return count
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        if count_dir(dr, dc) + count_dir(-dr, -dc) +1 >=4:
            return True
    return False

def board_full(board):
    return all(board[0][c] != ' ' for c in range(COLS))

board = create_board()
players = CHECKERS[:PLAYERS]
current = random.randint(0, PLAYERS-1)

print_board(board)
while True:
    p = players[current]
    move = input(f"Player {p}, please enter a column: ").upper()
    if not valid_col(move):
        continue
    col = get_column_index(move)
    if not can_place(board, col):
        current = (current +1) % PLAYERS
        continue
    r, c = place_checker(board, col, p)
    print_board(board)
    if win_check(board, r, c, p):
        print(f"Player {p} won!")
        break
    if board_full(board):
        print("Game is a draw!")
        break
    current = (current +1) % PLAYERS
