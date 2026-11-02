import random
import os

ROWS = 6
COLS = 7
MAX_COLS = 26
NPLAYERS = 2
TOKENS_ALL = ["X", "O", "V", "H", "M"]
TOKENS = TOKENS_ALL[:NPLAYERS]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear_screen():
    os.system('clear')

def print_board(b):
    clear_screen()
    letters = [chr(ord('A') + i) for i in range(len(b[0]))]
    top = "  " + "   ".join(letters)
    print(top)
    line = "+" + ("---+" * len(b[0]))
    for r in range(len(b)):
        print(line)
        row_str = ""
        for c in range(len(b[0])):
            row_str += "|" + " " + b[r][c] + " "
        row_str += "|"
        print(row_str)
    print(line)

def col_from_input(s):
    if not s or len(s) != 1:
        return None
    ch = s.upper()
    if not ('A' <= ch <= 'Z'):
        return None
    idx = ord(ch) - ord('A')
    if 0 <= idx < COLS:
        return idx
    return None

def drop_checker(b, col, token):
    for r in range(ROWS - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = token
            return r, col
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win_from(b, r, c, dr, dc):
    t = b[r][c]
    if t == " ":
        return False
    count = 0
    rr, cc = r, c
    while in_bounds(rr, cc) and b[rr][cc] == t:
        count += 1
        if count == 4:
            return True
        rr += dr
        cc += dc
    return False

def check_win(b):
    for r in range(ROWS):
        for c in range(COLS):
            if b[r][c] == " ":
                continue
            if check_win_from(b, r, c, 0, 1):   # horizontal
                return True
            if check_win_from(b, r, c, 1, 0):   # vertical
                return True
            if check_win_from(b, r, c, 1, 1):   # diag down-right
                return True
            if check_win_from(b, r, c, 1, -1):  # diag down-left
                return True
    return False

def board_full(b):
    for c in range(COLS):
        if b[0][c] == " ":
            return False
    return True

def main():
    if COLS > MAX_COLS:
        print("Too many columns.")
        return
    b = make_board(ROWS, COLS)
    cur = random.randrange(NPLAYERS)
    print_board(b)
    while True:
        token = TOKENS[cur]
        print(f"Player {token}, please enter a column:")
        while True:
            s = input().strip()
            col = col_from_input(s)
            if col is None:
                print_board(b)
                print(f"Player {token}, please enter a column:")
                continue
            res = drop_checker(b, col, token)
            if res is None:
                print_board(b)
                # turn lost if column full
                break
            print_board(b)
            if check_win(b):
                print(f"Player {token} won!")
                return
            if board_full(b):
                print("It's a draw.")
                return
            # move successful, go to next player
            break
        cur = (cur + 1) % NPLAYERS

if __name__ == "__main__":
    main()
