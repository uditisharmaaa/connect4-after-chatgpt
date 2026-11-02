import os
import random
import string

# Constants (changeable; for submission keep as below)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_N = 4

def clear():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    letters = string.ascii_uppercase[:cols]
    header = "  " + "   ".join(letters)
    sep = "+" + "+".join(["---"] * cols) + "+"
    print(header)
    for r in range(len(board)):
        print(sep)
        row = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row)
    print(sep)

def input_column(valid_max_col):
    while True:
        col = input().strip().upper()
        if len(col) == 1 and 'A' <= col <= chr(ord('A') + valid_max_col - 1):
            return ord(col) - ord('A')
        print("Invalid input. Please enter a valid column letter:")

def lowest_empty_row(board, col):
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def check_win(board, sym):
    rows, cols = len(board), len(board[0])
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != sym:
                continue
            for dr, dc in dirs:
                cnt = 1
                rr, cc = r + dr, c + dc
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == sym and cnt < WIN_N:
                    cnt += 1
                    rr += dr
                    cc += dc
                if cnt >= WIN_N:
                    return True
    return False

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def main():
    if COLS > 26:
        raise ValueError("Max 26 columns supported.")
    board = create_board(ROWS, COLS)
    current = random.randrange(NUM_PLAYERS)
    while True:
        clear()
        print_board(board)
        print(f"Player {CHECKERS[current]}, please enter a column:")
        col = input_column(COLS)
        row = lowest_empty_row(board, col)
        if row is None:
            # Column full, lose turn
            current = (current + 1) % NUM_PLAYERS
            continue
        board[row][col] = CHECKERS[current]
        if check_win(board, CHECKERS[current]):
            clear()
            print_board(board)
            print(f"Player {CHECKERS[current]} won!")
            break
        if board_full(board):
            clear()
            print_board(board)
            print("It's a draw!")
            break
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
