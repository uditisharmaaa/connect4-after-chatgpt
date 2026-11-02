import os
import random
import string

ROWS = 6
COLS = 7
PLAYERS = 2

symbols = ["X", "O", "V", "H", "M"][:PLAYERS]
letters = list(string.ascii_uppercase[:COLS])

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear():
    os.system('clear')

def print_board(b):
    hdr = "  " + "   ".join(letters)
    line = "+" + "+".join(["---"] * COLS) + "+"
    print(hdr)
    print(line)
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(b[r][c])
        print("| " + " | ".join(row) + " |")
        print(line)

def get_col_input(p):
    while True:
        s = input(f"Player {p}, please enter a column: ").strip().upper()
        if len(s) != 1:
            continue
        if s not in letters:
            continue
        return letters.index(s)

def drop(b, col, sym):
    for r in range(ROWS - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = sym
            return r, col
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(b, sym):
    for r in range(ROWS):
        for c in range(COLS):
            if b[r][c] != sym:
                continue
            dirs = [(0,1),(1,0),(1,1),(1,-1)]
            for dr, dc in dirs:
                ok = True
                for k in range(1,4):
                    nr = r + dr*k
                    nc = c + dc*k
                    if not in_bounds(nr,nc) or b[nr][nc] != sym:
                        ok = False
                        break
                if ok:
                    return True
    return False

def is_draw(b):
    for r in range(ROWS):
        for c in range(COLS):
            if b[r][c] == " ":
                return False
    return True

def main():
    b = make_board(ROWS, COLS)
    turn = random.randrange(len(symbols))
    while True:
        clear()
        print_board(b)
        p = symbols[turn]
        col = get_col_input(p)
        placed = drop(b, col, p)
        if placed is None:
            turn = (turn + 1) % len(symbols)
            continue
        if check_win(b, p):
            clear()
            print_board(b)
            print(f"Player {p} won!")
            break
        if is_draw(b):
            clear()
            print_board(b)
            print("It's a draw!")
            break
        turn = (turn + 1) % len(symbols)

if __name__ == "__main__":
    main()
