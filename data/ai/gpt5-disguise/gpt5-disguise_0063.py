import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2

SYMS = ["X", "O", "V", "H", "M"]

if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    NUM_PLAYERS = 2
if COLS < 1 or COLS > 26:
    COLS = 7
if ROWS < 1:
    ROWS = 6

players = SYMS[:NUM_PLAYERS]
board = [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board():
    os.system('clear')
    letters = [string.ascii_uppercase[i] for i in range(COLS)]
    print("  " + "   ".join(letters))
    print("+---" * COLS + "+")
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(board[r][c])
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def drop(col, sym):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = sym
            return r
    return -1

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def count_dir(r, c, dr, dc, sym):
    cnt = 0
    rr, cc = r, c
    while in_bounds(rr, cc) and board[rr][cc] == sym:
        cnt += 1
        rr += dr
        cc += dc
    return cnt

def won(r, c, sym):
    # horizontal
    a = count_dir(r, c, 0, -1, sym) + count_dir(r, c, 0, 1, sym) - 1
    if a >= 4:
        return True
    # vertical
    a = count_dir(r, c, -1, 0, sym) + count_dir(r, c, 1, 0, sym) - 1
    if a >= 4:
        return True
    # diag \
    a = count_dir(r, c, -1, -1, sym) + count_dir(r, c, 1, 1, sym) - 1
    if a >= 4:
        return True
    # diag /
    a = count_dir(r, c, -1, 1, sym) + count_dir(r, c, 1, -1, sym) - 1
    if a >= 4:
        return True
    return False

def full():
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

current = random.randint(0, NUM_PLAYERS - 1)

# initial board print before game starts
print_board()

while True:
    sym = players[current]
    col = None
    while True:
        inp = input(f"Player {sym}, please enter a column: ").strip().upper()
        if len(inp) == 1 and "A" <= inp <= chr(ord("A") + COLS - 1):
            col = ord(inp) - ord("A")
            break
        else:
            print("Invalid input. Please enter a valid column letter.")
    row_placed = drop(col, sym)
    if row_placed == -1:
        # column full, turn lost
        current = (current + 1) % NUM_PLAYERS
        print_board()
        continue
    # print updated board and check win/draw
    print_board()
    if won(row_placed, col, sym):
        print(f"Player {sym} won!")
        break
    if full():
        print("It's a draw!")
        break
    current = (current + 1) % NUM_PLAYERS
