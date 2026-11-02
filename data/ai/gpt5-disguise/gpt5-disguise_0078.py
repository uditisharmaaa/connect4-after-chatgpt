import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
SYMS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear():
    os.system('clear')

def letters(n):
    return [chr(ord('A') + i) for i in range(n)]

def print_board(b):
    cols = letters(COLS)
    print("  " + "   ".join(cols))
    print("+" + "---+" * COLS)
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(b[r][c])
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def drop(b, col, sym):
    for r in range(ROWS - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = sym
            return r, col
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def won(b, sym):
    for r in range(ROWS):
        for c in range(COLS):
            if b[r][c] != sym:
                continue
            # right
            if c + 3 < COLS and all(b[r][c + k] == sym for k in range(4)):
                return True
            # down
            if r + 3 < ROWS and all(b[r + k][c] == sym for k in range(4)):
                return True
            # down-right
            if r + 3 < ROWS and c + 3 < COLS and all(b[r + k][c + k] == sym for k in range(4)):
                return True
            # down-left
            if r + 3 < ROWS and c - 3 >= 0 and all(b[r + k][c - k] == sym for k in range(4)):
                return True
    return False

def full(b):
    for c in range(COLS):
        if b[0][c] == " ":
            return False
    return True

def read_col():
    valid = set(letters(COLS))
    while True:
        s = input().strip().upper()
        if len(s) == 1 and s in valid:
            return ord(s) - ord('A')
        else:
            print("Invalid input, try again:")

def main():
    b = make_board(ROWS, COLS)
    cur = random.randrange(NUM_PLAYERS)
    while True:
        clear()
        print_board(b)
        print(f"Player {SYMS[cur]}, please enter a column:")
        col = read_col()
        if b[0][col] != " ":
            # column full, lose turn
            cur = (cur + 1) % NUM_PLAYERS
            continue
        drop(b, col, SYMS[cur])
        clear()
        print_board(b)
        if won(b, SYMS[cur]):
            print(f"Player {SYMS[cur]} won!")
            break
        if full(b):
            print("It's a draw!")
            break
        cur = (cur + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
