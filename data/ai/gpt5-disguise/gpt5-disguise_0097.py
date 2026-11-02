import os
import random
import sys

ROWS = 6
COLS = 7
PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]
WINN = 4

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear():
    os.system('clear')

def print_board(b):
    clear()
    letters = [chr(ord('A') + i) for i in range(len(b[0]))]
    print("  " + "   ".join(letters))
    print("+" + "---+" * len(b[0]))
    for r in range(len(b)):
        row = []
        for c in range(len(b[0])):
            row.append(b[r][c])
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(b[0]))

def in_bounds_col(ch):
    if len(ch) != 1:
        return False
    if not ('A' <= ch <= chr(ord('A') + COLS - 1)):
        return False
    return True

def drop(b, col, t):
    for r in range(ROWS - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = t
            return r, col
    return None

def check_dir(b, r, c, dr, dc, t):
    cnt = 0
    i, j = r, c
    while 0 <= i < ROWS and 0 <= j < COLS and b[i][j] == t:
        cnt += 1
        i += dr
        j += dc
    return cnt

def won(b, r, c, t):
    # horizontal
    h = check_dir(b, r, c, 0, -1, t) + check_dir(b, r, c + 1, 0, 1, t)
    if h >= WINN: return True
    # vertical
    v = check_dir(b, r, c, -1, 0, t) + check_dir(b, r + 1, c, 1, 0, t)
    if v >= WINN: return True
    # diag /
    d1 = check_dir(b, r, c, -1, 1, t) + check_dir(b, r + 1, c - 1, 1, -1, t)
    if d1 >= WINN: return True
    # diag \
    d2 = check_dir(b, r, c, -1, -1, t) + check_dir(b, r + 1, c + 1, 1, 1, t)
    if d2 >= WINN: return True
    return False

def full(b):
    for c in range(COLS):
        if b[0][c] == " ":
            return False
    return True

def main():
    if COLS > 26:
        print("Max 26 columns.")
        return
    if not (2 <= PLAYERS <= 5):
        print("Players must be between 2 and 5.")
        return

    syms = TOKENS[:PLAYERS]
    b = make_board(ROWS, COLS)
    cur = random.randint(0, PLAYERS - 1)
    print_board(b)

    while True:
        t = syms[cur]
        print(f"Player {t}, please enter a column:")
        col_input = input().strip().upper()
        while not in_bounds_col(col_input):
            print_board(b)
            print(f"Player {t}, please enter a column:")
            col_input = input().strip().upper()
        col = ord(col_input) - ord('A')

        pos = drop(b, col, t)
        print_board(b)
        if pos is None:
            print("Column is full. Turn lost.")
            if full(b):
                print("It's a draw.")
                break
            cur = (cur + 1) % PLAYERS
            continue

        r, c = pos
        if won(b, r, c, t):
            print(f"Player {t} won!")
            break
        if full(b):
            print("It's a draw.")
            break
        cur = (cur + 1) % PLAYERS

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
