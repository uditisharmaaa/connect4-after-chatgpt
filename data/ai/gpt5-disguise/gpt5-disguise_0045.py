import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(b, letters):
    os.system('clear')
    print("  " + "   ".join(letters))
    print("+---" * len(letters) + "+")
    for row in b:
        line = "| " + " | ".join(row) + " |"
        print(line)
        print("+---" * len(letters) + "+")

def valid_input(s, letters):
    if len(s) != 1:
        return False
    if not s.isalpha():
        return False
    s = s.upper()
    return s in letters

def get_col(letters, token):
    while True:
        s = input(f"Player {token}, please enter a column: ").strip()
        if not valid_input(s, letters):
            print("Invalid input. Please enter a valid column letter.")
            continue
        return letters.index(s.upper())

def drop(b, col, token):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = token
            return True
    return False

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
                rr, cc = r + dr, c + dc
                while cnt < 4 and in_bounds(rr, cc, rows, cols) and b[rr][cc] == token:
                    cnt += 1
                    rr += dr
                    cc += dc
                if cnt == 4:
                    return True
    return False

def check_draw(b):
    for c in range(len(b[0])):
        if b[0][c] == " ":
            return False
    return True

def main():
    players = TOKENS[:NUM_PLAYERS]
    letters = list(string.ascii_uppercase[:COLS])
    board = make_board(ROWS, COLS)
    cur = random.randrange(len(players))

    print_board(board, letters)

    while True:
        token = players[cur]
        col = get_col(letters, token)
        if board[0][col] != " ":
            print("Column is full. Turn lost.")
            cur = (cur + 1) % len(players)
            print_board(board, letters)
            continue
        drop(board, col, token)
        print_board(board, letters)
        if check_win(board, token):
            print(f"Player {token} won!")
            break
        if check_draw(board):
            print("The game is a draw.")
            break
        cur = (cur + 1) % len(players)

if __name__ == "__main__":
    main()
