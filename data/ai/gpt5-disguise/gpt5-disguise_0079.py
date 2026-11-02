import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LEN = 4

SYMS = ["X", "O", "V", "H", "M"]
LETTERS = [chr(ord('A') + i) for i in range(26)]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear():
    os.system('clear')

def print_board(b):
    cols = len(b[0])
    header = "  " + "   ".join(LETTERS[:cols])
    sep = "+" + "---+" * cols
    print(header)
    print(sep)
    for r in range(len(b)):
        row = []
        for c in range(cols):
            row.append(b[r][c])
        print("| " + " | ".join(row) + " |")
        print(sep)

def find_row(b, col):
    for r in range(len(b)-1, -1, -1):
        if b[r][col] == " ":
            return r
    return None

def in_bounds(r, c, R, C):
    return 0 <= r < R and 0 <= c < C

def check_win(b, sym):
    R = len(b)
    C = len(b[0])
    dirs = [(1,0),(0,1),(1,1),(1,-1)]
    for r in range(R):
        for c in range(C):
            if b[r][c] != sym:
                continue
            for dr, dc in dirs:
                cnt = 0
                rr, cc = r, c
                while in_bounds(rr, cc, R, C) and b[rr][cc] == sym and cnt < WIN_LEN:
                    cnt += 1
                    rr += dr
                    cc += dc
                if cnt >= WIN_LEN:
                    return True
    return False

def board_full(b):
    for r in b:
        for x in r:
            if x == " ":
                return False
    return True

def main():
    players = SYMS[:max(2, min(5, NUM_PLAYERS))]
    rows = ROWS
    cols = min(COLS, 26)
    b = make_board(rows, cols)
    cur = random.randrange(len(players))

    while True:
        clear()
        print_board(b)
        p = players[cur]
        print(f"Player {p}, please enter a column:")
        # get valid input letter
        col = None
        while True:
            s = input().strip()
            if len(s) != 1:
                print("Invalid input. Enter a single letter.")
                continue
            ch = s.upper()
            if ch not in LETTERS[:cols]:
                print("Invalid column. Try again.")
                continue
            col = LETTERS.index(ch)
            break

        r = find_row(b, col)
        if r is None:
            # turn lost
            cur = (cur + 1) % len(players)
            continue
        b[r][col] = p

        if check_win(b, p):
            clear()
            print_board(b)
            print(f"Player {p} won!")
            break

        if board_full(b):
            clear()
            print_board(b)
            print("It's a draw!")
            break

        cur = (cur + 1) % len(players)

if __name__ == "__main__":
    main()
