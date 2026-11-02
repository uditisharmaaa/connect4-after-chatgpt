import random
import os
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(b):
    os.system('clear')
    letters = string.ascii_uppercase[:len(b[0])]
    s = "  " + "   ".join(letters)
    print(s)
    sep = "+" + "+".join(["---"] * len(b[0])) + "+"
    for r in range(len(b)):
        print(sep)
        row = "|"
        for c in range(len(b[0])):
            row += " " + b[r][c] + " |"
        print(row)
    print(sep)

def get_players(n):
    return TOKENS[:n]

def valid_col_input(x, maxc):
    if len(x) != 1:
        return False
    if x < "A" or x > chr(ord("A") + maxc - 1):
        return False
    return True

def place(b, col, t):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = t
            return r, col
    return None

def check_line(b, r, c, dr, dc, t):
    cnt = 0
    rr = r
    cc = c
    while 0 <= rr < len(b) and 0 <= cc < len(b[0]) and b[rr][cc] == t:
        cnt += 1
        rr += dr
        cc += dc
    rr = r - dr
    cc = c - dc
    while 0 <= rr < len(b) and 0 <= cc < len(b[0]) and b[rr][cc] == t:
        cnt += 1
        rr -= dr
        cc -= dc
    return cnt >= 4

def has_won(b, r, c, t):
    return (check_line(b, r, c, 0, 1, t) or
            check_line(b, r, c, 1, 0, t) or
            check_line(b, r, c, 1, 1, t) or
            check_line(b, r, c, 1, -1, t))

def board_full(b):
    for c in range(len(b[0])):
        if b[0][c] == " ":
            return False
    return True

def main():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        return
    if COLS > 26:
        return
    b = make_board(ROWS, COLS)
    players = get_players(NUM_PLAYERS)
    turn = random.randint(0, NUM_PLAYERS - 1)
    print_board(b)
    while True:
        p = players[turn]
        print(f"Player {p}, please enter a column:")
        x = input().strip().upper()
        while not valid_col_input(x, COLS):
            print("Invalid input. Try again:")
            x = input().strip().upper()
        col = ord(x) - ord("A")
        res = place(b, col, p)
        if res is None:
            print_board(b)
            print(f"Column {x} is full. Turn lost.")
            turn = (turn + 1) % NUM_PLAYERS
            continue
        r, c = res
        print_board(b)
        if has_won(b, r, c, p):
            print(f"Player {p} won!")
            break
        if board_full(b):
            print("It's a draw!")
            break
        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
