import random
import os
import sys

ROWS = 6
COLS = 7
PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]
WIN_LEN = 4

if PLAYERS < 2 or PLAYERS > 5:
    print("PLAYERS must be between 2 and 5")
    sys.exit(1)
if COLS < 1 or COLS > 26:
    print("COLS must be between 1 and 26")
    sys.exit(1)

board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
players = TOKENS[:PLAYERS]
cols_labels = [chr(ord('A') + i) for i in range(COLS)]

def clear():
    os.system('clear')

def print_board():
    clear()
    header = "  " + "   ".join(cols_labels)
    print(header)
    print("+" + "---+" * COLS)
    for r in range(ROWS):
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
        print("+" + "---+" * COLS)

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win_token(t):
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != t:
                continue
            for dr, dc in dirs:
                cnt = 1
                rr, cc = r + dr, c + dc
                while cnt < WIN_LEN and in_bounds(rr, cc) and board[rr][cc] == t:
                    cnt += 1
                    rr += dr
                    cc += dc
                if cnt >= WIN_LEN:
                    return True
    return False

def is_draw():
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def drop_token(col_idx, t):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = t
            return True
    return False

current = random.randint(0, PLAYERS - 1)
game_over = False

while not game_over:
    print_board()
    print(f"Player {players[current]}, please enter a column:")
    col_input = input().strip()
    while True:
        if len(col_input) != 1:
            print("Invalid input. Please enter a single uppercase letter for the column:")
        else:
            ch = col_input.upper()
            if 'A' <= ch <= chr(ord('A') + COLS - 1):
                col = ord(ch) - ord('A')
                break
            else:
                print("Invalid input. Please enter a valid column letter:")
        col_input = input().strip()

    placed = drop_token(col, players[current])
    if not placed:
        print("Column full, turn lost.")
    else:
        if check_win_token(players[current]):
            print_board()
            print(f"Player {players[current]} won!")
            break
        if is_draw():
            print_board()
            print("It's a draw!")
            break

    current = (current + 1) % PLAYERS
