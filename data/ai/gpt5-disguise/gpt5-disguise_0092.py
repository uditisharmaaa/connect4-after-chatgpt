import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]

if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    raise SystemExit("NUM_PLAYERS must be between 2 and 5")
if COLS > 26:
    raise SystemExit("COLS must be at most 26")

players = TOKENS[:NUM_PLAYERS]
labels = list(string.ascii_uppercase[:COLS])

def make_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(b):
    header = "  " + "   ".join(labels)
    line = "+" + ("---+" * COLS)
    print(header)
    print(line)
    for r in range(ROWS):
        row_cells = []
        for c in range(COLS):
            row_cells.append(b[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print(line)

def drop(b, col_idx, ch):
    for r in range(ROWS - 1, -1, -1):
        if b[r][col_idx] == " ":
            b[r][col_idx] = ch
            return True
    return False

def check_win(b, ch):
    for r in range(ROWS):
        for c in range(COLS):
            if b[r][c] != ch:
                continue
            # right
            if c + 3 < COLS and all(b[r][c + k] == ch for k in range(4)):
                return True
            # down
            if r + 3 < ROWS and all(b[r + k][c] == ch for k in range(4)):
                return True
            # down-right
            if r + 3 < ROWS and c + 3 < COLS and all(b[r + k][c + k] == ch for k in range(4)):
                return True
            # down-left
            if r + 3 < ROWS and c - 3 >= 0 and all(b[r + k][c - k] == ch for k in range(4)):
                return True
    return False

def is_draw(b):
    for r in range(ROWS):
        for c in range(COLS):
            if b[r][c] == " ":
                return False
    return True

def get_input():
    while True:
        s = input().strip()
        if len(s) != 1:
            print("Invalid input. Try again:")
            continue
        ch = s.upper()
        if ch not in labels:
            print("Invalid input. Try again:")
            continue
        return labels.index(ch)

def main():
    b = make_board()
    turn = random.randrange(NUM_PLAYERS)

    while True:
        os.system('clear')
        print_board(b)
        curr = players[turn]
        print(f"Player {curr}, please enter a column:")
        col = get_input()

        placed = drop(b, col, curr)
        if not placed:
            print("Column is full. Turn lost.")
            turn = (turn + 1) % NUM_PLAYERS
            input()  # wait for enter
            continue

        if check_win(b, curr):
            os.system('clear')
            print_board(b)
            print(f"Player {curr} won!")
            break

        if is_draw(b):
            os.system('clear')
            print_board(b)
            print("It's a draw!")
            break

        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
