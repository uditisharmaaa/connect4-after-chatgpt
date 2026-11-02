import os
import random
import string

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

if PLAYERS < 2:
    PLAYERS = 2
if PLAYERS > 5:
    PLAYERS = 5
if COLS > 26:
    COLS = 26

board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
players = CHECKERS[:PLAYERS]

def clear():
    os.system('clear')

def print_board():
    letters = string.ascii_uppercase[:COLS]
    header = "  " + "   ".join(letters)
    sep = "+" + "+".join(["---"] * COLS) + "+"
    print(header)
    print(sep)
    for r in range(ROWS):
        row = "|"
        for c in range(COLS):
            row += " " + board[r][c] + " |"
        print(row)
        print(sep)

def drop(col, ch):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = ch
            return r, col
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(r, c, ch):
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in dirs:
        count = 1
        rr, cc = r + dr, c + dc
        while in_bounds(rr, cc) and board[rr][cc] == ch:
            count += 1
            rr += dr
            cc += dc
        rr, cc = r - dr, c - dc
        while in_bounds(rr, cc) and board[rr][cc] == ch:
            count += 1
            rr -= dr
            cc -= dc
        if count >= 4:
            return True
    return False

def board_full():
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

curr = random.randint(0, PLAYERS - 1)

while True:
    clear()
    print_board()
    ch = players[curr]
    print(f"Player {ch}, please enter a column:")
    col_idx = None
    while True:
        s = input().strip().upper()
        if len(s) == 1 and 'A' <= s <= chr(ord('A') + COLS - 1):
            col_idx = ord(s) - ord('A')
            break
        else:
            print("Invalid input. Please enter a valid column letter:")
    if board[0][col_idx] != " ":
        # column full, lose turn
        curr = (curr + 1) % PLAYERS
        continue
    pos = drop(col_idx, ch)
    if pos:
        r, c = pos
        if check_win(r, c, ch):
            clear()
            print_board()
            print(f"Player {ch} won!")
            break
        if board_full():
            clear()
            print_board()
            print("It's a draw!")
            break
    curr = (curr + 1) % PLAYERS
