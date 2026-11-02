import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear_screen():
    os.system('clear')

def print_board(b):
    cols = len(b[0])
    letters = string.ascii_uppercase[:cols]
    print("  " + "   ".join(letters))
    print("+" + "---+" * cols)
    for r in range(len(b)):
        row = "|"
        for c in range(cols):
            row += " " + b[r][c] + " |"
        print(row)
        print("+" + "---+" * cols)

def drop_piece(b, col, sym):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = sym
            return r, col
    return None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(b, sym):
    rows = len(b)
    cols = len(b[0])
    for r in range(rows):
        for c in range(cols):
            if b[r][c] != sym:
                continue
            # right
            if c + 3 < cols and all(b[r][c + k] == sym for k in range(4)):
                return True
            # down
            if r + 3 < rows and all(b[r + k][c] == sym for k in range(4)):
                return True
            # down-right
            if r + 3 < rows and c + 3 < cols and all(b[r + k][c + k] == sym for k in range(4)):
                return True
            # down-left
            if r + 3 < rows and c - 3 >= 0 and all(b[r + k][c - k] == sym for k in range(4)):
                return True
    return False

def board_full(b):
    for r in b:
        for v in r:
            if v == " ":
                return False
    return True

def get_valid_input(cols):
    letters = string.ascii_uppercase[:cols]
    while True:
        s = input().strip().upper()
        if len(s) == 1 and s in letters:
            return letters.index(s)
        else:
            print("Invalid input, try again:")

def main():
    cols = min(COLS, 26)
    rows = ROWS
    n = max(2, min(NUM_PLAYERS, 5))
    syms = CHECKERS[:n]

    b = make_board(rows, cols)
    cur = random.randrange(n)

    clear_screen()
    print_board(b)

    while True:
        print(f"Player {syms[cur]}, please enter a column:")
        col = get_valid_input(cols)
        pos = drop_piece(b, col, syms[cur])
        clear_screen()
        print_board(b)
        if pos is None:
            # column full, lose turn
            cur = (cur + 1) % n
            continue
        if check_win(b, syms[cur]):
            print(f"Player {syms[cur]} won!")
            break
        if board_full(b):
            print("It's a draw!")
            break
        cur = (cur + 1) % n

if __name__ == "__main__":
    main()
