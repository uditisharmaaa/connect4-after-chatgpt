import random
import os
import sys

# settings
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
SYMS = ["X", "O", "V", "H", "M"]
WIN = 4

if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    print("Number of players must be between 2 and 5.")
    sys.exit(1)
if COLS > 26:
    COLS = 26

players = SYMS[:NUM_PLAYERS]

board = [[" " for _ in range(COLS)] for _ in range(ROWS)]

letters = [chr(ord('A') + i) for i in range(COLS)]

def clear():
    os.system('clear')

def print_board():
    print("  " + "   ".join(letters))
    line = "+" + "---+" * COLS
    for r in range(ROWS):
        print(line)
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(line)

def col_from_input(s):
    if len(s) != 1:
        return None
    ch = s.upper()
    if ch < 'A' or ch >= chr(ord('A') + COLS):
        return None
    return ord(ch) - ord('A')

def first_empty_row(c):
    for r in range(ROWS - 1, -1, -1):
        if board[r][c] == " ":
            return r
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_dir(r, c, dr, dc, sym):
    cnt = 0
    rr, cc = r, c
    while in_bounds(rr, cc) and board[rr][cc] == sym:
        cnt += 1
        rr += dr
        cc += dc
    return cnt

def check_win(r, c, sym):
    # horizontal
    total = check_dir(r, c, 0, -1, sym) + check_dir(r, c, 0, 1, sym) - 1
    if total >= WIN:
        return True
    # vertical
    total = check_dir(r, c, -1, 0, sym) + check_dir(r, c, 1, 0, sym) - 1
    if total >= WIN:
        return True
    # diag down-right / up-left
    total = check_dir(r, c, -1, -1, sym) + check_dir(r, c, 1, 1, sym) - 1
    if total >= WIN:
        return True
    # diag up-right / down-left
    total = check_dir(r, c, -1, 1, sym) + check_dir(r, c, 1, -1, sym) - 1
    if total >= WIN:
        return True
    return False

def is_draw():
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

cur = random.randint(0, NUM_PLAYERS - 1)

while True:
    clear()
    print_board()
    s = input(f"Player {players[cur]}, please enter a column: ").strip().upper()
    while col_from_input(s) is None:
        clear()
        print_board()
        s = input(f"Player {players[cur]}, please enter a column: ").strip().upper()
    col = col_from_input(s)
    r = first_empty_row(col)
    if r is None:
        # column full, lose turn
        cur = (cur + 1) % NUM_PLAYERS
        # check for draw even if no placement
        if is_draw():
            clear()
            print_board()
            print("It's a draw!")
            break
        continue
    board[r][col] = players[cur]
    if check_win(r, col, players[cur]):
        clear()
        print_board()
        print(f"Player {players[cur]} won!")
        break
    if is_draw():
        clear()
        print_board()
        print("It's a draw!")
        break
    cur = (cur + 1) % NUM_PLAYERS
