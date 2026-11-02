import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]
WIN_LEN = 4

def make_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear():
    os.system('clear')

def print_board(b):
    letters = [chr(ord('A') + i) for i in range(len(b[0]))]
    header = "  " + "   ".join(letters)
    line = "+" + "+".join(["---"] * len(b[0])) + "+"
    print(header)
    for r in range(len(b)):
        print(line)
        row_str = "|"
        for c in range(len(b[0])):
            row_str += " " + b[r][c] + " |"
        print(row_str)
    print(line)

def valid_col(ch, cols):
    if len(ch) != 1:
        return False
    if not ch.isalpha():
        return False
    ch = ch.upper()
    idx = ord(ch) - ord('A')
    return 0 <= idx < cols

def drop(b, col, t):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = t
            return r
    return None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_line(b, r, c, dr, dc, t):
    cnt = 0
    rr, cc = r, c
    while in_bounds(rr, cc, len(b), len(b[0])) and b[rr][cc] == t:
        cnt += 1
        rr += dr
        cc += dc
    return cnt

def check_win(b, t):
    rows = len(b)
    cols = len(b[0])
    for r in range(rows):
        for c in range(cols):
            if b[r][c] != t:
                continue
            # right
            if c + WIN_LEN - 1 < cols:
                ok = True
                for i in range(WIN_LEN):
                    if b[r][c + i] != t:
                        ok = False
                        break
                if ok:
                    return True
            # down
            if r + WIN_LEN - 1 < rows:
                ok = True
                for i in range(WIN_LEN):
                    if b[r + i][c] != t:
                        ok = False
                        break
                if ok:
                    return True
            # diag down-right
            if r + WIN_LEN - 1 < rows and c + WIN_LEN - 1 < cols:
                ok = True
                for i in range(WIN_LEN):
                    if b[r + i][c + i] != t:
                        ok = False
                        break
                if ok:
                    return True
            # diag down-left
            if r + WIN_LEN - 1 < rows and c - (WIN_LEN - 1) >= 0:
                ok = True
                for i in range(WIN_LEN):
                    if b[r + i][c - i] != t:
                        ok = False
                        break
                if ok:
                    return True
    return False

def board_full(b):
    for r in b:
        for v in r:
            if v == " ":
                return False
    return True

def main():
    cols = COLS
    rows = ROWS
    n = NUM_PLAYERS
    if n < 2:
        n = 2
    if n > 5:
        n = 5
    tokens = TOKENS[:n]
    b = make_board(rows, cols)
    turn = random.randrange(n)

    clear()
    print_board(b)

    while True:
        t = tokens[turn]
        inp = input(f"Player {t}, please enter a column: ").strip().upper()
        while not valid_col(inp, cols):
            inp = input(f"Player {t}, please enter a column: ").strip().upper()
        c = ord(inp) - ord('A')

        r = drop(b, c, t)
        clear()
        print_board(b)

        if r is None:
            print(f"Column {inp} is full. Turn lost.")
            turn = (turn + 1) % n
            continue

        if check_win(b, t):
            print(f"Player {t} won!")
            break

        if board_full(b):
            print("It's a draw!")
            break

        turn = (turn + 1) % n

if __name__ == "__main__":
    main()
