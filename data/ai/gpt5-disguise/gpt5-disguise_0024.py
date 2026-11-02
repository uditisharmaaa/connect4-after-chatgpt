import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear_screen():
    os.system('clear')

def print_board(b):
    clear_screen()
    header = "  " + "   ".join(string.ascii_uppercase[:len(b[0])])
    print(header)
    print("+" + "---+" * len(b[0]))
    for r in range(len(b)):
        row = "|"
        for c in range(len(b[0])):
            row += f" {b[r][c]} |"
        print(row)
        print("+" + "---+" * len(b[0]))

def col_index(ch):
    if len(ch) != 1:
        return -1
    if ch < "A" or ch > "Z":
        return -1
    idx = ord(ch) - ord("A")
    return idx

def next_free_row(b, c):
    for r in range(ROWS - 1, -1, -1):
        if b[r][c] == " ":
            return r
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def count_dir(b, r, c, dr, dc, ch):
    cnt = 0
    rr, cc = r, c
    while in_bounds(rr, cc) and b[rr][cc] == ch:
        cnt += 1
        rr += dr
        cc += dc
    return cnt

def check_win(b, r, c, ch):
    # horizontal
    a = count_dir(b, r, c, 0, -1, ch) - 1
    b1 = count_dir(b, r, c, 0, 1, ch)
    if a + b1 >= 4: return True
    # vertical
    a = count_dir(b, r, c, -1, 0, ch) - 1
    b1 = count_dir(b, r, c, 1, 0, ch)
    if a + b1 >= 4: return True
    # diag \
    a = count_dir(b, r, c, -1, -1, ch) - 1
    b1 = count_dir(b, r, c, 1, 1, ch)
    if a + b1 >= 4: return True
    # diag /
    a = count_dir(b, r, c, -1, 1, ch) - 1
    b1 = count_dir(b, r, c, 1, -1, ch)
    if a + b1 >= 4: return True
    return False

def is_draw(b):
    for r in b:
        for v in r:
            if v == " ":
                return False
    return True

def main():
    players = TOKENS[:max(2, min(5, NUM_PLAYERS))]
    board = make_board(ROWS, COLS)
    cur = random.randrange(len(players))
    print_board(board)
    while True:
        p = players[cur]
        print(f"Player {p}, please enter a column:")
        col = None
        while True:
            s = input().strip().upper()
            idx = col_index(s)
            if idx == -1 or idx >= COLS:
                print("Invalid input. Please enter a valid column letter:")
                continue
            col = idx
            break
        r = next_free_row(board, col)
        if r is None:
            print("Column is full. Turn lost.")
            cur = (cur + 1) % len(players)
            print_board(board)
            continue
        board[r][col] = p
        print_board(board)
        if check_win(board, r, col, p):
            print(f"Player {p} won!")
            break
        if is_draw(board):
            print("It's a draw!")
            break
        cur = (cur + 1) % len(players)

if __name__ == "__main__":
    main()
