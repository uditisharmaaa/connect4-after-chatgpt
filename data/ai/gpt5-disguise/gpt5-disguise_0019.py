import random
import os
import sys

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(b):
    letters = [chr(ord('A') + i) for i in range(len(b[0]))]
    print("  " + "   ".join(letters))
    line = "+" + ("---+" * len(b[0]))
    for r in range(len(b)):
        print(line)
        row = []
        for c in range(len(b[0])):
            row.append(b[r][c])
        print("| " + " | ".join(row) + " |")
    print(line)

def drop(b, col, token):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = token
            return r
    return -1

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_four(b, token):
    rows = len(b)
    cols = len(b[0])
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(rows):
        for c in range(cols):
            if b[r][c] != token:
                continue
            for dr, dc in dirs:
                cnt = 0
                rr, cc = r, c
                while in_bounds(rr, cc, rows, cols) and b[rr][cc] == token:
                    cnt += 1
                    if cnt == 4:
                        return True
                    rr += dr
                    cc += dc
    return False

def full(b):
    for r in b:
        for x in r:
            if x == " ":
                return False
    return True

def get_col_input(max_col):
    last = chr(ord('A') + max_col - 1)
    while True:
        s = input().strip().upper()
        if len(s) == 1 and 'A' <= s <= last:
            return ord(s) - ord('A')
        print("Invalid input, try again:")

def main():
    if COLS > 26 or NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Invalid settings.")
        return
    b = make_board(ROWS, COLS)
    players = TOKENS[:NUM_PLAYERS]
    cur = random.randrange(NUM_PLAYERS)

    while True:
        os.system('clear')
        print_board(b)
        print(f"Player {players[cur]}, please enter a column:")
        col = get_col_input(COLS)
        row = drop(b, col, players[cur])
        if row == -1:
            os.system('clear')
            print_board(b)
            print(f"Column {chr(ord('A')+col)} is full. Turn lost.")
        else:
            if check_four(b, players[cur]):
                os.system('clear')
                print_board(b)
                print(f"Player {players[cur]} won!")
                break
            if full(b):
                os.system('clear')
                print_board(b)
                print("Game is a draw.")
                break
        cur = (cur + 1) % NUM_PLAYERS

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
