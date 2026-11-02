import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def make_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    cols = len(board[0])
    labels = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(labels)
    print("+" + "---+" * cols)
    for r in range(len(board)):
        row = "|"
        for c in range(cols):
            row += " " + board[r][c] + " |"
        print(row)
        print("+" + "---+" * cols)

def drop_token(board, col, token):
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r
    return None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, r, c, token):
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    rows = len(board)
    cols = len(board[0])
    for dr, dc in dirs:
        count = 1
        rr, cc = r + dr, c + dc
        while in_bounds(rr, cc, rows, cols) and board[rr][cc] == token:
            count += 1
            rr += dr
            cc += dc
        rr, cc = r - dr, c - dc
        while in_bounds(rr, cc, rows, cols) and board[rr][cc] == token:
            count += 1
            rr -= dr
            cc -= dc
        if count >= WIN_COUNT:
            return True
    return False

def board_full(board):
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def valid_col_input(s, cols):
    if len(s) != 1:
        return False
    if s < "A" or s > chr(ord("A") + cols - 1):
        return False
    return True

def main():
    cols = COLS
    rows = ROWS
    players = TOKENS[:NUM_PLAYERS]
    board = make_board(rows, cols)
    current = random.randrange(len(players))
    print_board(board)

    while True:
        token = players[current]
        print(f"Player {token}, please enter a column:")
        col_input = input().strip().upper()
        while not valid_col_input(col_input, cols):
            print("Invalid input. Please enter a valid column letter:")
            col_input = input().strip().upper()
        c = ord(col_input) - ord("A")
        placed_row = drop_token(board, c, token)
        print_board(board)
        if placed_row is None:
            print("Column full. Turn lost.")
        else:
            if check_win(board, placed_row, c, token):
                print(f"Player {token} won!")
                break
            if board_full(board):
                print("It's a draw!")
                break
        current = (current + 1) % len(players)

if __name__ == "__main__":
    main()
