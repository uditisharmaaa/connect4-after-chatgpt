import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
SYMS = ["X", "O", "V", "H", "M"]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear():
    os.system('clear')

def print_board(b):
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    line = "+" + "+".join(["---"] * COLS) + "+"
    for r in range(ROWS):
        print(line)
        row = []
        for c in range(COLS):
            row.append(" " + b[r][c] + " ")
        print("|" + "|".join(row) + "|")
    print(line)

def col_from_input(s):
    s = s.strip().upper()
    if len(s) != 1:
        return None
    o = ord(s) - ord('A')
    if 0 <= o < COLS:
        return o
    return None

def drop(b, col, sym):
    for r in range(ROWS - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = sym
            return r, col
    return None

def win_from(b, r, c, sym, dr, dc):
    count = 0
    rr, cc = r, c
    for _ in range(4):
        if 0 <= rr < ROWS and 0 <= cc < COLS and b[rr][cc] == sym:
            count += 1
            rr += dr
            cc += dc
        else:
            break
    return count == 4

def check_win(b, sym):
    for r in range(ROWS):
        for c in range(COLS):
            if b[r][c] != sym:
                continue
            if c + 3 < COLS and win_from(b, r, c, sym, 0, 1):
                return True
            if r + 3 < ROWS and win_from(b, r, c, sym, 1, 0):
                return True
            if r + 3 < ROWS and c + 3 < COLS and win_from(b, r, c, sym, 1, 1):
                return True
            if r - 3 >= 0 and c + 3 < COLS and win_from(b, r, c, sym, -1, 1):
                return True
    return False

def board_full(b):
    for r in b:
        for v in r:
            if v == " ":
                return False
    return True

def main():
    b = make_board(ROWS, COLS)
    n = max(2, min(5, PLAYERS))
    players = SYMS[:n]
    cur = random.randrange(n)

    while True:
        clear()
        print_board(b)
        print(f"Player {players[cur]}, please enter a column:")
        col = None
        while True:
            s = input().strip()
            col = col_from_input(s)
            if col is not None:
                break
            print("Invalid input. Please enter a valid column letter:")
        pos = drop(b, col, players[cur])
        if pos is None:
            # column full, lose turn
            cur = (cur + 1) % n
            continue
        r, c = pos
        if check_win(b, players[cur]):
            clear()
            print_board(b)
            print(f"Player {players[cur]} won!")
            break
        if board_full(b):
            clear()
            print_board(b)
            print("It's a draw!")
            break
        cur = (cur + 1) % n

if __name__ == "__main__":
    main()
