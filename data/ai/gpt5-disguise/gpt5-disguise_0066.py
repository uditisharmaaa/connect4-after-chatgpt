import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2

symbols = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(b):
    os.system('clear')
    letters = list(string.ascii_uppercase[:len(b[0])])
    print("  " + "   ".join(letters))
    sep = "+" + "+".join(["---"] * len(b[0])) + "+"
    for r in range(len(b)):
        print(sep)
        row_s = "|"
        for c in range(len(b[0])):
            row_s += " " + b[r][c] + " |"
        print(row_s)
    print(sep)

def get_col_input(valid_cols, player_sym):
    while True:
        s = input(f"Player {player_sym}, please enter a column: ").strip().upper()
        if len(s) != 1:
            continue
        if s not in valid_cols:
            continue
        return valid_cols.index(s)

def drop(b, col, sym):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = sym
            return (r, col)
    return None

def full(b):
    for r in b:
        for v in r:
            if v == " ":
                return False
    return True

def check_win(b, sym):
    R = len(b)
    C = len(b[0])
    for r in range(R):
        for c in range(C - 3):
            if b[r][c] == sym and b[r][c+1] == sym and b[r][c+2] == sym and b[r][c+3] == sym:
                return True
    for r in range(R - 3):
        for c in range(C):
            if b[r][c] == sym and b[r+1][c] == sym and b[r+2][c] == sym and b[r+3][c] == sym:
                return True
    for r in range(R - 3):
        for c in range(C - 3):
            if b[r][c] == sym and b[r+1][c+1] == sym and b[r+2][c+2] == sym and b[r+3][c+3] == sym:
                return True
    for r in range(3, R):
        for c in range(C - 3):
            if b[r][c] == sym and b[r-1][c+1] == sym and b[r-2][c+2] == sym and b[r-3][c+3] == sym:
                return True
    return False

def main():
    if COLS > 26:
        print("Max 26 columns supported.")
        return
    b = make_board(ROWS, COLS)
    start = random.randint(0, NUM_PLAYERS - 1)
    turn = start
    print_board(b)
    cols_labels = list(string.ascii_uppercase[:COLS])
    while True:
        player_sym = symbols[turn]
        col = get_col_input(cols_labels, player_sym)
        pos = drop(b, col, player_sym)
        print_board(b)
        if pos is None:
            print("Column is full. Turn lost.")
        else:
            if check_win(b, player_sym):
                print(f"Player {player_sym} won!")
                break
            if full(b):
                print("It's a draw!")
                break
        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
