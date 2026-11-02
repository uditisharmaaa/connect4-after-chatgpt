import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]

WIN_LEN = 4

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(b, letters):
    os.system('clear')
    print("  " + "   ".join(letters))
    sep = "+" + "+".join(["---"] * len(b[0])) + "+"
    for r in range(len(b)):
        print(sep)
        row = []
        for c in range(len(b[0])):
            row.append(" " + b[r][c] + " ")
        print("|" + "|".join(row) + "|")
    print(sep)

def valid_col_input(s, letters):
    return len(s) == 1 and s in letters

def drop(b, col, t):
    for r in range(len(b)-1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = t
            return r
    return None

def check_line(a, b, c, d, t):
    return a == t and b == t and c == t and d == t

def check_win(board, t):
    rmax = len(board)
    cmax = len(board[0])

    for r in range(rmax):
        for c in range(cmax - WIN_LEN + 1):
            if check_line(board[r][c], board[r][c+1], board[r][c+2], board[r][c+3], t):
                return True

    for c in range(cmax):
        for r in range(rmax - WIN_LEN + 1):
            if check_line(board[r][c], board[r+1][c], board[r+2][c], board[r+3][c], t):
                return True

    for r in range(rmax - WIN_LEN + 1):
        for c in range(cmax - WIN_LEN + 1):
            if check_line(board[r][c], board[r+1][c+1], board[r+2][c+2], board[r+3][c+3], t):
                return True

    for r in range(WIN_LEN - 1, rmax):
        for c in range(cmax - WIN_LEN + 1):
            if check_line(board[r][c], board[r-1][c+1], board[r-2][c+2], board[r-3][c+3], t):
                return True

    return False

def board_full(b):
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

    players = TOKENS[:NUM_PLAYERS]
    letters = list(string.ascii_uppercase[:COLS])

    board = make_board(ROWS, COLS)
    turn = random.randint(0, NUM_PLAYERS - 1)

    print_board(board, letters)

    while True:
        t = players[turn]
        print(f"Player {t}, please enter a column:")
        col_in = input().strip().upper()
        while not valid_col_input(col_in, letters):
            print("Invalid input. Please enter a valid column letter:")
            col_in = input().strip().upper()

        col_idx = letters.index(col_in)
        row_put = drop(board, col_idx, t)

        if row_put is None:
            print_board(board, letters)
            print("Column is full. Turn lost.")
            turn = (turn + 1) % NUM_PLAYERS
            continue

        print_board(board, letters)

        if check_win(board, t):
            print(f"Player {t} won!")
            break

        if board_full(board):
            print("It's a draw!")
            break

        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
