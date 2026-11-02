import os
import random

ROWS = 6
COLS = 7
N_PLAYERS = 2

SYMS = ["X", "O", "V", "H", "M"]


def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]


def print_board(b, labels):
    os.system('clear')
    header = "  " + "   ".join(labels)
    print(header)
    sep = "+" + "+".join(["---"] * len(labels)) + "+"
    for r in range(len(b)):
        print(sep)
        row = "|"
        for c in range(len(b[0])):
            row += " " + b[r][c] + " |"
        print(row)
    print(sep)


def drop(b, col, sym):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = sym
            return True
    return False


def win(b, sym):
    R = len(b)
    C = len(b[0])
    for r in range(R):
        for c in range(C):
            if b[r][c] != sym:
                continue
            # right
            if c + 3 < C and b[r][c+1] == sym and b[r][c+2] == sym and b[r][c+3] == sym:
                return True
            # down
            if r + 3 < R and b[r+1][c] == sym and b[r+2][c] == sym and b[r+3][c] == sym:
                return True
            # diag down-right
            if r + 3 < R and c + 3 < C and b[r+1][c+1] == sym and b[r+2][c+2] == sym and b[r+3][c+3] == sym:
                return True
            # diag down-left
            if r + 3 < R and c - 3 >= 0 and b[r+1][c-1] == sym and b[r+2][c-2] == sym and b[r+3][c-3] == sym:
                return True
    return False


def full(b):
    for r in b:
        for v in r:
            if v == " ":
                return False
    return True


def main():
    if COLS > 26:
        print("Max 26 columns supported.")
        return
    players = SYMS[:N_PLAYERS]
    labels = [chr(ord('A') + i) for i in range(COLS)]
    lab_to_idx = {labels[i]: i for i in range(COLS)}
    b = make_board(ROWS, COLS)
    turn = random.randint(0, N_PLAYERS - 1)
    while True:
        print_board(b, labels)
        p = players[turn]
        col_input = ""
        while True:
            col_input = input(f"Player {p}, please enter a column: ").strip().upper()
            if len(col_input) != 1:
                continue
            if col_input not in lab_to_idx:
                continue
            break
        cidx = lab_to_idx[col_input]
        placed = drop(b, cidx, p)
        if placed:
            if win(b, p):
                print_board(b, labels)
                print(f"Player {p} won!")
                break
            if full(b):
                print_board(b, labels)
                print("It's a draw!")
                break
        # if not placed, turn is lost
        turn = (turn + 1) % N_PLAYERS


if __name__ == "__main__":
    main()
