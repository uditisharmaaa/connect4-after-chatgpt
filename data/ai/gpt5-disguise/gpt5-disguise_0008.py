import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LEN = 4

CHARS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(b):
    letters = [chr(ord('A') + i) for i in range(len(b[0]))]
    header = "  " + "   ".join(letters)
    line = "+" + "+".join(["---"] * len(b[0])) + "+"
    print(header)
    for r in range(len(b)):
        print(line)
        row_str = "|"
        for c in range(len(b[0])):
            row_str += " " + b[r][c] + " |"
        print(row_str)
    print(line)

def drop(b, col, ch):
    for r in range(ROWS - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = ch
            return r
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(b, r, c, ch):
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in dirs:
        cnt = 1
        rr, cc = r + dr, c + dc
        while in_bounds(rr, cc) and b[rr][cc] == ch:
            cnt += 1
            rr += dr
            cc += dc
        rr, cc = r - dr, c - dc
        while in_bounds(rr, cc) and b[rr][cc] == ch:
            cnt += 1
            rr -= dr
            cc -= dc
        if cnt >= WIN_LEN:
            return True
    return False

def main():
    if COLS > 26:
        print("Max 26 columns allowed.")
        return
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Players must be between 2 and 5.")
        return

    b = make_board(ROWS, COLS)
    moves = 0
    turn = random.randint(0, NUM_PLAYERS - 1)

    while True:
        os.system('clear')
        print_board(b)
        print(f"Player {CHARS[turn]}, please enter a column:")
        col = None
        while True:
            s = input().strip().upper()
            if len(s) != 1 or not ('A' <= s <= chr(ord('A') + COLS - 1)):
                print("Invalid input. Please enter a valid column letter:")
                continue
            col = ord(s) - ord('A')
            break

        row = drop(b, col, CHARS[turn])
        if row is None:
            turn = (turn + 1) % NUM_PLAYERS
            continue

        moves += 1
        if check_win(b, row, col, CHARS[turn]):
            os.system('clear')
            print_board(b)
            print(f"Player {CHARS[turn]} won!")
            break

        if moves == ROWS * COLS:
            os.system('clear')
            print_board(b)
            print("Game is a draw.")
            break

        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
