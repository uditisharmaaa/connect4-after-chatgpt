import random
import os
import sys

ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # between 2 and 5

MARKS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def make_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear():
    os.system('clear')

def print_board(b):
    clear()
    letters = [chr(ord('A') + i) for i in range(len(b[0]))]
    print("  " + "   ".join(letters))
    print("+" + "---+" * len(b[0]))
    for r in range(len(b)):
        row = "|"
        for c in range(len(b[0])):
            row += " " + b[r][c] + " |"
        print(row)
        print("+" + "---+" * len(b[0]))

def drop(b, col, ch):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = ch
            return True
    return False

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(b, ch):
    rows = len(b)
    cols = len(b[0])
    for r in range(rows):
        for c in range(cols):
            if b[r][c] != ch:
                continue
            # right
            if c + 3 < cols and all(b[r][c + i] == ch for i in range(4)):
                return True
            # down
            if r + 3 < rows and all(b[r + i][c] == ch for i in range(4)):
                return True
            # down-right
            if r + 3 < rows and c + 3 < cols and all(b[r + i][c + i] == ch for i in range(4)):
                return True
            # down-left
            if r + 3 < rows and c - 3 >= 0 and all(b[r + i][c - i] == ch for i in range(4)):
                return True
    return False

def board_full(b):
    for r in b:
        for v in r:
            if v == " ":
                return False
    return True

def read_column(cols):
    valid_letters = [chr(ord('A') + i) for i in range(cols)]
    while True:
        s = input().strip()
        if len(s) != 1 or not s.isalpha():
            print("Invalid input. Please enter a single uppercase letter for a column:")
            continue
        s = s.upper()
        if s not in valid_letters:
            print("Invalid column. Please enter a letter between A and " + valid_letters[-1] + ":")
            continue
        return ord(s) - ord('A')

def main():
    if COLS > 26:
        print("Max 26 columns supported.")
        sys.exit(1)
    b = make_board(ROWS, COLS)
    current = random.randint(0, NUM_PLAYERS - 1)
    print_board(b)
    while True:
        p = MARKS[current]
        print(f"Player {p}, please enter a column:")
        col = read_column(COLS)
        placed = drop(b, col, p)
        print_board(b)
        if not placed:
            print("Column is full. Turn lost.")
        else:
            if check_win(b, p):
                print(f"Player {p} won!")
                break
            if board_full(b):
                print("It's a draw.")
                break
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
