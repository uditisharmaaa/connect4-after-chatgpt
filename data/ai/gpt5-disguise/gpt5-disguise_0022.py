import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def clear():
    os.system('clear')

def make_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(b):
    clear()
    letters = list(string.ascii_uppercase[:len(b[0])])
    print("  " + "   ".join(letters))
    sep = "+" + ("---+" * len(b[0]))
    for r in range(len(b)):
        print(sep)
        row_str = []
        for c in range(len(b[0])):
            row_str.append(b[r][c])
        print("| " + " | ".join(row_str) + " |")
    print(sep)

def drop(b, col, token):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = token
            return r, col
    return None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(b, token):
    rows = len(b)
    cols = len(b[0])
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(rows):
        for c in range(cols):
            if b[r][c] != token:
                continue
            for dr, dc in dirs:
                ok = True
                for k in range(1,4):
                    nr = r + dr*k
                    nc = c + dc*k
                    if not in_bounds(nr, nc, rows, cols) or b[nr][nc] != token:
                        ok = False
                        break
                if ok:
                    return True
    return False

def board_full(b):
    for row in b:
        if " " in row:
            return False
    return True

def get_col_input(valid_cols):
    while True:
        s = input().strip().upper()
        if len(s) != 1:
            print("Invalid input. Enter a single letter.")
            continue
        if s not in valid_cols:
            print("Invalid column. Try again.")
            continue
        return valid_cols.index(s)

def main():
    if COLS > 26:
        print("Max 26 columns supported.")
        return
    b = make_board(ROWS, COLS)
    current = random.randrange(NUM_PLAYERS)
    letters = list(string.ascii_uppercase[:COLS])

    print_board(b)
    while True:
        token = TOKENS[current]
        print(f"Player {token}, please enter a column:")
        col = get_col_input(letters)

        placed = drop(b, col, token)
        print_board(b)

        if placed is None:
            print("Column is full. Turn lost.")
        else:
            if check_win(b, token):
                print(f"Player {token} won!")
                break
            if board_full(b):
                print("It's a draw!")
                break

        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
