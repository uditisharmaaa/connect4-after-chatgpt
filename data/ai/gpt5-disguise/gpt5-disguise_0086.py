import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2

CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

def clear():
    os.system('clear')

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

def drop(b, col, sym):
    for r in range(ROWS - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = sym
            return r
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(b, sym):
    dirs = [(1,0),(0,1),(1,1),(1,-1)]
    for r in range(ROWS):
        for c in range(COLS):
            if b[r][c] != sym:
                continue
            for dr, dc in dirs:
                ok = True
                for k in range(1,4):
                    nr = r + dr*k
                    nc = c + dc*k
                    if not in_bounds(nr, nc) or b[nr][nc] != sym:
                        ok = False
                        break
                if ok:
                    return True
    return False

def board_full(b):
    for r in range(ROWS):
        for c in range(COLS):
            if b[r][c] == " ":
                return False
    return True

def get_col_input():
    while True:
        s = input("Please enter a column: ").strip().upper()
        if len(s) != 1 or not s.isalpha():
            print("Invalid input. Enter a single letter.")
            continue
        col = ord(s) - ord('A')
        if not (0 <= col < COLS):
            print("Invalid column. Choose between A and " + chr(ord('A') + COLS - 1) + ".")
            continue
        return s, col

def main():
    if COLS > 26:
        print("Maximum 26 columns supported.")
        return
    b = make_board(ROWS, COLS)
    turn = random.randint(0, PLAYERS - 1)
    clear()
    print_board(b)
    while True:
        sym = CHECKERS[turn]
        print(f"Player {sym}, please enter a column:")
        s, col = get_col_input()
        row = drop(b, col, sym)
        if row is None:
            clear()
            print_board(b)
            print(f"Column {s} is full. Turn lost.")
            turn = (turn + 1) % PLAYERS
            continue
        clear()
        print_board(b)
        if check_win(b, sym):
            print(f"Player {sym} won!")
            break
        if board_full(b):
            print("It's a draw!")
            break
        turn = (turn + 1) % PLAYERS

if __name__ == "__main__":
    main()
