import os
import random
import sys

ROWS = 6
COLS = 7
PLAYERS = 2
SYMS = ["X", "O", "V", "H", "M"]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear():
    os.system('clear')

def print_board(b):
    letters = [chr(ord('A') + i) for i in range(len(b[0]))]
    print("  " + "   ".join(letters))
    print("+" + ("---+" * len(b[0])))
    for r in range(len(b)):
        row = "|"
        for c in range(len(b[0])):
            row += " " + b[r][c] + " |"
        print(row)
        print("+" + ("---+" * len(b[0])))

def drop(b, col, sym):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = sym
            return r, col
    return None

def in_bounds(r, c, R, C):
    return 0 <= r < R and 0 <= c < C

def check_dir(b, r, c, dr, dc, sym):
    count = 0
    R = len(b)
    C = len(b[0])
    for k in range(4):
        rr = r + dr * k
        cc = c + dc * k
        if not in_bounds(rr, cc, R, C):
            return False
        if b[rr][cc] != sym:
            return False
    return True

def check_win(b, sym):
    R = len(b)
    C = len(b[0])
    for r in range(R):
        for c in range(C):
            if b[r][c] != sym:
                continue
            if check_dir(b, r, c, 0, 1, sym):
                return True
            if check_dir(b, r, c, 1, 0, sym):
                return True
            if check_dir(b, r, c, 1, 1, sym):
                return True
            if check_dir(b, r, c, 1, -1, sym):
                return True
    return False

def draw(b):
    for r in b:
        for v in r:
            if v == " ":
                return False
    return True

def get_col_input(valid_letters):
    while True:
        try:
            s = input().strip()
        except EOFError:
            sys.exit(0)
        if len(s) != 1:
            print("Invalid input, try again:")
            continue
        ch = s.upper()
        if ch not in valid_letters:
            print("Invalid input, try again:")
            continue
        return valid_letters.index(ch)

def main():
    if COLS > 26:
        print("Max 26 columns.")
        return
    p_syms = SYMS[:PLAYERS]
    b = make_board(ROWS, COLS)
    letters = [chr(ord('A') + i) for i in range(COLS)]
    turn = random.randint(0, PLAYERS - 1)

    clear()
    print_board(b)
    while True:
        sym = p_syms[turn]
        print(f"Player {sym}, please enter a column:")
        col = get_col_input(letters)
        pos = drop(b, col, sym)
        if pos is None:
            clear()
            print_board(b)
            print("Column is full, you lose your turn.")
            turn = (turn + 1) % PLAYERS
            continue
        clear()
        print_board(b)
        if check_win(b, sym):
            print(f"Player {sym} won!")
            break
        if draw(b):
            print("It's a draw!")
            break
        turn = (turn + 1) % PLAYERS

if __name__ == "__main__":
    main()
