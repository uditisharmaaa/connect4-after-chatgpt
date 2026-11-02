import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_LEN = 4

def clear():
    os.system('clear')

def make_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear()
    letters = [string.ascii_uppercase[i] for i in range(len(board[0]))]
    print("  " + "   ".join(letters))
    border = "+" + "+".join(["---"] * len(board[0])) + "+"
    for r in range(len(board)):
        print(border)
        row_str = "|"
        for c in range(len(board[0])):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(border)

def drop_piece(board, col, token):
    for r in range(len(board)-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r
    return -1

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, token):
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            # right
            cnt = 0
            for k in range(WIN_LEN):
                if in_bounds(r, c+k, rows, cols) and board[r][c+k] == token:
                    cnt += 1
                else:
                    break
            if cnt == WIN_LEN:
                return True
            # down
            cnt = 0
            for k in range(WIN_LEN):
                if in_bounds(r+k, c, rows, cols) and board[r+k][c] == token:
                    cnt += 1
                else:
                    break
            if cnt == WIN_LEN:
                return True
            # down-right
            cnt = 0
            for k in range(WIN_LEN):
                if in_bounds(r+k, c+k, rows, cols) and board[r+k][c+k] == token:
                    cnt += 1
                else:
                    break
            if cnt == WIN_LEN:
                return True
            # down-left
            cnt = 0
            for k in range(WIN_LEN):
                if in_bounds(r+k, c-k, rows, cols) and board[r+k][c-k] == token:
                    cnt += 1
                else:
                    break
            if cnt == WIN_LEN:
                return True
    return False

def check_draw(board):
    for r in board:
        for v in r:
            if v == " ":
                return False
    return True

def get_col_input(cols):
    while True:
        s = input("Please enter a column: ").strip()
        if len(s) != 1:
            print("Invalid input.")
            continue
        ch = s.upper()
        if ch < 'A' or ord(ch) >= ord('A') + cols:
            print("Invalid input.")
            continue
        return ord(ch) - ord('A')

def main():
    board = make_board(ROWS, COLS)
    current = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    print(f"Player {TOKENS[current]}, you start.")
    while True:
        print_board(board)
        print(f"Player {TOKENS[current]}, please enter a column:")
        col = get_col_input(COLS)
        row_placed = drop_piece(board, col, TOKENS[current])
        print_board(board)
        if row_placed == -1:
            print("Column is full. Turn lost.")
            current = (current + 1) % NUM_PLAYERS
            continue
        if check_win(board, TOKENS[current]):
            print(f"Player {TOKENS[current]} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
