import random
import os

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
SYMS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(b):
    os.system('clear')
    letters = [chr(ord('A') + i) for i in range(len(b[0]))]
    print("  " + "   ".join(letters))
    print("+" + "---+" * len(b[0]))
    for r in range(len(b)):
        row = []
        for c in range(len(b[0])):
            row.append(b[r][c])
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(b[0]))

def col_full(b, c):
    return b[0][c] != " "

def drop_piece(b, c, s):
    for r in range(len(b) - 1, -1, -1):
        if b[r][c] == " ":
            b[r][c] = s
            return r, c
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_dir(b, r, c, dr, dc, s):
    for k in range(4):
        rr = r + dr * k
        cc = c + dc * k
        if not in_bounds(rr, cc):
            return False
        if b[rr][cc] != s:
            return False
    return True

def check_win(b, s):
    for r in range(ROWS):
        for c in range(COLS):
            if b[r][c] != s:
                continue
            if check_dir(b, r, c, 0, 1, s):
                return True
            if check_dir(b, r, c, 1, 0, s):
                return True
            if check_dir(b, r, c, 1, 1, s):
                return True
            if check_dir(b, r, c, -1, 1, s):
                return True
    return False

def board_full(b):
    for c in range(COLS):
        if b[0][c] == " ":
            return False
    return True

def get_col_input():
    while True:
        s = input("Player " + current_sym + ", please enter a column: ").strip()
        if len(s) != 1:
            continue
        ch = s.upper()
        if not ('A' <= ch <= 'Z'):
            continue
        idx = ord(ch) - ord('A')
        if 0 <= idx < COLS:
            return idx

board = make_board(ROWS, COLS)
current = random.randrange(NUM_PLAYERS)
while True:
    current_sym = SYMS[current]
    print_board(board)
    c = get_col_input()
    if col_full(board, c):
        # loses the turn
        current = (current + 1) % NUM_PLAYERS
        continue
    drop_piece(board, c, current_sym)
    if check_win(board, current_sym):
        print_board(board)
        print("Player " + current_sym + " won!")
        break
    if board_full(board):
        print_board(board)
        print("It's a draw!")
        break
    current = (current + 1) % NUM_PLAYERS
