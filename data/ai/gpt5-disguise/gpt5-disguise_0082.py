import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear():
    os.system('clear')

def print_board(b):
    letters = list(string.ascii_uppercase[:len(b[0])])
    print("  " + "   ".join(letters))
    line = "+" + "---+" * len(b[0])
    for r in range(len(b)):
        print(line)
        row = ""
        for c in range(len(b[0])):
            row += f"| {b[r][c]} "
        row += "|"
        print(row)
    print(line)

def find_row(b, col):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            return r
    return None

def drop(b, col, token):
    r = find_row(b, col)
    if r is None:
        return False
    b[r][col] = token
    return True

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(b, token):
    rows = len(b)
    cols = len(b[0])
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(rows):
        for c in range(cols):
            if b[r][c] != token:
                continue
            for dr, dc in dirs:
                cnt = 0
                rr, cc = r, c
                while cnt < 4 and in_bounds(rr, cc, rows, cols) and b[rr][cc] == token:
                    cnt += 1
                    rr += dr
                    cc += dc
                if cnt == 4:
                    return True
    return False

def board_full(b):
    for r in b:
        for v in r:
            if v == " ":
                return False
    return True

def get_col_input(valid_cols):
    while True:
        s = input("Player {}, please enter a column: ".format(current_token)).strip()
        if len(s) != 1:
            print("Invalid input.")
            continue
        ch = s.upper()
        if ch not in valid_cols:
            print("Invalid input.")
            continue
        return valid_cols.index(ch)

board = make_board(ROWS, COLS)
letters = list(string.ascii_uppercase[:COLS])
start = random.randint(0, NUM_PLAYERS - 1)
turn = start

clear()
print_board(board)

while True:
    current_token = TOKENS[turn]
    col = get_col_input(letters)

    placed = drop(board, col, current_token)
    if not placed:
        print("Column is full. Turn lost.")
        # move to next player
        turn = (turn + 1) % NUM_PLAYERS
        if board_full(board):
            clear()
            print_board(board)
            print("It's a draw!")
            break
        clear()
        print_board(board)
        continue

    if check_win(board, current_token):
        clear()
        print_board(board)
        print("Player {} won!".format(current_token))
        break

    if board_full(board):
        clear()
        print_board(board)
        print("It's a draw!")
        break

    turn = (turn + 1) % NUM_PLAYERS
    clear()
    print_board(board)
