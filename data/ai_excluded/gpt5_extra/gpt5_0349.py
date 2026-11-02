import os, random, string, sys

# Constants (submission must be 6x7 with 2 players)
ROWS, COLS = 6, 7
NUM_PLAYERS = 2  # between 2 and 5
TOKENS = "XOVHM"[:NUM_PLAYERS]
WINLEN = 4

def clear():
    os.system('clear')

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(board):
    r, c = len(board), len(board[0])
    letters = [chr(65+i) for i in range(c)]
    print("  " + "   ".join(letters))
    sep = "+" + "+".join(["---"]*c) + "+"
    for row in board:
        print(sep)
        print("|" + "|".join(f" {ch} " for ch in row) + "|")
    print(sep)

def valid_col(ch):
    if len(ch) != 1 or ch not in string.ascii_uppercase:
        return None
    idx = ord(ch) - 65
    return idx if 0 <= idx < COLS else None

def drop_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(board, token):
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != token: continue
            for dr, dc in dirs:
                cnt = 1
                nr, nc = r, c
                for _ in range(WINLEN-1):
                    nr += dr; nc += dc
                    if in_bounds(nr, nc) and board[nr][nc] == token:
                        cnt += 1
                    else:
                        break
                if cnt == WINLEN:
                    return True
    return False

def is_draw(board):
    return all(board[r][c] != " " for r in range(ROWS) for c in range(COLS))

def main():
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5 or COLS > 26:
        print("Invalid configuration."); sys.exit(1)
    board = make_board(ROWS, COLS)
    turn = random.randrange(NUM_PLAYERS)
    while True:
        clear()
        print_board(board)
        token = TOKENS[turn]
        # Input loop for valid column letter
        col = None
        while col is None:
            inp = input(f"Player {token}, please enter a column: ").strip().upper()
            col = valid_col(inp)
            if col is None:
                print("Invalid input. Use a column letter shown above.")
        row = drop_row(board, col)
        if row is None:
            print("Column is full! Turn lost. Press Enter to continue.")
            input()
        else:
            board[row][col] = token
            if check_win(board, token):
                clear(); print_board(board)
                print(f"Player {token} won!")
                break
            if is_draw(board):
                clear(); print_board(board)
                print("It's a draw!")
                break
        turn = (turn + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
