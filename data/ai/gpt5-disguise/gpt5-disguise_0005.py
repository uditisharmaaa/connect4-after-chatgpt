import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def make_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    letters = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(letters))
    line = "+" + ("---+" * len(board[0]))
    for r in range(len(board)):
        print(line)
        row_str = ""
        for c in range(len(board[0])):
            row_str += "|" + " " + board[r][c] + " "
        row_str += "|"
        print(row_str)
    print(line)

def drop(board, col, ch):
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = ch
            return r
    return None

def has_four(board, ch):
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols - 3):
            if board[r][c] == ch and board[r][c+1] == ch and board[r][c+2] == ch and board[r][c+3] == ch:
                return True
    for r in range(rows - 3):
        for c in range(cols):
            if board[r][c] == ch and board[r+1][c] == ch and board[r+2][c] == ch and board[r+3][c] == ch:
                return True
    for r in range(rows - 3):
        for c in range(cols - 3):
            if board[r][c] == ch and board[r+1][c+1] == ch and board[r+2][c+2] == ch and board[r+3][c+3] == ch:
                return True
    for r in range(3, rows):
        for c in range(cols - 3):
            if board[r][c] == ch and board[r-1][c+1] == ch and board[r-2][c+2] == ch and board[r-3][c+3] == ch:
                return True
    return False

def board_full(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def main():
    players = CHECKERS[:NUM_PLAYERS]
    board = make_board(ROWS, COLS)
    current = random.randint(0, NUM_PLAYERS - 1)

    while True:
        os.system('clear')
        print_board(board)
        ch = players[current]
        valid_cols = [chr(ord('A') + i) for i in range(COLS)]
        while True:
            s = input(f"Player {ch}, please enter a column: ").strip().upper()
            if len(s) == 1 and s in valid_cols:
                col = ord(s) - ord('A')
                break
            else:
                print("Invalid input. Try again.")
        row = drop(board, col, ch)
        if row is None:
            print(f"Column {s} is full. Turn lost.")
            input("Press Enter to continue...")
            current = (current + 1) % NUM_PLAYERS
            continue
        if has_four(board, ch):
            os.system('clear')
            print_board(board)
            print(f"Player {ch} won!")
            break
        if board_full(board):
            os.system('clear')
            print_board(board)
            print("It's a draw.")
            break
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
