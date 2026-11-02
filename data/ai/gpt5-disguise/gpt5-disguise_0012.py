import os
import random
import sys

ROWS = 6
COLS = 7
NUM_PLAYERS = 2

tokens = ["X", "O", "V", "H", "M"]


def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]


def clear():
    os.system('clear')


def print_board(b):
    letters = [chr(ord('A') + i) for i in range(len(b[0]))]
    print("  " + "   ".join(letters))
    print("+" + "---+" * len(b[0]))
    for r in range(len(b)):
        row = "|"
        for c in range(len(b[0])):
            row += " " + b[r][c] + " |"
        print(row)
        print("+" + "---+" * len(b[0]))


def get_col_input(max_c):
    while True:
        s = input().strip()
        if len(s) == 0:
            print("Invalid input, try again:")
            continue
        ch = s[0].upper()
        if not ch.isalpha():
            print("Invalid input, try again:")
            continue
        idx = ord(ch) - ord('A')
        if idx < 0 or idx >= max_c:
            print("Invalid input, try again:")
            continue
        return idx


def drop(b, col, t):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = t
            return r, col
    return None


def in_bounds(r, c, R, C):
    return 0 <= r < R and 0 <= c < C


def check_win_from(b, r, c):
    if b[r][c] == " ":
        return False
    t = b[r][c]
    dirs = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    R = len(b)
    C = len(b[0])
    for dr, dc in dirs:
        cnt = 1
        rr, cc = r + dr, c + dc
        while in_bounds(rr, cc, R, C) and b[rr][cc] == t:
            cnt += 1
            rr += dr
            cc += dc
        rr, cc = r - dr, c - dc
        while in_bounds(rr, cc, R, C) and b[rr][cc] == t:
            cnt += 1
            rr -= dr
            cc -= dc
        if cnt >= 4:
            return True
    return False


def check_win(b):
    for r in range(len(b)):
        for c in range(len(b[0])):
            if check_win_from(b, r, c):
                return True
    return False


def full_col(b, c):
    return b[0][c] != " "


def board_full(b):
    for c in range(len(b[0])):
        if b[0][c] == " ":
            return False
    return True


def main():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Invalid number of players")
        return
    if COLS > 26:
        print("Too many columns")
        return

    ps = tokens[:NUM_PLAYERS]
    b = make_board(ROWS, COLS)
    turn = random.randint(0, len(ps) - 1)

    while True:
        clear()
        print_board(b)
        print("Player " + ps[turn] + ", please enter a column:")
        col = get_col_input(COLS)

        if full_col(b, col):
            # lose turn
            turn = (turn + 1) % len(ps)
            continue

        pos = drop(b, col, ps[turn])

        if check_win(b):
            clear()
            print_board(b)
            print("Player " + ps[turn] + " won!")
            break

        if board_full(b):
            clear()
            print_board(b)
            print("It's a draw!")
            break

        turn = (turn + 1) % len(ps)


if __name__ == "__main__":
    main()
