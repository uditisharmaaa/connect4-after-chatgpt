import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LEN = 4

SYMS_ALL = ["X", "O", "V", "H", "M"]
SYMS = SYMS_ALL[:NUM_PLAYERS]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear():
    os.system('clear')

def print_board(b):
    clear()
    labels = "  " + "   ".join(string.ascii_uppercase[:len(b[0])])
    print(labels)
    sep = "+" + "+".join(["---"] * len(b[0])) + "+"
    for r in range(len(b)):
        print(sep)
        row = "|"
        for c in range(len(b[0])):
            row += " " + b[r][c] + " |"
        print(row)
    print(sep)

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def place(b, col, sym):
    for r in range(ROWS - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = sym
            return r, col
    return None

def get_move(col_count):
    while True:
        s = input().strip()
        if len(s) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        ch = s.upper()
        if ch < "A" or ch >= chr(ord("A") + col_count):
            print("Invalid column. Please enter a valid letter.")
            continue
        return ord(ch) - ord("A")

def count_dir(b, r, c, dr, dc, sym):
    cnt = 0
    rr, cc = r, c
    while in_bounds(rr, cc) and b[rr][cc] == sym:
        cnt += 1
        rr += dr
        cc += dc
    return cnt

def check_win_from(b, r, c, sym):
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in dirs:
        total = count_dir(b, r, c, dr, dc, sym) + count_dir(b, r, c, -dr, -dc, sym) - 1
        if total >= WIN_LEN:
            return True
    return False

def board_full(b):
    for r in b:
        for v in r:
            if v == " ":
                return False
    return True

def main():
    if COLS > 26:
        print("Maximum columns is 26.")
        return
    b = make_board(ROWS, COLS)
    cur = random.randint(0, NUM_PLAYERS - 1)
    print_board(b)
    while True:
        sym = SYMS[cur]
        print(f"Player {sym}, please enter a column:")
        col = get_move(COLS)
        res = place(b, col, sym)
        print_board(b)
        if res is None:
            print("Column is full. Turn lost.")
        else:
            r, c = res
            if check_win_from(b, r, c, sym):
                print(f"Player {sym} won!")
                break
        if board_full(b):
            print("It's a draw!")
            break
        cur = (cur + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
