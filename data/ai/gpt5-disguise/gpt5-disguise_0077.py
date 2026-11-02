import random
import os

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
SYMS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
WIN_LEN = 4

def make_board(r, c):
    return [[' ' for _ in range(c)] for _ in range(r)]

def print_board(b):
    letters = [chr(ord('A') + i) for i in range(len(b[0]))]
    print("  " + "   ".join(letters))
    print("+" + ("---+" * len(b[0])))
    for r in range(len(b)):
        row = "|"
        for c in range(len(b[0])):
            row += " " + b[r][c] + " |"
        print(row)
        print("+" + ("---+" * len(b[0])))

def drop_piece(b, col, sym):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == ' ':
            b[r][col] = sym
            return True
    return False

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(b, sym):
    rows = len(b)
    cols = len(b[0])
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(rows):
        for c in range(cols):
            if b[r][c] != sym:
                continue
            for dr, dc in dirs:
                cnt = 1
                nr, nc = r + dr, c + dc
                while cnt < WIN_LEN and in_bounds(nr, nc, rows, cols) and b[nr][nc] == sym:
                    cnt += 1
                    nr += dr
                    nc += dc
                if cnt == WIN_LEN:
                    return True
    return False

def board_full(b):
    for r in b:
        for v in r:
            if v == ' ':
                return False
    return True

def get_col_index(inp, max_cols):
    if len(inp) != 1:
        return None
    ch = inp.upper()
    if not ('A' <= ch <= 'Z'):
        return None
    idx = ord(ch) - ord('A')
    if 0 <= idx < max_cols:
        return idx
    return None

def main():
    random.seed()
    board = make_board(ROWS, COLS)
    start = random.randint(0, NUM_PLAYERS - 1)
    turn = start

    print_board(board)

    while True:
        sym = SYMS[turn]
        move_col = None
        while True:
            try:
                s = input(f"Player {sym}, please enter a column: ").strip()
            except EOFError:
                return
            except KeyboardInterrupt:
                return
            col = get_col_index(s, COLS)
            if col is None:
                continue
            move_col = col
            break

        placed = drop_piece(board, move_col, sym)
        if not placed:
            os.system('clear')
            print_board(board)
            print("Column is full. Turn lost.")
            turn = (turn + 1) % NUM_PLAYERS
            continue

        os.system('clear')
        print_board(board)

        if check_win(board, sym):
            print(f"Player {sym} won!")
            break

        if board_full(board):
            print("It's a draw!")
            break

        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
