import os
import random
import string

ROWS = 6
COLS = 7
N_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(b):
    os.system('clear')
    letters = string.ascii_uppercase[:len(b[0])]
    header = "  " + "   ".join(list(letters))
    print(header)
    sep = "+" + "+".join(["---"] * len(b[0])) + "+"
    for r in range(len(b)):
        print(sep)
        row = "|"
        for c in range(len(b[0])):
            row += " " + b[r][c] + " |"
        print(row)
    print(sep)

def in_bounds_col(ch, c):
    if len(ch) != 1:
        return False
    if ch not in string.ascii_uppercase:
        return False
    idx = ord(ch) - ord('A')
    return 0 <= idx < c

def drop(b, col, t):
    for r in range(len(b)-1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = t
            return (r, col)
    return None

def check_line(b, r, c, dr, dc, t):
    for k in range(4):
        rr = r + dr*k
        cc = c + dc*k
        if rr < 0 or rr >= len(b) or cc < 0 or cc >= len(b[0]):
            return False
        if b[rr][cc] != t:
            return False
    return True

def check_win(b, t):
    for r in range(len(b)):
        for c in range(len(b[0])):
            if b[r][c] == t:
                if check_line(b, r, c, 0, 1, t):  # right
                    return True
                if check_line(b, r, c, 1, 0, t):  # down
                    return True
                if check_line(b, r, c, 1, 1, t):  # down-right
                    return True
                if check_line(b, r, c, 1, -1, t): # down-left
                    return True
    return False

def check_draw(b):
    for r in b:
        for v in r:
            if v == " ":
                return False
    return True

def main():
    players = TOKENS[:max(2, min(5, N_PLAYERS))]
    board = make_board(ROWS, COLS)
    start = random.randrange(len(players))
    turn = start
    print_board(board)
    while True:
        cur = players[turn]
        print(f"Player {cur}, please enter a column:")
        col_input = input().strip().upper()
        while not in_bounds_col(col_input, COLS):
            print("Invalid input, try again (use letters A-" + chr(ord('A') + COLS - 1) + "):")
            col_input = input().strip().upper()
        col_idx = ord(col_input) - ord('A')
        pos = drop(board, col_idx, cur)
        print_board(board)
        if pos is None:
            print("Column full. Turn lost.")
        else:
            if check_win(board, cur):
                print(f"Player {cur} won!")
                break
            if check_draw(board):
                print("It's a draw!")
                break
        turn = (turn + 1) % len(players)

if __name__ == "__main__":
    main()
