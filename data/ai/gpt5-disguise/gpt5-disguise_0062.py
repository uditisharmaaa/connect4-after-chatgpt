import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
SYMS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(b):
    os.system('clear')
    letters = [chr(ord('A') + i) for i in range(len(b[0]))]
    print("  " + "   ".join(letters))
    sep = "+" + "+".join(["---"] * len(b[0])) + "+"
    for row in b:
        print(sep)
        print("|" + "|".join(" " + cell + " " for cell in row) + "|")
    print(sep)

def drop_piece(b, col, sym):
    for r in range(len(b)-1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = sym
            return r
    return None

def in_bounds(r, c, R, C):
    return 0 <= r < R and 0 <= c < C

def check_win(b, sym):
    R = len(b)
    C = len(b[0])
    dirs = [(0,1),(1,0),(1,1),(-1,1)]
    for r in range(R):
        for c in range(C):
            if b[r][c] != sym:
                continue
            for dr, dc in dirs:
                count = 1
                rr, cc = r + dr, c + dc
                while in_bounds(rr, cc, R, C) and b[rr][cc] == sym:
                    count += 1
                    if count == 4:
                        return True
                    rr += dr
                    cc += dc
    return False

def board_full(b):
    for row in b:
        for cell in row:
            if cell == " ":
                return False
    return True

def main():
    board = make_board(ROWS, COLS)
    turn = random.randint(0, NUM_PLAYERS - 1)
    moves = 0
    print_board(board)
    while True:
        sym = SYMS[turn]
        last_col_letter = chr(ord('A') + COLS - 1)
        while True:
            print(f"Player {sym}, please enter a column:")
            x = input().strip().upper()
            if len(x) != 1 or not ('A' <= x <= last_col_letter):
                print_board(board)
                print("Invalid input. Please enter a letter between A and " + last_col_letter + ".")
                continue
            col = ord(x) - ord('A')
            break
        row_idx = drop_piece(board, col, sym)
        if row_idx is None:
            print_board(board)
            print("Column is full. You lose this turn.")
            turn = (turn + 1) % NUM_PLAYERS
            continue
        moves += 1
        print_board(board)
        if check_win(board, sym):
            print(f"Player {sym} won!")
            break
        if moves == ROWS * COLS:
            print("It's a draw!")
            break
        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
