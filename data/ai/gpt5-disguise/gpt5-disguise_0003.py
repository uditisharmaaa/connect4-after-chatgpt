import os
import random
import sys

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_N = 4
TOKENS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def clear():
    os.system('clear')

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(b):
    clear()
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    print("+---" * COLS + "+")
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(b[r][c])
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def col_full(b, c):
    return b[0][c] != " "

def drop(b, c, t):
    for r in range(ROWS - 1, -1, -1):
        if b[r][c] == " ":
            b[r][c] = t
            return r, c
    return None

def inside(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_dir(b, r, c, dr, dc, t):
    cnt = 0
    for k in range(WIN_N):
        rr = r + dr * k
        cc = c + dc * k
        if not inside(rr, cc) or b[rr][cc] != t:
            return False
    return True

def won(b, t):
    for r in range(ROWS):
        for c in range(COLS):
            if b[r][c] != t:
                continue
            if check_dir(b, r, c, 0, 1, t):
                return True
            if check_dir(b, r, c, 1, 0, t):
                return True
            if check_dir(b, r, c, 1, 1, t):
                return True
            if check_dir(b, r, c, 1, -1, t):
                return True
    return False

def board_full(b):
    for c in range(COLS):
        if b[0][c] == " ":
            return False
    return True

def get_move():
    while True:
        s = input().strip().upper()
        if len(s) != 1:
            print("Invalid input, try again:")
            continue
        if not ('A' <= s <= chr(ord('A') + COLS - 1)):
            print("Invalid input, try again:")
            continue
        return ord(s) - ord('A')

def main():
    if COLS > 26 or NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Config error")
        sys.exit(1)

    board = make_board(ROWS, COLS)
    turn = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board(board)
        print(f"Player {TOKENS[turn]}, please enter a column:")
        c = get_move()
        if col_full(board, c):
            print_board(board)
            print(f"Column {chr(ord('A')+c)} is full. Turn lost.")
        else:
            drop(board, c, TOKENS[turn])
            if won(board, TOKENS[turn]):
                print_board(board)
                print(f"Player {TOKENS[turn]} won!")
                break
            if board_full(board):
                print_board(board)
                print("It's a draw!")
                break
        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
