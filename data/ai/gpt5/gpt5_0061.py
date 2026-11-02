import os
import random
import sys

# Config
ROWS = 6
COLS = 7  # max 26
PLAYERS = 2  # between 2 and 5
TOKENS = ["X", "O", "V", "H", "M"][:PLAYERS]

assert 2 <= PLAYERS <= 5
assert 1 <= COLS <= 26

def clear():
    os.system('clear')

def new_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(letters))
    print("+" + "---+" * cols)
    for r in range(len(board)):
        print("|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|")
        print("+" + "---+" * cols)

def drop_token(board, col, token):
    # returns row index placed, or None if column full
    if board[0][col] != " ":
        return None
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, r, c, token):
    # count consecutive tokens in a direction
    def count_dir(dr, dc):
        cnt = 0
        rr, cc = r + dr, c + dc
        while in_bounds(rr, cc, len(board), len(board[0])) and board[rr][cc] == token:
            cnt += 1
            rr += dr
            cc += dc
        return cnt
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        total = 1 + count_dir(dr, dc) + count_dir(-dr, -dc)
        if total >= 4:
            return True
    return False

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def get_valid_column_input(cols):
    while True:
        s = input().strip().upper()
        if len(s) == 1 and 'A' <= s <= chr(ord('A') + cols - 1):
            return ord(s) - ord('A')
        print("Invalid input. Please enter a valid column letter:")

def main():
    board = new_board(ROWS, COLS)
    current = random.randrange(PLAYERS)
    while True:
        clear()
        print_board(board)
        print(f"Player {TOKENS[current]}, please enter a column:")
        col = get_valid_column_input(COLS)
        row = drop_token(board, col, TOKENS[current])
        if row is None:
            print("Column is full. Turn lost. Press Enter to continue.")
            input()
            current = (current + 1) % PLAYERS
            continue
        if check_win(board, row, col, TOKENS[current]):
            clear()
            print_board(board)
            print(f"Player {TOKENS[current]} won!")
            break
        if board_full(board):
            clear()
            print_board(board)
            print("It's a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
