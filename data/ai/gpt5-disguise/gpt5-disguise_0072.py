import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
SYMS = ["X", "O", "V", "H", "M"]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear():
    os.system('clear')

def print_board(board):
    cols = len(board[0])
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(header)
    print("+" + "---+" * cols)
    for r in range(len(board)):
        row = "|"
        for c in range(cols):
            row += " " + board[r][c] + " |"
        print(row)
        print("+" + "---+" * cols)

def valid_col_input(s, max_col):
    if len(s) != 1:
        return False
    if not s.isalpha():
        return False
    s = s.upper()
    if ord(s) < ord('A') or ord(s) >= ord('A') + max_col:
        return False
    return True

def drop_checker(board, col, sym):
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = sym
            return r
    return None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, sym):
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != sym:
                continue
            # right
            if c + 3 < cols and all(board[r][c+i] == sym for i in range(4)):
                return True
            # down
            if r + 3 < rows and all(board[r+i][c] == sym for i in range(4)):
                return True
            # down-right
            if r + 3 < rows and c + 3 < cols and all(board[r+i][c+i] == sym for i in range(4)):
                return True
            # down-left
            if r + 3 < rows and c - 3 >= 0 and all(board[r+i][c-i] == sym for i in range(4)):
                return True
    return False

def board_full(board):
    for r in board:
        for v in r:
            if v == " ":
                return False
    return True

def main():
    board = make_board(ROWS, COLS)
    players = SYMS[:PLAYERS]
    turn = random.randint(0, PLAYERS - 1)

    clear()
    print_board(board)

    while True:
        sym = players[turn]
        print(f"Player {sym}, please enter a column:")
        col_in = input().strip().upper()
        while not valid_col_input(col_in, COLS):
            print(f"Player {sym}, please enter a column:")
            col_in = input().strip().upper()

        col = ord(col_in) - ord('A')
        placed_row = drop_checker(board, col, sym)

        clear()
        print_board(board)

        if placed_row is None:
            turn = (turn + 1) % PLAYERS
        else:
            if check_win(board, sym):
                print(f"Player {sym} won!")
                break
            if board_full(board):
                print("It's a draw!")
                break
            turn = (turn + 1) % PLAYERS

if __name__ == "__main__":
    main()
