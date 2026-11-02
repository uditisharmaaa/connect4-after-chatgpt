import random
import os
import sys

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PIECES = ["X", "O", "V", "H", "M"]
WIN_N = 4

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear():
    os.system('clear')

def col_labels(n):
    return [chr(ord('A') + i) for i in range(n)]

def print_board(board):
    labels = col_labels(len(board[0]))
    print("  " + "   ".join(labels))
    print("+" + "+".join(["---"] * len(board[0])) + "+")
    for row in board:
        print("|" + "|".join(f" {cell} " for cell in row) + "|")
        print("+" + "+".join(["---"] * len(board[0])) + "+")

def letter_to_col(ch):
    if len(ch) != 1 or not ch.isalpha():
        return None
    ch = ch.upper()
    idx = ord(ch) - ord('A')
    if 0 <= idx < COLS:
        return idx
    return None

def drop_piece(board, col, p):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = p
            return r
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(board, p):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != p:
                continue
            # right
            ok = True
            for k in range(WIN_N):
                if not in_bounds(r, c + k) or board[r][c + k] != p:
                    ok = False
                    break
            if ok:
                return True
            # down
            ok = True
            for k in range(WIN_N):
                if not in_bounds(r + k, c) or board[r + k][c] != p:
                    ok = False
                    break
            if ok:
                return True
            # diag down-right
            ok = True
            for k in range(WIN_N):
                if not in_bounds(r + k, c + k) or board[r + k][c + k] != p:
                    ok = False
                    break
            if ok:
                return True
            # diag down-left
            ok = True
            for k in range(WIN_N):
                if not in_bounds(r + k, c - k) or board[r + k][c - k] != p:
                    ok = False
                    break
            if ok:
                return True
    return False

def board_full(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def main():
    if COLS > 26:
        print("Max 26 columns supported.")
        sys.exit(1)
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Players must be between 2 and 5.")
        sys.exit(1)

    board = make_board(ROWS, COLS)
    players = PIECES[:NUM_PLAYERS]
    turn = random.randrange(NUM_PLAYERS)

    clear()
    print_board(board)

    while True:
        p = players[turn]
        print(f"Player {p}, please enter a column:")
        while True:
            s = input().strip()
            if len(s) == 0:
                print(f"Player {p}, please enter a column:")
                continue
            col = letter_to_col(s[0])
            if col is None:
                print("Invalid input. Please enter a valid column letter.")
                continue
            break

        row_placed = drop_piece(board, col, p)
        clear()
        print_board(board)

        if row_placed is None:
            # column full, lose turn
            turn = (turn + 1) % NUM_PLAYERS
        else:
            if check_win(board, p):
                print(f"Player {p} won!")
                break
            if board_full(board):
                print("It's a draw!")
                break
            turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
