import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
SYMS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear():
    os.system('clear')

def print_board(b):
    clear()
    letters = [chr(ord('A') + i) for i in range(len(b[0]))]
    print("  " + "   ".join(letters))
    print("+" + "---+" * len(b[0]))
    for i in range(len(b)):
        row = "|"
        for j in range(len(b[0])):
            row += " " + b[i][j] + " |"
        print(row)
        print("+" + "---+" * len(b[0]))

def place(b, col, sym):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = sym
            return True
    return False

def in_bounds(r, c, R, C):
    return 0 <= r < R and 0 <= c < C

def check_win(b):
    R = len(b)
    C = len(b[0])
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(R):
        for c in range(C):
            if b[r][c] == " ":
                continue
            ch = b[r][c]
            for dr, dc in dirs:
                cnt = 0
                rr = r
                cc = c
                while in_bounds(rr, cc, R, C) and b[rr][cc] == ch:
                    cnt += 1
                    if cnt == 4:
                        return ch
                    rr += dr
                    cc += dc
    return None

def full(b):
    for row in b:
        for x in row:
            if x == " ":
                return False
    return True

def get_col_input(C):
    while True:
        s = input().strip().upper()
        if len(s) != 1:
            print("Invalid input. Enter a single letter.")
            continue
        if not ('A' <= s <= 'Z'):
            print("Invalid input. Enter a letter.")
            continue
        idx = ord(s) - ord('A')
        if 0 <= idx < C:
            return idx
        else:
            print("Column out of range.")

def main():
    b = make_board(ROWS, COLS)
    cur = random.randint(0, NUM_PLAYERS - 1)
    print_board(b)
    while True:
        print(f"Player {SYMS[cur]}, please enter a column:")
        col = get_col_input(COLS)
        ok = place(b, col, SYMS[cur])
        print_board(b)
        if not ok:
            cur = (cur + 1) % NUM_PLAYERS
            if full(b):
                print("It's a draw!")
                break
            continue
        w = check_win(b)
        if w:
            print(f"Player {w} won!")
            break
        if full(b):
            print("It's a draw!")
            break
        cur = (cur + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
