import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
SYMS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def clear():
    os.system('clear')

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(b):
    clear()
    letters = [string.ascii_uppercase[i] for i in range(len(b[0]))]
    print("  " + "   ".join(letters))
    print("+---" * len(b[0]) + "+")
    for r in range(len(b)):
        row = []
        for c in range(len(b[0])):
            row.append(b[r][c])
        print("| " + " | ".join(row) + " |")
        print("+---" * len(b[0]) + "+")

def in_bounds_col(ch):
    if len(ch) != 1:
        return False
    if ch < 'A' or ch >= chr(ord('A') + COLS):
        return False
    return True

def ask_col(sym):
    while True:
        s = input(f"Player {sym}, please enter a column: ").strip().upper()
        if in_bounds_col(s):
            return ord(s) - ord('A')

def drop(b, col, sym):
    for r in range(ROWS - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = sym
            return r, col
    return None

def count_dir(b, r, c, dr, dc, sym):
    cnt = 0
    rr, cc = r, c
    while 0 <= rr < ROWS and 0 <= cc < COLS and b[rr][cc] == sym:
        cnt += 1
        rr += dr
        cc += dc
    return cnt

def won(b, r, c, sym):
    # horizontal
    a = count_dir(b, r, c, 0, -1, sym) + count_dir(b, r, c + 1, 0, 1, sym)
    if a >= 4:
        return True
    # vertical
    a = count_dir(b, r, c, -1, 0, sym) + count_dir(b, r + 1, c, 1, 0, sym)
    if a >= 4:
        return True
    # diag down-right
    a = count_dir(b, r, c, -1, -1, sym) + count_dir(b, r + 1, c + 1, 1, 1, sym)
    if a >= 4:
        return True
    # diag up-right
    a = count_dir(b, r, c, 1, -1, sym) + count_dir(b, r - 1, c + 1, -1, 1, sym)
    if a >= 4:
        return True
    return False

def full(b):
    for c in range(COLS):
        if b[0][c] == " ":
            return False
    return True

def main():
    b = make_board(ROWS, COLS)
    start = random.randint(0, NUM_PLAYERS - 1)
    turn = start
    print_board(b)
    while True:
        sym = SYMS[turn]
        col = ask_col(sym)
        pos = drop(b, col, sym)
        print_board(b)
        if pos is None:
            print("Column full. Turn lost.")
        else:
            r, c = pos
            if won(b, r, c, sym):
                print(f"Player {sym} won!")
                break
        if full(b):
            print("It's a draw!")
            break
        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
