import os
import random
import string

ROWS = 6
COLS = 7
PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]

def clear():
    os.system('clear')

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(b):
    labels = list(string.ascii_uppercase[:len(b[0])])
    print("  " + "   ".join(labels))
    print("+---" * len(b[0]) + "+")
    for row in b:
        line = "|"
        for cell in row:
            line += " " + cell + " |"
        print(line)
        print("+---" * len(b[0]) + "+")

def drop(b, col, token):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = token
            return r, col
    return None

def in_bounds(r, c, R, C):
    return 0 <= r < R and 0 <= c < C

def check_four(b, r, c, dr, dc, token):
    cnt = 0
    rr, cc = r, c
    while in_bounds(rr, cc, len(b), len(b[0])) and b[rr][cc] == token:
        cnt += 1
        rr += dr
        cc += dc
    rr, cc = r - dr, c - dc
    while in_bounds(rr, cc, len(b), len(b[0])) and b[rr][cc] == token:
        cnt += 1
        rr -= dr
        cc -= dc
    return cnt >= 4

def is_win(b, r, c, token):
    return (check_four(b, r, c, 0, 1, token) or
            check_four(b, r, c, 1, 0, token) or
            check_four(b, r, c, 1, 1, token) or
            check_four(b, r, c, 1, -1, token))

def is_draw(b):
    for row in b:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    players = TOKENS[:PLAYERS]
    board = make_board(ROWS, COLS)
    turn = random.randint(0, PLAYERS - 1)
    labels = list(string.ascii_uppercase[:COLS])

    clear()
    print_board(board)

    while True:
        p = players[turn]
        col_input = input(f"Player {p}, please enter a column: ").strip()
        while True:
            if len(col_input) != 1:
                col_input = input(f"Player {p}, please enter a column: ").strip()
                continue
            col_input = col_input.upper()
            if col_input not in labels:
                col_input = input(f"Player {p}, please enter a column: ").strip()
                continue
            break

        col_idx = labels.index(col_input)
        placed = drop(board, col_idx, p)
        clear()
        print_board(board)

        if placed is None:
            print(f"Column {col_input} is full. Turn lost.")
            # no placement, just switch turn
            turn = (turn + 1) % PLAYERS
            continue

        r, c = placed
        if is_win(board, r, c, p):
            print(f"Player {p} won!")
            break

        if is_draw(board):
            print("It's a draw!")
            break

        turn = (turn + 1) % PLAYERS

if __name__ == "__main__":
    main()
