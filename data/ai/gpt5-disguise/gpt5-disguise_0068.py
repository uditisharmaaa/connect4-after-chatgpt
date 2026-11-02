import os
import random
import string

ROWS = 6
COLS = 7
PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]
WIN_LEN = 4

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(b):
    os.system('clear')
    letters = list(string.ascii_uppercase)[:len(b[0])]
    print("  " + "   ".join(letters))
    print("+" + "---+" * len(b[0]))
    for r in range(len(b)):
        row = "|"
        for c in range(len(b[0])):
            row += " " + b[r][c] + " |"
        print(row)
        print("+" + "---+" * len(b[0]))

def get_input(valid_cols, token):
    while True:
        s = input(f"Player {token}, please enter a column: ").strip().upper()
        if len(s) == 1 and s in valid_cols:
            return valid_cols.index(s)

def drop(b, col, token):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = token
            return (r, col)
    return None

def in_bounds(r, c, R, C):
    return 0 <= r < R and 0 <= c < C

def check_win(b, token):
    R = len(b)
    C = len(b[0])
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(R):
        for c in range(C):
            if b[r][c] != token:
                continue
            for dr, dc in dirs:
                cnt = 1
                nr, nc = r + dr, c + dc
                while cnt < WIN_LEN and in_bounds(nr, nc, R, C) and b[nr][nc] == token:
                    cnt += 1
                    nr += dr
                    nc += dc
                if cnt == WIN_LEN:
                    return True
    return False

def check_draw(b):
    for r in b:
        if " " in r:
            return False
    return True

def main():
    cols_letters = list(string.ascii_uppercase)[:min(COLS, 26)]
    players = TOKENS[:PLAYERS]
    b = make_board(ROWS, COLS)
    turn = random.randint(0, PLAYERS - 1)
    while True:
        print_board(b)
        token = players[turn]
        col = get_input(cols_letters, token)
        pos = drop(b, col, token)
        if pos is None:
            print("Column is full. Turn lost.")
            input("Press Enter to continue...")
        else:
            if check_win(b, token):
                print_board(b)
                print(f"Player {token} won!")
                break
            if check_draw(b):
                print_board(b)
                print("Game is a draw.")
                break
        turn = (turn + 1) % PLAYERS

if __name__ == "__main__":
    main()
