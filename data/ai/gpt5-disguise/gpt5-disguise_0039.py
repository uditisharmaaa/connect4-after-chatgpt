import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear():
    os.system('clear')

def print_board(b):
    letters = [string.ascii_uppercase[i] for i in range(COLS)]
    header = "  " + "   ".join(letters)
    line = "+" + "+".join(["---"] * COLS) + "+"
    print(header)
    print(line)
    for r in range(ROWS):
        row = "|"
        for c in range(COLS):
            row += " " + b[r][c] + " |"
        print(row)
        print(line)

def drop(b, col, t):
    for r in range(ROWS - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = t
            return r
    return -1

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_dir(b, r, c, dr, dc, t):
    cnt = 0
    rr, cc = r, c
    while in_bounds(rr, cc) and b[rr][cc] == t:
        cnt += 1
        rr += dr
        cc += dc
    rr, cc = r - dr, c - dc
    while in_bounds(rr, cc) and b[rr][cc] == t:
        cnt += 1
        rr -= dr
        cc -= dc
    return cnt >= 4

def won(b, r, c, t):
    return (check_dir(b, r, c, 0, 1, t) or
            check_dir(b, r, c, 1, 0, t) or
            check_dir(b, r, c, 1, 1, t) or
            check_dir(b, r, c, 1, -1, t))

def full(b):
    for c in range(COLS):
        if b[0][c] == " ":
            return False
    return True

def main():
    random.seed()
    b = make_board(ROWS, COLS)
    players = TOKENS[:NUM_PLAYERS]
    turn = random.randint(0, NUM_PLAYERS - 1)

    clear()
    print_board(b)

    while True:
        t = players[turn]
        print(f"Player {t}, please enter a column:")
        s = input().strip().upper()

        while True:
            if len(s) == 1 and 'A' <= s <= chr(ord('A') + COLS - 1):
                col = ord(s) - ord('A')
                r = drop(b, col, t)
                if r == -1:
                    clear()
                    print_board(b)
                    # turn lost
                    turn = (turn + 1) % NUM_PLAYERS
                else:
                    if won(b, r, col, t):
                        clear()
                        print_board(b)
                        print(f"Player {t} won!")
                        return
                    if full(b):
                        clear()
                        print_board(b)
                        print("It's a draw!")
                        return
                    turn = (turn + 1) % NUM_PLAYERS
                    clear()
                    print_board(b)
                break
            else:
                print("Invalid input. Please enter a valid column letter:")
                s = input().strip().upper()

if __name__ == "__main__":
    main()
