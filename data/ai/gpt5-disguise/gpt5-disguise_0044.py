import os
import random
import sys

ROWS = 6
COLS = 7
NUM_PLAYERS = 2

SYMS_ALL = ["X", "O", "V", "H", "M"]
SYMS = SYMS_ALL[:NUM_PLAYERS]

board = [[" " for _ in range(COLS)] for _ in range(ROWS)]

def clear():
    os.system('clear')

def print_board():
    clear()
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    print("+---" * COLS + "+")
    for r in range(ROWS):
        row = "|"
        for c in range(COLS):
            row += " " + board[r][c] + " |"
        print(row)
        print("+---" * COLS + "+")

def drop(col, sym):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = sym
            return r, col
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(sym):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != sym:
                continue
            # right
            if c + 3 < COLS and all(board[r][c + k] == sym for k in range(4)):
                return True
            # down
            if r + 3 < ROWS and all(board[r + k][c] == sym for k in range(4)):
                return True
            # down-right
            if r + 3 < ROWS and c + 3 < COLS and all(board[r + k][c + k] == sym for k in range(4)):
                return True
            # down-left
            if r + 3 < ROWS and c - 3 >= 0 and all(board[r + k][c - k] == sym for k in range(4)):
                return True
    return False

def board_full():
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def get_col_input(sym):
    while True:
        s = input().strip().upper()
        if len(s) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        if not ('A' <= s <= chr(ord('A') + COLS - 1)):
            print("Invalid input. Column out of range.")
            continue
        return ord(s) - ord('A')

def main():
    if COLS > 26 or COLS < 1 or ROWS < 1:
        print("Invalid board size.")
        sys.exit(1)

    p = random.randrange(NUM_PLAYERS)

    while True:
        print_board()
        print(f"Player {SYMS[p]}, please enter a column:")
        col = get_col_input(SYMS[p])

        if board[0][col] != " ":
            # column full, lose turn
            p = (p + 1) % NUM_PLAYERS
            continue

        drop(col, SYMS[p])

        if check_win(SYMS[p]):
            print_board()
            print(f"Player {SYMS[p]} won!")
            break

        if board_full():
            print_board()
            print("It's a draw!")
            break

        p = (p + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
