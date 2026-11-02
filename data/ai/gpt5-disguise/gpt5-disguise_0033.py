import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]

def make_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(b):
    letters = [chr(ord('A') + i) for i in range(len(b[0]))]
    print("  " + "   ".join(letters))
    line = "+" + "+".join(["---"] * len(b[0])) + "+"
    for r in range(len(b)):
        print(line)
        row_str = "|"
        for c in range(len(b[0])):
            row_str += " " + b[r][c] + " |"
        print(row_str)
    print(line)

def clear():
    os.system('clear')

def get_col_index(s, cols):
    if len(s) != 1:
        return None
    if not s.isalpha():
        return None
    s = s.upper()
    idx = ord(s) - ord('A')
    if 0 <= idx < cols:
        return idx
    return None

def place_token(b, col, token):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = token
            return r, col
    return None

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
                cnt = 1
                rr, cc = r, c
                for _ in range(3):
                    rr += dr
                    cc += dc
                    if in_bounds(rr, cc, rows, cols) and b[rr][cc] == token:
                        cnt += 1
                    else:
                        break
                if cnt == 4:
                    return True
    return False

def board_full(b):
    for r in b:
        for v in r:
            if v == " ":
                return False
    return True

def main():
    cols = min(COLS, 26)
    rows = ROWS
    players = max(2, min(NUM_PLAYERS, 5))
    tokens = TOKENS[:players]
    b = make_board(rows, cols)
    turn = random.randrange(players)

    clear()
    print_board(b)

    while True:
        t = tokens[turn]
        print(f"Player {t}, please enter a column:")
        move = input().strip().upper()
        col = get_col_index(move, cols)
        while col is None:
            print("Invalid input. Please enter a valid column letter.")
            move = input().strip().upper()
            col = get_col_index(move, cols)

        placed = place_token(b, col, t)
        if placed is None:
            print("Column is full. Turn lost.")
            turn = (turn + 1) % players
            if board_full(b):
                clear()
                print_board(b)
                print("It's a draw!")
                break
            clear()
            print_board(b)
            continue

        r, c = placed
        clear()
        print_board(b)

        if check_win(b, t):
            print(f"Player {t} won!")
            break

        if board_full(b):
            print("It's a draw!")
            break

        turn = (turn + 1) % players

if __name__ == "__main__":
    main()
