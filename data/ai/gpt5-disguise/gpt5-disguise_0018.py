import os
import random
import string

ROWS = 6
COLS = 7
PLAYERS = 2

TOKENS = ["X", "O", "V", "H", "M"]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(board):
    letters = [string.ascii_uppercase[i] for i in range(len(board[0]))]
    print("  " + "   ".join(letters))
    print("+" + "---+" * len(board[0]))
    for r in range(len(board)):
        row = "|"
        for c in range(len(board[0])):
            row += " " + board[r][c] + " |"
        print(row)
        print("+" + "---+" * len(board[0]))

def drop(board, col, token):
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r, col
    return None

def check_win(board, token):
    rlen = len(board)
    clen = len(board[0])
    for r in range(rlen):
        for c in range(clen):
            if board[r][c] != token:
                continue
            # right
            if c + 3 < clen and all(board[r][c + i] == token for i in range(4)):
                return True
            # down
            if r + 3 < rlen and all(board[r + i][c] == token for i in range(4)):
                return True
            # down-right
            if r + 3 < rlen and c + 3 < clen and all(board[r + i][c + i] == token for i in range(4)):
                return True
            # down-left
            if r + 3 < rlen and c - 3 >= 0 and all(board[r + i][c - i] == token for i in range(4)):
                return True
    return False

def is_draw(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def main():
    n = max(2, min(5, PLAYERS))
    board = make_board(ROWS, COLS)
    players = TOKENS[:n]
    turn = random.randint(0, n - 1)

    while True:
        os.system('clear')
        print_board(board)
        current = players[turn]
        col_letter = ""
        while True:
            col_letter = input(f"Player {current}, please enter a column: ").strip().upper()
            if len(col_letter) != 1:
                continue
            if col_letter < "A" or ord(col_letter) - ord("A") >= COLS:
                continue
            break

        col_idx = ord(col_letter) - ord("A")
        placed = drop(board, col_idx, current)
        if placed:
            if check_win(board, current):
                os.system('clear')
                print_board(board)
                print(f"Player {current} won!")
                break
            if is_draw(board):
                os.system('clear')
                print_board(board)
                print("It's a draw!")
                break
        turn = (turn + 1) % n

if __name__ == "__main__":
    main()
