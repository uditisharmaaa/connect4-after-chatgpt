import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2

SYMS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(b):
    os.system('clear')
    labels = [string.ascii_uppercase[i] for i in range(len(b[0]))]
    print("  " + "   ".join(labels))
    sep = "+" + ("---+" * len(b[0]))
    for r in range(len(b)):
        print(sep)
        row = "|"
        for c in range(len(b[0])):
            row += " " + b[r][c] + " |"
        print(row)
    print(sep)

def col_index(ch):
    if len(ch) != 1:
        return -1
    ch = ch.upper()
    if ch < 'A' or ch >= chr(ord('A') + COLS):
        return -1
    return ord(ch) - ord('A')

def drop(b, col, sym):
    for r in range(ROWS - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = sym
            return r
    return -1

def win_from(b, r, c, sym, dr, dc):
    for k in range(4):
        rr = r + dr * k
        cc = c + dc * k
        if rr < 0 or rr >= ROWS or cc < 0 or cc >= COLS:
            return False
        if b[rr][cc] != sym:
            return False
    return True

def check_win(b, sym):
    for r in range(ROWS):
        for c in range(COLS):
            if b[r][c] != sym:
                continue
            if win_from(b, r, c, sym, 0, 1):
                return True
            if win_from(b, r, c, sym, 1, 0):
                return True
            if win_from(b, r, c, sym, 1, 1):
                return True
            if win_from(b, r, c, sym, -1, 1):
                return True
    return False

def is_draw(b):
    for r in b:
        for x in r:
            if x == " ":
                return False
    return True

def main():
    board = make_board(ROWS, COLS)
    cur = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    while True:
        sym = SYMS[cur]
        print(f"Player {sym}, please enter a column:")
        col = -1
        while True:
            s = input().strip()
            col = col_index(s)
            if col != -1:
                break
            print("Invalid input. Please enter a valid column letter:")
        row = drop(board, col, sym)
        if row == -1:
            print_board(board)
            print("Column is full. Turn lost.")
            cur = (cur + 1) % NUM_PLAYERS
            continue
        print_board(board)
        if check_win(board, sym):
            print(f"Player {sym} won!")
            break
        if is_draw(board):
            print("It's a draw!")
            break
        cur = (cur + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
