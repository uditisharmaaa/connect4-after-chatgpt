import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2

SYMS = ["X", "O", "V", "H", "M"]

def make_board(r, c):
    b = []
    for i in range(r):
        row = []
        for j in range(c):
            row.append(" ")
        b.append(row)
    return b

def print_board(b):
    letters = []
    for i in range(COLS):
        letters.append(chr(ord('A') + i))
    print("  " + "   ".join(letters))
    line = "+" + ("---+" * COLS)
    for r in range(ROWS):
        print(line)
        s = "|"
        for c in range(COLS):
            s += " " + b[r][c] + " |"
        print(s)
    print(line)

def find_row_for_col(b, col):
    for r in range(ROWS - 1, -1, -1):
        if b[r][col] == " ":
            return r
    return -1

def place(b, col, sym):
    r = find_row_for_col(b, col)
    if r == -1:
        return False
    b[r][col] = sym
    return True

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_dir(b, r, c, dr, dc, sym):
    count = 0
    for k in range(4):
        rr = r + dr * k
        cc = c + dc * k
        if not in_bounds(rr, cc):
            return False
        if b[rr][cc] != sym:
            return False
    return True

def check_win(b, sym):
    for r in range(ROWS):
        for c in range(COLS):
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
    for r in range(ROWS):
        for c in range(COLS):
            if b[r][c] == " ":
                return False
    return True

def valid_col_input(s):
    if len(s) != 1:
        return False
    if not s.isalpha():
        return False
    if not s.isupper():
        return False
    idx = ord(s) - ord('A')
    if idx < 0 or idx >= COLS:
        return False
    return True

def main():
    players = SYMS[:NUM_PLAYERS]
    board = make_board(ROWS, COLS)
    turn = random.randint(0, NUM_PLAYERS - 1)
    while True:
        os.system('clear')
        print_board(board)
        p = players[turn]
        col_input = ""
        while True:
            col_input = input(f"Player {p}, please enter a column: ").strip()
            col_input = col_input.upper()
            if valid_col_input(col_input):
                break
        col_idx = ord(col_input) - ord('A')
        placed = place(board, col_idx, p)
        if not placed:
            turn = (turn + 1) % NUM_PLAYERS
            if draw(board):
                os.system('clear')
                print_board(board)
                print("It's a draw!")
                break
            continue
        if check_win(board, p):
            os.system('clear')
            print_board(board)
            print(f"Player {p} won!")
            break
        if draw(board):
            os.system('clear')
            print_board(board)
            print("It's a draw!")
            break
        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
