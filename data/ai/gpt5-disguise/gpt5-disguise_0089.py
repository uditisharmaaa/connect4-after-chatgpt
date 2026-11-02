import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def make_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(b):
    cols = len(b[0])
    letters = string.ascii_uppercase[:cols]
    print("  " + "   ".join(list(letters)))
    print("+" + "---+" * cols)
    for r in range(len(b)):
        row = "|" + "|".join(f" {b[r][c]} " for c in range(cols)) + "|"
        print(row)
        print("+" + "---+" * cols)

def clear():
    os.system('clear')

def get_input(cols):
    letters = string.ascii_uppercase[:cols]
    while True:
        s = input().strip().upper()
        if len(s) == 1 and s in letters:
            return letters.index(s)
        print("Invalid input. Please enter a valid column letter:")

def drop(b, col, ch):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = ch
            return r, col
    return None

def check_win(b):
    rows = len(b)
    cols = len(b[0])
    dirs = [(0,1),(1,0),(1,1),(-1,1)]
    for r in range(rows):
        for c in range(cols):
            if b[r][c] == " ":
                continue
            for dr, dc in dirs:
                cnt = 1
                rr, cc = r, c
                for _ in range(3):
                    rr += dr
                    cc += dc
                    if 0 <= rr < rows and 0 <= cc < cols and b[rr][cc] == b[r][c]:
                        cnt += 1
                    else:
                        break
                if cnt >= 4:
                    return True
    return False

def check_draw(b):
    for c in range(len(b[0])):
        if b[0][c] == " ":
            return False
    return True

def main():
    players = CHECKERS[:NUM_PLAYERS]
    b = make_board(ROWS, COLS)
    turn = random.randrange(len(players))
    clear()
    print_board(b)
    while True:
        p = players[turn]
        print(f"Player {p}, please enter a column:")
        col = get_input(COLS)
        res = drop(b, col, p)
        if res is None:
            clear()
            print_board(b)
            print("Column is full. Turn lost.")
            turn = (turn + 1) % len(players)
            continue
        clear()
        print_board(b)
        if check_win(b):
            print(f"Player {p} won!")
            break
        if check_draw(b):
            print("It's a draw!")
            break
        turn = (turn + 1) % len(players)

if __name__ == "__main__":
    main()
