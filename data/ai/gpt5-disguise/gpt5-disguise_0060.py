import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2

SYMS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(b):
    letters = "  " + "   ".join(string.ascii_uppercase[:len(b[0])])
    print(letters)
    sep = "+" + "+".join(["---"] * len(b[0])) + "+"
    for row in b:
        print(sep)
        line = "|"
        for cell in row:
            line += f" {cell} |"
        print(line)
    print(sep)

def clear():
    os.system('clear')

def valid_col_input(s):
    if len(s) != 1:
        return False
    ch = s.upper()
    if ch < 'A' or ch >= chr(ord('A') + COLS):
        return False
    return True

def col_full(b, c):
    return b[0][c] != " "

def drop(b, c, sym):
    for r in range(ROWS - 1, -1, -1):
        if b[r][c] == " ":
            b[r][c] = sym
            return r, c
    return None

def win_from(b, r, c, sym, dr, dc):
    count = 0
    rr, cc = r, c
    while 0 <= rr < ROWS and 0 <= cc < COLS and b[rr][cc] == sym:
        count += 1
        rr += dr
        cc += dc
    return count

def check_win(b, sym):
    for r in range(ROWS):
        for c in range(COLS):
            if b[r][c] != sym:
                continue
            # right
            if c + 3 < COLS and all(b[r][c + k] == sym for k in range(4)):
                return True
            # down
            if r + 3 < ROWS and all(b[r + k][c] == sym for k in range(4)):
                return True
            # diag down-right
            if r + 3 < ROWS and c + 3 < COLS and all(b[r + k][c + k] == sym for k in range(4)):
                return True
            # diag down-left
            if r + 3 < ROWS and c - 3 >= 0 and all(b[r + k][c - k] == sym for k in range(4)):
                return True
    return False

def board_full(b):
    for c in range(COLS):
        if not col_full(b, c):
            return False
    return True

def main():
    random.seed()
    board = make_board(ROWS, COLS)
    turn = random.randrange(NUM_PLAYERS)
    clear()
    print_board(board)
    while True:
        sym = SYMS[turn]
        choice = ""
        while True:
            choice = input(f"Player {sym}, please enter a column: ").strip().upper()
            if valid_col_input(choice):
                break
        col = ord(choice) - ord('A')
        if col_full(board, col):
            turn = (turn + 1) % NUM_PLAYERS
            clear()
            print_board(board)
            continue
        drop(board, col, sym)
        if check_win(board, sym):
            clear()
            print_board(board)
            print(f"Player {sym} won!")
            break
        if board_full(board):
            clear()
            print_board(board)
            print("It's a draw!")
            break
        turn = (turn + 1) % NUM_PLAYERS
        clear()
        print_board(board)

if __name__ == "__main__":
    main()
