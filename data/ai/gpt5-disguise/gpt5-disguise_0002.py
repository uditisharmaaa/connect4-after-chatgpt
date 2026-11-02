import os
import random
import string

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(b):
    os.system('clear')
    labels = [string.ascii_uppercase[i] for i in range(len(b[0]))]
    print("  " + "   ".join(labels))
    print("+---" * len(b[0]) + "+")
    for r in range(len(b)):
        row = []
        for c in range(len(b[0])):
            row.append(b[r][c])
        print("| " + " | ".join(row) + " |")
        print("+---" * len(b[0]) + "+")

def drop_piece(b, col, ch):
    for r in range(len(b)-1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = ch
            return r, col
    return None

def in_bounds(r, c, b):
    return 0 <= r < len(b) and 0 <= c < len(b[0])

def check_win(b, ch):
    for r in range(len(b)):
        for c in range(len(b[0])):
            if b[r][c] != ch:
                continue
            # right
            if all(in_bounds(r, c+i, b) and b[r][c+i] == ch for i in range(4)):
                return True
            # down
            if all(in_bounds(r+i, c, b) and b[r+i][c] == ch for i in range(4)):
                return True
            # down-right
            if all(in_bounds(r+i, c+i, b) and b[r+i][c+i] == ch for i in range(4)):
                return True
            # down-left
            if all(in_bounds(r+i, c-i, b) and b[r+i][c-i] == ch for i in range(4)):
                return True
    return False

def board_full(b):
    for r in b:
        for x in r:
            if x == " ":
                return False
    return True

def get_input(valid_cols, current_ch):
    while True:
        s = input(f"Player {current_ch}, please enter a column: ").strip().upper()
        if len(s) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        if s not in valid_cols:
            print("Invalid column. Please enter a valid letter.")
            continue
        return s

def main():
    if COLS > 26:
        print("Too many columns. Max 26.")
        return
    if PLAYERS < 2 or PLAYERS > 5:
        print("Players must be between 2 and 5.")
        return

    b = make_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS]
    turn = random.randint(0, PLAYERS - 1)

    print_board(b)

    labels = [string.ascii_uppercase[i] for i in range(COLS)]

    while True:
        ch = players[turn]
        col_label = get_input(labels, ch)
        col = ord(col_label) - ord('A')

        pos = drop_piece(b, col, ch)
        if pos is None:
            print(f"Column {col_label} is full. Turn lost.")
            turn = (turn + 1) % PLAYERS
            print_board(b)
            continue

        print_board(b)

        if check_win(b, ch):
            print(f"Player {ch} won!")
            break

        if board_full(b):
            print("It's a draw!")
            break

        turn = (turn + 1) % PLAYERS

if __name__ == "__main__":
    main()
