import os
import random
import sys

# Constants (submission: 6 rows x 7 columns and 2 players)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
CONNECT = 4

def clear():
    os.system('clear')

def make_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    letters = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(letters))
    horiz = "+" + "+".join(["---"] * len(board[0])) + "+"
    for r in range(len(board)):
        print(horiz)
        print("|" + "|".join(f" {board[r][c]} " for c in range(len(board[0]))) + "|")
    print(horiz)

def valid_col(ch):
    if len(ch) != 1 or not ch.isalpha():
        return False
    idx = ord(ch.upper()) - ord('A')
    return 0 <= idx < COLS

def drop_checker(board, col, sym):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = sym
            return r
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(board, sym):
    dirs = [(0,1), (1,0), (1,1), (1,-1)]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != sym:
                continue
            for dr, dc in dirs:
                cnt = 1
                rr, cc = r + dr, c + dc
                while cnt < CONNECT and in_bounds(rr, cc) and board[rr][cc] == sym:
                    cnt += 1
                    rr += dr
                    cc += dc
                if cnt == CONNECT:
                    return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    if COLS > 26 or NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Invalid configuration.", file=sys.stderr)
        return
    board = make_board(ROWS, COLS)
    current = random.randrange(NUM_PLAYERS)
    while True:
        clear()
        print_board(board)
        if is_draw(board):
            print("It's a draw!")
            break
        sym = CHECKERS[current]
        while True:
            col_input = input(f"Player {sym}, please enter a column: ").strip()
            if not valid_col(col_input):
                print("Invalid input. Enter a letter within the board (e.g., A-G).")
                continue
            col = ord(col_input.upper()) - ord('A')
            row = drop_checker(board, col, sym)
            if row is None:
                print(f"Column {chr(ord('A')+col)} is full. Turn lost.")
            else:
                if check_win(board, sym):
                    clear()
                    print_board(board)
                    print(f"Player {sym} won!")
                    return
            # advance turn after a valid column entry (placed or full)
            current = (current + 1) % NUM_PLAYERS
            break

if __name__ == "__main__":
    main()
