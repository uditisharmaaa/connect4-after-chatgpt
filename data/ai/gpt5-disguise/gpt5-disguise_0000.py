import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PIECES = ["X", "O", "V", "H", "M"]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(b):
    letters = [string.ascii_uppercase[i] for i in range(len(b[0]))]
    print("  " + "   ".join(letters))
    print("+" + ("---+" * len(b[0])))
    for r in range(len(b)):
        row = "|"
        for c in range(len(b[0])):
            row += " " + b[r][c] + " |"
        print(row)
        print("+" + ("---+" * len(b[0])))

def drop_piece(b, col, piece):
    for r in range(len(b)-1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = piece
            return True
    return False

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(b, piece):
    rows = len(b)
    cols = len(b[0])
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(rows):
        for c in range(cols):
            if b[r][c] != piece:
                continue
            for dr, dc in dirs:
                cnt = 0
                rr, cc = r, c
                for _ in range(4):
                    if in_bounds(rr, cc, rows, cols) and b[rr][cc] == piece:
                        cnt += 1
                        rr += dr
                        cc += dc
                    else:
                        break
                if cnt == 4:
                    return True
    return False

def board_full(b):
    for r in b:
        for c in r:
            if c == " ":
                return False
    return True

def get_col_index(inp, max_cols):
    if len(inp) != 1:
        return -1
    if inp < 'A' or inp > 'Z':
        return -1
    idx = ord(inp) - ord('A')
    if idx < 0 or idx >= max_cols:
        return -1
    return idx

def main():
    if COLS > 26:
        print("Max 26 columns supported.")
        return
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Players must be between 2 and 5.")
        return

    b = make_board(ROWS, COLS)
    players = PIECES[:NUM_PLAYERS]
    cur = random.randint(0, NUM_PLAYERS - 1)

    os.system('clear')
    print_board(b)

    while True:
        p = players[cur]
        print(f"Player {p}, please enter a column:")
        x = input().strip().upper()
        while True:
            col = get_col_index(x, COLS)
            if col == -1:
                print("Invalid input. Please enter a valid column letter:")
                x = input().strip().upper()
                continue
            placed = drop_piece(b, col, p)
            if not placed:
                os.system('clear')
                print_board(b)
                print("Column is full. Turn lost.")
                cur = (cur + 1) % NUM_PLAYERS
                break
            os.system('clear')
            print_board(b)
            if check_win(b, p):
                print(f"Player {p} won!")
                return
            if board_full(b):
                print("The game is a draw.")
                return
            cur = (cur + 1) % NUM_PLAYERS
            break

if __name__ == "__main__":
    main()
