import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2

SYMS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
LETTERS = list(string.ascii_uppercase[:min(COLS, 26)])

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear():
    os.system('clear')

def print_board(b):
    header = "  " + "   ".join(LETTERS)
    line = "+" + "+".join(["---"] * len(b[0])) + "+"
    print(header)
    for r in range(len(b)):
        print(line)
        row = "|" + "|".join(f" {b[r][c]} " for c in range(len(b[0]))) + "|"
        print(row)
    print(line)

def drop(b, col, sym):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = sym
            return r
    return None

def in_bounds(r, c, R, C):
    return 0 <= r < R and 0 <= c < C

def check_win(b, sym):
    R = len(b)
    C = len(b[0])
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(R):
        for c in range(C):
            if b[r][c] != sym:
                continue
            for dr, dc in dirs:
                cnt = 1
                rr, cc = r + dr, c + dc
                while cnt < 4 and in_bounds(rr, cc, R, C) and b[rr][cc] == sym:
                    cnt += 1
                    rr += dr
                    cc += dc
                if cnt == 4:
                    return True
    return False

def is_draw(b):
    for row in b:
        if " " in row:
            return False
    return True

def read_move():
    while True:
        s = input().strip().upper()
        if len(s) != 1 or s not in LETTERS:
            print("Invalid input. Please enter a valid column letter:")
            continue
        return LETTERS.index(s), s

def main():
    random.seed()
    board = make_board(ROWS, COLS)
    current = random.randrange(NUM_PLAYERS)

    clear()
    print_board(board)

    while True:
        sym = SYMS[current]
        print(f"Player {sym}, please enter a column:")
        col_idx, col_letter = read_move()

        row = drop(board, col_idx, sym)
        clear()
        print_board(board)

        if row is None:
            print(f"Column {col_letter} is full. Turn lost.")
        else:
            if check_win(board, sym):
                print(f"Player {sym} won!")
                break
            if is_draw(board):
                print("It's a draw!")
                break

        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
