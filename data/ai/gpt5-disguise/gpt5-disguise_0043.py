import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2

PIECES = ["X", "O", "V", "H", "M"]
PLAYERS = PIECES[:NUM_PLAYERS]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear():
    os.system('clear')

def col_letter(i):
    return chr(ord('A') + i)

def print_board(b):
    clear()
    header = "  " + "   ".join(col_letter(i) for i in range(COLS))
    print(header)
    line = "+" + "+".join(["---"] * COLS) + "+"
    for r in range(ROWS):
        print(line)
        row = "|" + "|".join(f" {b[r][c]} " for c in range(COLS)) + "|"
        print(row)
    print(line)

def get_col_input():
    valid = [col_letter(i) for i in range(COLS)]
    while True:
        s = input("Please enter a column: ").strip().upper()
        if len(s) == 1 and s in valid:
            return valid.index(s)
        else:
            print("Invalid input. Use a letter between A and " + valid[-1] + ".")

def place(b, col, piece):
    for r in range(ROWS - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = piece
            return (r, col)
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(b, piece):
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(ROWS):
        for c in range(COLS):
            if b[r][c] != piece:
                continue
            for dr, dc in dirs:
                count = 1
                rr, cc = r + dr, c + dc
                while count < 4 and in_bounds(rr, cc) and b[rr][cc] == piece:
                    count += 1
                    rr += dr
                    cc += dc
                if count == 4:
                    return True
    return False

def board_full(b):
    for r in range(ROWS):
        for c in range(COLS):
            if b[r][c] == " ":
                return False
    return True

def main():
    random.seed()
    board = make_board(ROWS, COLS)
    current = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    while True:
        p = PLAYERS[current]
        print(f"Player {p}, please enter a column:")
        col = get_col_input()
        pos = place(board, col, p)
        if pos is None:
            print(f"Column {col_letter(col)} is full. Turn lost.")
        else:
            if check_win(board, p):
                print_board(board)
                print(f"Player {p} won!")
                break
        if board_full(board):
            print_board(board)
            print("It's a draw!")
            break
        current = (current + 1) % NUM_PLAYERS
        print_board(board)

if __name__ == "__main__":
    main()
