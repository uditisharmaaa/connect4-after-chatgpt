import os
import random
import string

# Constants (submission requires ROWS=6, COLS=7, N_PLAYERS=2)
ROWS = 6
COLS = 7
N_PLAYERS = 2
WIN_LEN = 4
SYMBOLS = ["X", "O", "V", "H", "M"]

assert 2 <= N_PLAYERS <= 5
assert 1 <= COLS <= 26

def clear():
    os.system('clear')

def make_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear()
    cols = len(board[0])
    letters = list(string.ascii_uppercase[:cols])
    print("  " + "   ".join(letters))
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(len(board)):
        print(sep)
        row = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row)
    print(sep)

def drop_piece(board, col, sym):
    for r in range(len(board)-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = sym
            return r, col
    return None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, r0, c0, sym):
    if r0 is None: 
        return False
    rows, cols = len(board), len(board[0])
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        count = 1
        for s in (1, -1):
            r, c = r0 + s*dr, c0 + s*dc
            while in_bounds(r, c, rows, cols) and board[r][c] == sym:
                count += 1
                if count >= WIN_LEN:
                    return True
                r += s*dr
                c += s*dc
    return False

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def read_valid_column(prompt, cols):
    while True:
        try:
            s = input(prompt).strip().upper()
        except EOFError:
            s = ""
        if len(s) == 1 and 'A' <= s <= chr(ord('A') + cols - 1):
            return ord(s) - ord('A')

def main():
    board = make_board(ROWS, COLS)
    players = SYMBOLS[:N_PLAYERS]
    current = random.randrange(N_PLAYERS)
    while True:
        print_board(board)
        sym = players[current]
        col = read_valid_column(f"Player {sym}, please enter a column: ", COLS)
        pos = drop_piece(board, col, sym)
        if pos is None:
            # Column full, turn lost
            current = (current + 1) % N_PLAYERS
            continue
        r, c = pos
        if check_win(board, r, c, sym):
            print_board(board)
            print(f"Player {sym} won!")
            break
        if board_full(board):
            print_board(board)
            print("It's a draw!")
            break
        current = (current + 1) % N_PLAYERS

if __name__ == "__main__":
    main()
