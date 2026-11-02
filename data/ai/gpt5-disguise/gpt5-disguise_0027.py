import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
SYMBOLS = ["X", "O", "V", "H", "M"]
WIN_LEN = 4

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(b):
    os.system('clear')
    letters = string.ascii_uppercase[:len(b[0])]
    print("  " + "   ".join(list(letters)))
    print("+" + "---+" * len(b[0]))
    for r in range(len(b)):
        row = "|" + "|".join(f" {b[r][c]} " for c in range(len(b[0]))) + "|"
        print(row)
        print("+" + "---+" * len(b[0]))

def drop(b, col, sym):
    for r in range(len(b)-1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = sym
            return r, col
    return None

def in_bounds(r, c, b):
    return 0 <= r < len(b) and 0 <= c < len(b[0])

def check_win(b, sym):
    R = len(b)
    C = len(b[0])
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(R):
        for c in range(C):
            if b[r][c] != sym:
                continue
            for dr, dc in dirs:
                cnt = 0
                rr, cc = r, c
                while in_bounds(rr, cc, b) and b[rr][cc] == sym and cnt < WIN_LEN:
                    cnt += 1
                    rr += dr
                    cc += dc
                if cnt >= WIN_LEN:
                    return True
    return False

def board_full(b):
    for c in range(len(b[0])):
        if b[0][c] == " ":
            return False
    return True

def valid_col_input(s, maxc):
    if len(s) != 1:
        return False
    if s < 'A' or s > chr(ord('A') + maxc - 1):
        return False
    return True

def main():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        return
    b = make_board(ROWS, COLS)
    players = SYMBOLS[:NUM_PLAYERS]
    turn = random.randrange(NUM_PLAYERS)
    print_board(b)

    while True:
        sym = players[turn]
        print(f"Player {sym}, please enter a column:")
        s = input().strip().upper()
        while not valid_col_input(s, COLS):
            print("Invalid input. Please enter a valid column letter:")
            s = input().strip().upper()
        col = ord(s) - ord('A')
        placed = drop(b, col, sym)
        if placed is None:
            # column full, lose turn
            turn = (turn + 1) % NUM_PLAYERS
            print_board(b)
            continue
        r, c = placed
        if check_win(b, sym):
            print_board(b)
            print(f"Player {sym} won!")
            break
        if board_full(b):
            print_board(b)
            print("It's a draw!")
            break
        turn = (turn + 1) % NUM_PLAYERS
        print_board(b)

if __name__ == "__main__":
    main()
