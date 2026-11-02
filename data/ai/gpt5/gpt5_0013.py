import os, random, sys

# Constants (submission requires 6x7 and 2 players)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # 2..5

SYMBOLS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear():
    os.system('clear')

def print_board(b):
    letters = [chr(ord('A') + i) for i in range(len(b[0]))]
    print("  " + "   ".join(letters))
    for r in range(len(b)):
        print("+" + "---+" * len(b[0]))
        print("|" + "|".join(f" {b[r][c]} " for c in range(len(b[0]))) + "|")
    print("+" + "---+" * len(b[0]))

def first_empty_row(b, col):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            return r
    return None

def in_bounds(r, c, R, C):
    return 0 <= r < R and 0 <= c < C

def won(b, r, c, sym):
    R, C = len(b), len(b[0])
    for dr, dc in [(0,1), (1,0), (1,1), (1,-1)]:
        cnt = 1
        for s in (1, -1):
            rr, cc = r + s*dr, c + s*dc
            while in_bounds(rr, cc, R, C) and b[rr][cc] == sym:
                cnt += 1
                rr += s*dr
                cc += s*dc
        if cnt >= 4:
            return True
    return False

def board_full(b):
    return all(cell != " " for row in b for cell in row)

def get_col_input(valid_cols):
    while True:
        s = input("Player {}, please enter a column: ".format(current_sym)).strip().upper()
        if len(s) == 1 and 'A' <= s <= chr(ord('A') + valid_cols - 1):
            return ord(s) - ord('A')
        # keep asking on invalid input

if __name__ == "__main__":
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5"); sys.exit(1)
    if not (1 <= COLS <= 26):
        print("COLS must be between 1 and 26"); sys.exit(1)

    board = make_board(ROWS, COLS)
    turn = random.randrange(NUM_PLAYERS)

    while True:
        clear()
        print_board(board)
        if board_full(board):
            print("It's a draw!")
            break
        current_sym = SYMBOLS[turn]
        col = get_col_input(COLS)
        row = first_empty_row(board, col)
        placed = False
        if row is not None:
            board[row][col] = current_sym
            placed = True
        # After the turn (even if invalid/skip), check for win/draw
        if placed and won(board, row, col, current_sym):
            clear()
            print_board(board)
            print(f"Player {current_sym} won!")
            break
        if placed and board_full(board):
            clear()
            print_board(board)
            print("It's a draw!")
            break
        turn = (turn + 1) % NUM_PLAYERS
