import os
import random

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
    letters = [chr(ord('A') + i) for i in range(len(b[0]))]
    print("  " + "   ".join(letters))
    sep = "+" + "+".join(["---"] * len(b[0])) + "+"
    for r in range(len(b)):
        print(sep)
        row_cells = []
        for c in range(len(b[0])):
            row_cells.append(b[r][c])
        print("| " + " | ".join(row_cells) + " |")
    print(sep)

def column_full(b, c):
    return b[0][c] != " "

def drop(b, c, token):
    for r in range(len(b) - 1, -1, -1):
        if b[r][c] == " ":
            b[r][c] = token
            return r, c
    return None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(b, token):
    rows = len(b)
    cols = len(b[0])
    dirs = [(1,0),(0,1),(1,1),(1,-1)]
    for r in range(rows):
        for c in range(cols):
            if b[r][c] != token:
                continue
            for dr, dc in dirs:
                cnt = 1
                rr, cc = r + dr, c + dc
                while cnt < 4 and in_bounds(rr, cc, rows, cols) and b[rr][cc] == token:
                    cnt += 1
                    rr += dr
                    cc += dc
                if cnt == 4:
                    return True
    return False

def board_full(b):
    for c in range(len(b[0])):
        if b[0][c] == " ":
            return False
    return True

def get_col_index(inp, cols):
    if len(inp) != 1 or not inp.isalpha():
        return None
    x = ord(inp.upper()) - ord('A')
    if 0 <= x < cols:
        return x
    return None

def main():
    if COLS > 26:
        print("Max 26 columns supported")
        return
    b = make_board(ROWS, COLS)
    current = random.randint(0, NUM_PLAYERS - 1)
    print_board(b)
    while True:
        if board_full(b):
            print("It's a draw.")
            break
        token = TOKENS[current]
        inp = input(f"Player {token}, please enter a column: ").strip().upper()
        col = get_col_index(inp, COLS)
        while col is None:
            print_board(b)
            print("Invalid input. Please enter a valid column letter.")
            inp = input(f"Player {token}, please enter a column: ").strip().upper()
            col = get_col_index(inp, COLS)
        if column_full(b, col):
            print_board(b)
            print(f"Column {chr(ord('A')+col)} is full. Turn lost.")
            current = (current + 1) % NUM_PLAYERS
            continue
        drop(b, col, token)
        if check_win(b, token):
            print_board(b)
            print(f"Player {token} won!")
            break
        if board_full(b):
            print_board(b)
            print("It's a draw.")
            break
        print_board(b)
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
