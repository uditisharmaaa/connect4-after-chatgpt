import os
import random
import sys

ROWS = 6
COLS = 7
NUM_PLAYERS = 2

TOKENS = ["X", "O", "V", "H", "M"]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear_screen():
    os.system('clear')

def print_board(b):
    cols = len(b[0])
    letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(letters))
    print("+" + "---+" * cols)
    for r in range(len(b)):
        row_str = "|"
        for c in range(cols):
            row_str += " " + b[r][c] + " |"
        print(row_str)
        print("+" + "---+" * cols)

def drop_piece(b, col, t):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = t
            return r
    return None

def in_bounds(r, c, R, C):
    return 0 <= r < R and 0 <= c < C

def check_win(b, t):
    R = len(b)
    C = len(b[0])
    for r in range(R):
        for c in range(C):
            if b[r][c] != t:
                continue
            # right
            if c + 3 < C and all(b[r][c + k] == t for k in range(4)):
                return True
            # down
            if r + 3 < R and all(b[r + k][c] == t for k in range(4)):
                return True
            # diag down-right
            if r + 3 < R and c + 3 < C and all(b[r + k][c + k] == t for k in range(4)):
                return True
            # diag down-left
            if r + 3 < R and c - 3 >= 0 and all(b[r + k][c - k] == t for k in range(4)):
                return True
    return False

def board_full(b):
    for c in range(len(b[0])):
        if b[0][c] == " ":
            return False
    return True

def get_col_input(prompt, max_col):
    while True:
        s = input(prompt).strip().upper()
        if len(s) != 1:
            continue
        if not ('A' <= s <= 'Z'):
            continue
        col = ord(s) - ord('A')
        if 0 <= col < max_col:
            return col

def main():
    if COLS > 26:
        print("Max 26 columns")
        sys.exit(1)
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Players must be between 2 and 5")
        sys.exit(1)

    b = make_board(ROWS, COLS)
    players = TOKENS[:NUM_PLAYERS]
    current = random.randrange(NUM_PLAYERS)

    clear_screen()
    print_board(b)

    while True:
        t = players[current]
        col = get_col_input(f"Player {t}, please enter a column: ", COLS)
        row = drop_piece(b, col, t)
        if row is None:
            current = (current + 1) % NUM_PLAYERS
            clear_screen()
            print_board(b)
            continue
        clear_screen()
        print_board(b)
        if check_win(b, t):
            print(f"Player {t} won!")
            break
        if board_full(b):
            print("Game is a draw.")
            break
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
