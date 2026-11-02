import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHARS = ["X", "O", "V", "H", "M"]
WIN_LEN = 4

players = CHARS[:NUM_PLAYERS]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(b):
    os.system('clear')
    letters = [chr(ord('A') + i) for i in range(len(b[0]))]
    print("  " + "   ".join(letters))
    print("+" + "---+" * len(b[0]))
    for r in range(len(b)):
        row = "|"
        for c in range(len(b[0])):
            row += " " + b[r][c] + " |"
        print(row)
        print("+" + "---+" * len(b[0]))

def drop(b, col, ch):
    for r in range(ROWS - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = ch
            return True
    return False

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_direction(b, r, c, dr, dc, ch):
    count = 0
    for i in range(WIN_LEN):
        rr = r + dr * i
        cc = c + dc * i
        if in_bounds(rr, cc) and b[rr][cc] == ch:
            count += 1
        else:
            return False
    return count == WIN_LEN

def check_win_for(b, ch):
    for r in range(ROWS):
        for c in range(COLS):
            if b[r][c] != ch:
                continue
            if check_direction(b, r, c, 0, 1, ch):
                return True
            if check_direction(b, r, c, 1, 0, ch):
                return True
            if check_direction(b, r, c, 1, 1, ch):
                return True
            if check_direction(b, r, c, 1, -1, ch):
                return True
    return False

def board_full(b):
    for r in range(ROWS):
        for c in range(COLS):
            if b[r][c] == " ":
                return False
    return True

def get_col_input(valid_max):
    while True:
        inp = input().strip()
        if len(inp) != 1:
            print("Invalid input. Enter a single letter.")
            continue
        ch = inp.upper()
        if not ch.isalpha():
            print("Invalid input. Enter a letter.")
            continue
        idx = ord(ch) - ord('A')
        if idx < 0 or idx >= valid_max:
            print("Invalid column. Try again.")
            continue
        return idx

def main():
    board = make_board(ROWS, COLS)
    current = random.randrange(NUM_PLAYERS)
    while True:
        print_board(board)
        sym = players[current]
        print(f"Player {sym}, please enter a column:")
        col = get_col_input(COLS)
        placed = drop(board, col, sym)
        if placed:
            if check_win_for(board, sym):
                print_board(board)
                print(f"Player {sym} won!")
                break
        else:
            # turn lost
            pass
        if board_full(board):
            print_board(board)
            print("It's a draw!")
            break
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
