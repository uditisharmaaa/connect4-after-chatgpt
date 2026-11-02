import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2

symbols = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def make_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    letters = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(letters))
    print("+" + "---+" * len(board[0]))
    for r in range(len(board)):
        row = "|"
        for c in range(len(board[0])):
            row += " " + board[r][c] + " |"
        print(row)
        print("+" + "---+" * len(board[0]))

def clear():
    os.system('clear')

def is_full(board):
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def place(board, col, sym):
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = sym
            return r, col
    return None

def valid_col_input(s, max_cols):
    if len(s) != 1:
        return False
    if not s.isalpha():
        return False
    ch = s.upper()
    if ord(ch) < ord('A') or ord(ch) >= ord('A') + max_cols:
        return False
    return True

def check_win(board, sym):
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != sym:
                continue
            # right
            if c + 3 < cols and all(board[r][c + k] == sym for k in range(4)):
                return True
            # down
            if r + 3 < rows and all(board[r + k][c] == sym for k in range(4)):
                return True
            # down-right
            if r + 3 < rows and c + 3 < cols and all(board[r + k][c + k] == sym for k in range(4)):
                return True
            # up-right
            if r - 3 >= 0 and c + 3 < cols and all(board[r - k][c + k] == sym for k in range(4)):
                return True
    return False

def main():
    board = make_board(ROWS, COLS)
    turn = random.randint(0, NUM_PLAYERS - 1)
    clear()
    print_board(board)
    while True:
        if is_full(board):
            print("It's a draw!")
            break
        sym = symbols[turn]
        valid_entered = False
        col = None
        while not valid_entered:
            inp = input(f"Player {sym}, please enter a column: ").strip().upper()
            if valid_col_input(inp, COLS):
                col = ord(inp) - ord('A')
                valid_entered = True
            else:
                print("Invalid input. Please enter a valid column letter.")
        if board[0][col] != " ":
            clear()
            print_board(board)
            print("Column is full. Turn lost.")
            turn = (turn + 1) % NUM_PLAYERS
            continue
        pos = place(board, col, sym)
        clear()
        print_board(board)
        if check_win(board, sym):
            print(f"Player {sym} won!")
            break
        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
