import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
SYMS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_LEN = 4

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear_screen():
    os.system('clear')

def print_board(b):
    hdr = "  " + "   ".join(chr(65+i) for i in range(len(b[0])))
    print(hdr)
    sep = "+" + "+".join(["---"] * len(b[0])) + "+"
    for r in range(len(b)):
        print(sep)
        row = "|"
        for c in range(len(b[0])):
            row += " " + b[r][c] + " |"
        print(row)
    print(sep)

def drop(b, col, s):
    for r in range(len(b)-1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = s
            return r
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(b, s):
    for r in range(ROWS):
        for c in range(COLS):
            if b[r][c] != s:
                continue
            # right
            ok = True
            for k in range(WIN_LEN):
                if not in_bounds(r, c+k) or b[r][c+k] != s:
                    ok = False
                    break
            if ok: return True
            # down
            ok = True
            for k in range(WIN_LEN):
                if not in_bounds(r+k, c) or b[r+k][c] != s:
                    ok = False
                    break
            if ok: return True
            # down-right
            ok = True
            for k in range(WIN_LEN):
                if not in_bounds(r+k, c+k) or b[r+k][c+k] != s:
                    ok = False
                    break
            if ok: return True
            # down-left
            ok = True
            for k in range(WIN_LEN):
                if not in_bounds(r+k, c-k) or b[r+k][c-k] != s:
                    ok = False
                    break
            if ok: return True
    return False

def is_draw(b):
    for r in b:
        for v in r:
            if v == " ":
                return False
    return True

def get_col_input(max_cols):
    while True:
        s = input().strip()
        if len(s) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        if not s.isalpha() or not s.isupper():
            print("Invalid input. Please enter an uppercase letter.")
            continue
        col = ord(s) - ord('A')
        if 0 <= col < max_cols:
            return col
        else:
            print("Invalid column. Please choose between A and " + chr(ord('A')+max_cols-1) + ".")

def main():
    if COLS > 26:
        print("Max 26 columns supported.")
        return
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Players must be between 2 and 5.")
        return
    b = make_board(ROWS, COLS)
    turn = random.randrange(NUM_PLAYERS)
    clear_screen()
    print_board(b)
    while True:
        sym = SYMS[turn]
        print("Player " + sym + ", please enter a column:")
        col = get_col_input(COLS)
        r = drop(b, col, sym)
        if r is None:
            # lose turn
            clear_screen()
            print_board(b)
            if is_draw(b):
                print("It's a draw!")
                break
            turn = (turn + 1) % NUM_PLAYERS
            continue
        clear_screen()
        print_board(b)
        if check_win(b, sym):
            print("Player " + sym + " won!")
            break
        if is_draw(b):
            print("It's a draw!")
            break
        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
