import random
import os
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(b):
    os.system('clear')
    letters = [string.ascii_uppercase[i] for i in range(len(b[0]))]
    print("  " + "   ".join(letters))
    border = "+" + "+".join(["---"] * len(b[0])) + "+"
    for r in range(len(b)):
        print(border)
        row_str = "|"
        for c in range(len(b[0])):
            row_str += " " + b[r][c] + " |"
        print(row_str)
    print(border)

def valid_col_input(s, max_c):
    if len(s) != 1:
        return False
    if s not in string.ascii_uppercase:
        return False
    idx = ord(s) - ord('A')
    return 0 <= idx < max_c

def drop_piece(b, col, token):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = token
            return r, col
    return None

def in_bounds(r, c, R, C):
    return 0 <= r < R and 0 <= c < C

def check_win(b, token):
    R = len(b)
    C = len(b[0])
    for r in range(R):
        for c in range(C):
            if b[r][c] != token:
                continue
            # right
            if c + 3 < C and all(b[r][c + k] == token for k in range(4)):
                return True
            # down
            if r + 3 < R and all(b[r + k][c] == token for k in range(4)):
                return True
            # down-right
            if r + 3 < R and c + 3 < C and all(b[r + k][c + k] == token for k in range(4)):
                return True
            # down-left
            if r + 3 < R and c - 3 >= 0 and all(b[r + k][c - k] == token for k in range(4)):
                return True
    return False

def is_draw(b):
    for r in b:
        for v in r:
            if v == " ":
                return False
    return True

def main():
    if COLS > 26:
        print("Max 26 columns supported.")
        return
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Players must be between 2 and 5.")
        return

    board = make_board(ROWS, COLS)
    players = TOKENS[:NUM_PLAYERS]
    turn = random.randrange(NUM_PLAYERS)

    while True:
        print_board(board)
        p = players[turn]
        col_letter = ""
        while True:
            col_letter = input(f"Player {p}, please enter a column: ").strip().upper()
            if valid_col_input(col_letter, COLS):
                break
        col_idx = ord(col_letter) - ord('A')

        placed = drop_piece(board, col_idx, p)
        if placed is None:
            print(f"Column {col_letter} is full. Turn lost.")
            input("Press Enter to continue...")
            turn = (turn + 1) % NUM_PLAYERS
            continue

        if check_win(board, p):
            print_board(board)
            print(f"Player {p} won!")
            break

        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
