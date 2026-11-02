import os, random, string, sys

# Constants (submission requires 6x7 and 2 players)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # 2..5
SYMBOLS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def clear():
    os.system('clear')

def create_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(board):
    clear()
    cols = len(board[0])
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    print(header)
    sep = "+" + ("---+" * cols)
    for row in board:
        print(sep)
        print("|" + "|".join(f" {cell} " for cell in row) + "|")
    print(sep)

def drop_piece(board, col_idx, sym):
    # Place at lowest available row in column; return True if placed
    for r in range(len(board)-1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = sym
            return True
    return False

def in_bounds(r, c, R, C):
    return 0 <= r < R and 0 <= c < C

def check_win(board, sym):
    R, C = len(board), len(board[0])
    dirs = [(0,1),(1,0),(1,1),(-1,1)]
    for r in range(R):
        for c in range(C):
            if board[r][c] != sym:
                continue
            for dr, dc in dirs:
                cnt = 0
                rr, cc = r, c
                while cnt < 4 and in_bounds(rr, cc, R, C) and board[rr][cc] == sym:
                    cnt += 1
                    rr += dr; cc += dc
                if cnt == 4:
                    return True
    return False

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def get_col_input(valid_cols, player_sym):
    while True:
        try:
            s = input(f"Player {player_sym}, please enter a column: ").strip().upper()
        except EOFError:
            sys.exit(0)
        if len(s) == 1 and s in valid_cols:
            return valid_cols.index(s)
        # invalid input; ask again

def main():
    board = create_board(ROWS, COLS)
    letters = list(string.ascii_uppercase[:COLS])
    current = random.randrange(NUM_PLAYERS)
    print_board(board)
    while True:
        sym = SYMBOLS[current]
        col = get_col_input(letters, sym)
        placed = drop_piece(board, col, sym)
        print_board(board)
        if placed:
            if check_win(board, sym):
                print(f"Player {sym} won!")
                break
            if board_full(board):
                print("It's a draw!")
                break
        # if not placed (column full), turn is lost
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
