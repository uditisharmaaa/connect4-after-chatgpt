import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear_and_print(b):
    os.system('clear')
    letters = [chr(ord('A') + i) for i in range(len(b[0]))]
    print("  " + "   ".join(letters))
    print("+" + ("---+" * len(b[0])))
    for row in b:
        print("|" + "|".join(" {} ".format(x) for x in row) + "|")
        print("+" + ("---+" * len(b[0])))

def get_col_input(c):
    while True:
        s = input("Please enter a column: ").strip().upper()
        if len(s) == 1 and 'A' <= s <= chr(ord('A') + c - 1):
            return ord(s) - ord('A')
        else:
            print("Invalid input. Enter a letter between A and {}.".format(chr(ord('A') + c - 1)))

def place(b, col, token):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = token
            return r
    return None

def in_bounds(r, c, rmax, cmax):
    return 0 <= r < rmax and 0 <= c < cmax

def check_win(b, r, c, token):
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in dirs:
        count = 1
        rr, cc = r + dr, c + dc
        while in_bounds(rr, cc, len(b), len(b[0])) and b[rr][cc] == token:
            count += 1
            rr += dr
            cc += dc
        rr, cc = r - dr, c - dc
        while in_bounds(rr, cc, len(b), len(b[0])) and b[rr][cc] == token:
            count += 1
            rr -= dr
            cc -= dc
        if count >= WIN_COUNT:
            return True
    return False

def board_full(b):
    for row in b:
        for x in row:
            if x == " ":
                return False
    return True

def main():
    if COLS > 26:
        print("Maximum 26 columns supported.")
        return
    n = max(2, min(5, NUM_PLAYERS))
    players = TOKENS[:n]
    b = make_board(ROWS, COLS)
    turn = random.randint(0, n - 1)
    clear_and_print(b)
    while True:
        p = players[turn]
        print("Player {}, {}".format(p, "please enter a column:"))
        col = get_col_input(COLS)
        row_placed = place(b, col, p)
        clear_and_print(b)
        if row_placed is None:
            print("Column is full. Player {} loses the turn.".format(p))
        else:
            if check_win(b, row_placed, col, p):
                print("Player {} won!".format(p))
                break
        if board_full(b):
            print("It's a draw!")
            break
        turn = (turn + 1) % n

if __name__ == "__main__":
    main()
