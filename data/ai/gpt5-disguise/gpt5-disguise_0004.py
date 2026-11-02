import os
import random
import sys

ROWS = 6
COLS = 7
NUM_PLAYERS = 2

if COLS > 26:
    COLS = 26
if NUM_PLAYERS < 2:
    NUM_PLAYERS = 2
if NUM_PLAYERS > 5:
    NUM_PLAYERS = 5

pieces = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear():
    os.system('clear')

def print_board(b):
    letters = [chr(ord('A') + i) for i in range(len(b[0]))]
    print("  " + "   ".join(letters))
    print("+" + "---+" * len(b[0]))
    for r in range(len(b)):
        row = []
        for c in range(len(b[0])):
            row.append(b[r][c])
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(b[0]))

def lowest_empty_row(b, col):
    for r in range(ROWS - 1, -1, -1):
        if b[r][col] == " ":
            return r
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_dir(b, r, c, dr, dc, ch):
    count = 0
    rr, cc = r, c
    while in_bounds(rr, cc) and b[rr][cc] == ch:
        count += 1
        if count == 4:
            return True
        rr += dr
        cc += dc
    return False

def check_win(b, last_r, last_c, ch):
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in dirs:
        count = 1
        rr, cc = last_r - dr, last_c - dc
        while in_bounds(rr, cc) and b[rr][cc] == ch:
            count += 1
            rr -= dr
            cc -= dc
        rr, cc = last_r + dr, last_c + dc
        while in_bounds(rr, cc) and b[rr][cc] == ch:
            count += 1
            rr += dr
            cc += dc
        if count >= 4:
            return True
    return False

def board_full(b):
    for c in range(COLS):
        if b[0][c] == " ":
            return False
    return True

def valid_col_input(s):
    if len(s) != 1:
        return False
    if not ('A' <= s <= 'Z'):
        return False
    idx = ord(s) - ord('A')
    if idx < 0 or idx >= COLS:
        return False
    return True

def main():
    board = make_board(ROWS, COLS)
    current = random.randint(0, NUM_PLAYERS - 1)

    last_move_pos = (-1, -1)
    winner = None

    while True:
        clear()
        print_board(board)
        print(f"Player {pieces[current]}, please enter a column:")
        col_in = input().strip()

        while not valid_col_input(col_in):
            print("Invalid input. Please enter a valid column letter (A-{}).".format(chr(ord('A') + COLS - 1)))
            col_in = input().strip()

        col = ord(col_in) - ord('A')
        row = lowest_empty_row(board, col)

        placed = False
        if row is not None:
            board[row][col] = pieces[current]
            placed = True
            last_move_pos = (row, col)

        if placed:
            if check_win(board, row, col, pieces[current]):
                clear()
                print_board(board)
                print(f"Player {pieces[current]} won!")
                return
            if board_full(board):
                clear()
                print_board(board)
                print("It's a draw!")
                return

        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
