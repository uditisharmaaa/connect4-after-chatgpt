import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear():
    os.system('clear')

def print_board(b):
    clear()
    cols = len(b[0])
    letters = string.ascii_uppercase[:cols]
    header = "  " + "   ".join(list(letters))
    print(header)
    print("+" + "---+" * cols)
    for r in range(len(b)):
        row_str = "|"
        for c in range(cols):
            row_str += " " + b[r][c] + " |"
        print(row_str)
        print("+" + "---+" * cols)

def get_input(valid_letters, token):
    while True:
        print(f"Player {token}, please enter a column:")
        s = input().strip().upper()
        if len(s) != 1:
            continue
        if s not in valid_letters:
            continue
        return s

def place_token(b, col, token):
    for r in range(len(b)-1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = token
            return r, col
    return None

def in_bounds(r, c, R, C):
    return 0 <= r < R and 0 <= c < C

def check_win(b, token):
    R = len(b)
    C = len(b[0])
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(R):
        for c in range(C):
            if b[r][c] != token:
                continue
            for dr, dc in dirs:
                count = 1
                rr = r + dr
                cc = c + dc
                while in_bounds(rr, cc, R, C) and b[rr][cc] == token:
                    count += 1
                    if count == 4:
                        return True
                    rr += dr
                    cc += dc
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
    players = TOKENS[:NUM_PLAYERS]
    board = make_board(ROWS, COLS)
    turn = random.randrange(len(players))
    print_board(board)

    letters = list(string.ascii_uppercase[:COLS])

    while True:
        token = players[turn]
        col_letter = get_input(letters, token)
        col_idx = letters.index(col_letter)

        spot = place_token(board, col_idx, token)
        if spot is None:
            print_board(board)
            print(f"Column {col_letter} is full. Player {token} loses the turn.")
            turn = (turn + 1) % len(players)
            continue

        print_board(board)

        if check_win(board, token):
            print(f"Player {token} won!")
            break

        if board_full(board):
            print("It's a draw!")
            break

        turn = (turn + 1) % len(players)

if __name__ == "__main__":
    main()
