import os
import random
import sys

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]

if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    print("NUM_PLAYERS must be between 2 and 5")
    sys.exit(1)
if COLS > 26:
    print("COLS must be at most 26")
    sys.exit(1)

players = TOKENS[:NUM_PLAYERS]

board = [[" " for _ in range(COLS)] for _ in range(ROWS)]

def clear():
    os.system('clear')

def print_board():
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    print("+" + "---+" * COLS)
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(board[r][c])
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def drop_token(col, token):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(r, c, token):
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

def board_full():
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

curr = random.randrange(NUM_PLAYERS)
game_over = False

clear()
print_board()

while not game_over:
    token = players[curr]
    valid_input = False
    lost_turn = False
    while not valid_input:
        s = input(f"Player {token}, please enter a column: ").strip().upper()
        if len(s) != 1 or not s.isalpha():
            continue
        col = ord(s) - ord('A')
        if col < 0 or col >= COLS:
            continue
        row = drop_token(col, token)
        if row is None:
            print("Column is full. Turn lost.")
            lost_turn = True
        valid_input = True

    clear()
    print_board()

    if not lost_turn:
        if check_win(row, col, token):
            print(f"Player {token} won!")
            break
        if board_full():
            print("Draw!")
            break

    curr = (curr + 1) % NUM_PLAYERS
