import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2

SYMS_ALL = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = max(2, min(5, NUM_PLAYERS))
COLS = max(1, min(26, COLS))
board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
syms = SYMS_ALL[:NUM_PLAYERS]

def print_board():
    os.system('clear')
    header = '  ' + '   '.join(chr(ord('A') + i) for i in range(COLS))
    print(header)
    line = '+' + '---+' * COLS
    for r in range(ROWS):
        print(line)
        row_str = '|'
        for c in range(COLS):
            row_str += ' ' + board[r][c] + ' |'
        print(row_str)
    print(line)

def place(col, sym):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = sym
            return r
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(sym):
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != sym:
                continue
            for dr, dc in dirs:
                ok = True
                for k in range(1,4):
                    rr = r + dr*k
                    cc = c + dc*k
                    if not in_bounds(rr, cc) or board[rr][cc] != sym:
                        ok = False
                        break
                if ok:
                    return True
    return False

def board_full():
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == ' ':
                return False
    return True

cur = random.randint(0, NUM_PLAYERS - 1)

while True:
    print_board()
    print(f"Player {syms[cur]}, please enter a column:")
    col = None
    while True:
        s = input().strip()
        if len(s) == 1 and s.isalpha():
            ch = s.upper()
            idx = ord(ch) - ord('A')
            if 0 <= idx < COLS:
                col = idx
                break
        print("Invalid input. Please enter a valid column:")
    row = place(col, syms[cur])
    if row is not None:
        if check_win(syms[cur]):
            print_board()
            print(f"Player {syms[cur]} won!")
            break
        if board_full():
            print_board()
            print("It's a draw!")
            break
    cur = (cur + 1) % NUM_PLAYERS
