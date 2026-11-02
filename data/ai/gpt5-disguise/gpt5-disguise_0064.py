import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(b):
    letters = [chr(ord('A') + i) for i in range(len(b[0]))]
    print("  " + "   ".join(letters))
    sep = "+" + "+".join(["---"] * len(b[0])) + "+"
    for r in range(len(b)):
        print(sep)
        row_str = "|"
        for c in range(len(b[0])):
            row_str += " " + b[r][c] + " |"
        print(row_str)
    print(sep)

def clear():
    os.system('clear')

def get_input(max_col):
    while True:
        s = input()
        if len(s) != 1:
            print("Invalid input. Please enter a single uppercase letter:")
            continue
        ch = s.upper()
        if not ('A' <= ch <= 'Z'):
            print("Invalid input. Please enter an uppercase letter:")
            continue
        idx = ord(ch) - ord('A')
        if idx < 0 or idx >= max_col:
            print("Out of range. Please enter a valid column:")
            continue
        return idx, ch

def drop(b, col, tok):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = tok
            return r
    return None

def in_bounds(r, c, R, C):
    return 0 <= r < R and 0 <= c < C

def check_win(b, tok):
    R = len(b)
    C = len(b[0])
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(R):
        for c in range(C):
            if b[r][c] != tok:
                continue
            for dr, dc in dirs:
                cnt = 1
                rr, cc = r + dr, c + dc
                while in_bounds(rr, cc, R, C) and b[rr][cc] == tok and cnt < WIN_COUNT:
                    cnt += 1
                    rr += dr
                    cc += dc
                if cnt >= WIN_COUNT:
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
        print("Max 26 columns supported.")
        return
    b = make_board(ROWS, COLS)
    players = TOKENS[:NUM_PLAYERS]
    turn = random.randrange(NUM_PLAYERS)

    while True:
        clear()
        print_board(b)
        p = players[turn]
        print(f"Player {p}, please enter a column:")
        col_idx, col_char = get_input(COLS)
        row_placed = drop(b, col_idx, p)
        if row_placed is None:
            clear()
            print_board(b)
            print(f"Column {col_char} is full. Turn lost.")
            turn = (turn + 1) % NUM_PLAYERS
            continue
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
        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
