import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]

def make_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(b):
    os.system('clear')
    letters = list(string.ascii_uppercase[:len(b[0])])
    print("  " + "   ".join(letters))
    print("+---" * len(b[0]) + "+")
    for r in range(len(b)):
        row = []
        for c in range(len(b[0])):
            row.append(b[r][c])
        print("| " + " | ".join(row) + " |")
        print("+---" * len(b[0]) + "+")

def get_col_input(cols):
    while True:
        s = input("Please enter a column: ").strip().upper()
        if len(s) != 1:
            print("Invalid input.")
            continue
        if s < "A" or ord(s) > ord("A") + cols - 1:
            print("Invalid input.")
            continue
        return ord(s) - ord("A")

def drop(b, col, token):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = token
            return r, col
    return None

def check_win(b, need=4):
    rows = len(b)
    cols = len(b[0])
    dirs = [(1,0),(0,1),(1,1),(1,-1)]
    for r in range(rows):
        for c in range(cols):
            if b[r][c] == " ":
                continue
            for dr, dc in dirs:
                cnt = 0
                rr, cc = r, c
                while 0 <= rr < rows and 0 <= cc < cols and b[rr][cc] == b[r][c]:
                    cnt += 1
                    if cnt == need:
                        return b[r][c]
                    rr += dr
                    cc += dc
    return None

def is_full(b):
    for c in range(len(b[0])):
        if b[0][c] == " ":
            return False
    return True

def main():
    cols = COLS
    rows = ROWS
    if cols > 26:
        cols = 26
    players = TOKENS[:NUM_PLAYERS]
    b = make_board(rows, cols)
    start = random.randrange(len(players))
    cur = start
    print_board(b)
    while True:
        print(f"Player {players[cur]}, please enter a column:")
        col = get_col_input(cols)
        placed = drop(b, col, players[cur])
        print_board(b)
        if placed is None:
            print("Column full. Turn lost.")
        else:
            w = check_win(b, 4)
            if w:
                print(f"Player {w} won!")
                break
            if is_full(b):
                print("It's a draw!")
                break
        cur = (cur + 1) % len(players)

if __name__ == "__main__":
    main()
