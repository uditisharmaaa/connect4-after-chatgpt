import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LEN = 4

SYMS = ["X", "O", "V", "H", "M"]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear():
    os.system('clear')

def print_board(b):
    clear()
    letters = list(string.ascii_uppercase[:len(b[0])])
    print("  " + "   ".join(letters))
    print("+---" * len(b[0]) + "+")
    for r in range(len(b)):
        row = []
        for c in range(len(b[0])):
            row.append(b[r][c])
        print("| " + " | ".join(row) + " |")
        print("+---" * len(b[0]) + "+")

def drop(b, col, sym):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = sym
            return r, col
    return None

def in_bounds(r, c, b):
    return 0 <= r < len(b) and 0 <= c < len(b[0])

def check_win_from(b, r, c, sym, dr, dc):
    count = 0
    rr, cc = r, c
    while in_bounds(rr, cc, b) and b[rr][cc] == sym:
        count += 1
        if count == WIN_LEN:
            return True
        rr += dr
        cc += dc
    return False

def check_win(b, sym):
    for r in range(len(b)):
        for c in range(len(b[0])):
            if b[r][c] != sym:
                continue
            if check_win_from(b, r, c, sym, 0, 1):
                return True
            if check_win_from(b, r, c, sym, 1, 0):
                return True
            if check_win_from(b, r, c, sym, 1, 1):
                return True
            if check_win_from(b, r, c, sym, 1, -1):
                return True
    return False

def board_full(b):
    for r in b:
        for v in r:
            if v == " ":
                return False
    return True

def valid_col_input(s, max_c):
    if len(s) != 1:
        return False
    if s < 'A' or s > chr(ord('A') + max_c - 1):
        return False
    return True

def main():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Invalid number of players.")
        return
    if COLS < 1 or COLS > 26 or ROWS < 1:
        print("Invalid board size.")
        return

    b = make_board(ROWS, COLS)
    players = SYMS[:NUM_PLAYERS]
    turn = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board(b)
        p = players[turn]
        print(f"Player {p}, please enter a column:")
        col_input = input().strip().upper()
        while not valid_col_input(col_input, COLS):
            print("Invalid input. Please enter a valid column letter:")
            col_input = input().strip().upper()
        col_idx = ord(col_input) - ord('A')
        placed = drop(b, col_idx, p)
        if placed is None:
            print("Column is full. Turn lost.")
        else:
            if check_win(b, p):
                print_board(b)
                print(f"Player {p} won!")
                break
            if board_full(b):
                print_board(b)
                print("It's a draw!")
                break
        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
