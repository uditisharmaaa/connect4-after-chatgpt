import random
import os
import sys

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]

if COLS > 26:
    print("Max 26 columns supported.")
    sys.exit(1)
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    print("Players must be between 2 and 5.")
    sys.exit(1)

players = TOKENS[:NUM_PLAYERS]
board = [[" " for _ in range(COLS)] for _ in range(ROWS)]

def clear():
    os.system('clear')

def print_board():
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    line = "+" + "+".join(["---"] * COLS) + "+"
    for r in range(ROWS):
        print(line)
        row = "|"
        for c in range(COLS):
            row += " " + board[r][c] + " |"
        print(row)
    print(line)

def col_from_input(s):
    s = s.strip().upper()
    if len(s) != 1:
        return None
    if not ('A' <= s <= chr(ord('A') + COLS - 1)):
        return None
    return ord(s) - ord('A')

def drop(col, token):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win_at(r, c, token):
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in dirs:
        count = 1
        rr, cc = r + dr, c + dc
        while in_bounds(rr, cc) and board[rr][cc] == token:
            count += 1
            rr += dr
            cc += dc
        rr, cc = r - dr, c - dc
        while in_bounds(rr, cc) and board[rr][cc] == token:
            count += 1
            rr -= dr
            cc -= dc
        if count >= 4:
            return True
    return False

def check_win(token):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == token and check_win_at(r, c, token):
                return True
    return False

def board_full():
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

current = random.randint(0, NUM_PLAYERS - 1)

while True:
    clear()
    print_board()
    token = players[current]
    print(f"Player {token}, please enter a column:", end=" ")
    col = None
    while True:
        s = input().strip()
        c = col_from_input(s)
        if c is None:
            print("Invalid input. Please enter a valid column letter:", end=" ")
            continue
        col = c
        break
    row = drop(col, token)
    if row is None:
        print(f"Column {chr(ord('A')+col)} is full. Turn lost.")
    else:
        if check_win(token):
            clear()
            print_board()
            print(f"Player {token} won!")
            break
        if board_full():
            clear()
            print_board()
            print("It's a draw!")
            break
    current = (current + 1) % NUM_PLAYERS
