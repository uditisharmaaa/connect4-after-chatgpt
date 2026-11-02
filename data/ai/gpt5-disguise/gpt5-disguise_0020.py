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

def print_board(board):
    c = len(board[0])
    letters = string.ascii_uppercase[:c]
    print("  " + "   ".join(list(letters)))
    print("+" + ("---+" * c))
    for r in range(len(board)):
        row = "|"
        for val in board[r]:
            row += " " + val + " |"
        print(row)
        print("+" + ("---+" * c))

def drop(board, col, token):
    for r in range(len(board)-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r
    return None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_line(board, r, c, dr, dc, token):
    count = 0
    rows = len(board)
    cols = len(board[0])
    for _ in range(4):
        if not in_bounds(r, c, rows, cols):
            return False
        if board[r][c] != token:
            return False
        r += dr
        c += dc
    return True

def check_win(board, token):
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            if check_line(board, r, c, 0, 1, token):
                return True
            if check_line(board, r, c, 1, 0, token):
                return True
            if check_line(board, r, c, 1, 1, token):
                return True
            if check_line(board, r, c, 1, -1, token):
                return True
    return False

def board_full(board):
    for r in board:
        for v in r:
            if v == " ":
                return False
    return True

def get_valid_input(valid_cols):
    while True:
        s = input().strip().upper()
        if len(s) != 1:
            print("Invalid input, try again:")
            continue
        if s not in valid_cols:
            print("Invalid input, try again:")
            continue
        return s

def main():
    cols_letters = list(string.ascii_uppercase[:min(COLS, 26)])
    players = TOKENS[:max(2, min(NUM_PLAYERS, 5))]
    board = make_board(ROWS, COLS)
    turn = random.randint(0, len(players)-1)

    clear()
    print_board(board)

    while True:
        p = players[turn]
        print(f"Player {p}, please enter a column:")
        col_letter = get_valid_input(cols_letters)
        col_index = cols_letters.index(col_letter)

        row_placed = drop(board, col_index, p)
        if row_placed is None:
            clear()
            print_board(board)
            print("Column full. Turn lost.")
            turn = (turn + 1) % len(players)
            continue

        clear()
        print_board(board)

        if check_win(board, p):
            print(f"Player {p} won!")
            break

        if board_full(board):
            print("It's a draw!")
            break

        turn = (turn + 1) % len(players)

if __name__ == "__main__":
    main()
