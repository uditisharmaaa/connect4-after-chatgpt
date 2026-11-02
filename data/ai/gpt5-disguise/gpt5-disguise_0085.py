import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def clear():
    os.system('clear')

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(b):
    letters = string.ascii_uppercase[:len(b[0])]
    print("  " + "   ".join(letters))
    sep = "+" + "+".join(["---"] * len(b[0])) + "+"
    for row in b:
        print(sep)
        line = "|" + "|".join(" {} ".format(x) for x in row) + "|"
        print(line)
    print(sep)

def get_col_input(max_col):
    while True:
        s = input().strip().upper()
        if len(s) == 1 and 'A' <= s <= chr(ord('A') + max_col - 1):
            return ord(s) - ord('A')
        print("Invalid input, try again:")

def drop_piece(b, col, ch):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = ch
            return r
    return -1

def count_dir(b, r, c, dr, dc, ch):
    cnt = 0
    i, j = r, c
    while 0 <= i < len(b) and 0 <= j < len(b[0]) and b[i][j] == ch:
        cnt += 1
        i += dr
        j += dc
    return cnt

def check_win(b, r, c, ch):
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in dirs:
        total = count_dir(b, r, c, dr, dc, ch) + count_dir(b, r, c, -dr, -dc, ch) - 1
        if total >= 4:
            return True
    return False

def is_draw(b):
    for row in b:
        if " " in row:
            return False
    return True

def main():
    board = make_board(ROWS, COLS)
    turn = random.randrange(NUM_PLAYERS)
    while True:
        clear()
        print_board(board)
        print("Player {}, please enter a column:".format(TOKENS[turn]))
        col = get_col_input(COLS)
        row = drop_piece(board, col, TOKENS[turn])
        if row == -1:
            print("Column is full! You lose your turn.")
        else:
            if check_win(board, row, col, TOKENS[turn]):
                clear()
                print_board(board)
                print("Player {} won!".format(TOKENS[turn]))
                break
            if is_draw(board):
                clear()
                print_board(board)
                print("It's a draw!")
                break
        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
