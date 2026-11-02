import os, random, sys

# Constants (submission requires 6x7 and 2 players)
ROWS, COLS = 6, 7
N_PLAYERS = 2  # between 2 and 5
WIN_LEN = 4
CHECKERS = "XOVHM"[:N_PLAYERS]
LABELS = [chr(ord('A') + i) for i in range(COLS)]

def clear():
    os.system('clear')

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(board):
    clear()
    print("  " + "   ".join(LABELS))
    print("+" + "---+" * COLS)
    for r in range(ROWS):
        print("|" + "|".join(f" {board[r][c]} " for c in range(COLS)) + "|")
        print("+" + "---+" * COLS)

def get_col_input(player):
    while True:
        s = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(s) == 1 and 'A' <= s <= chr(ord('A') + COLS - 1):
            return ord(s) - ord('A')
        # invalid input -> reprompt

def place_checker(board, col, ch):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = ch
            return r, col
    return None  # column full

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(board, ch):
    dirs = [(1,0),(0,1),(1,1),(1,-1)]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != ch: continue
            for dr, dc in dirs:
                cnt = 0
                rr, cc = r, c
                while in_bounds(rr, cc) and board[rr][cc] == ch:
                    cnt += 1
                    if cnt == WIN_LEN: return True
                    rr += dr; cc += dc
    return False

def is_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    random.seed()
    board = make_board(ROWS, COLS)
    current = random.randrange(N_PLAYERS)
    print_board(board)
    while True:
        ch = CHECKERS[current]
        col = get_col_input(ch)
        placed = place_checker(board, col, ch)
        if not placed:
            # Column full: turn is lost
            current = (current + 1) % N_PLAYERS
            print_board(board)
            continue
        if check_win(board, ch):
            print_board(board)
            print(f"Player {ch} won!")
            break
        if is_draw(board):
            print_board(board)
            print("Game is a draw.")
            break
        current = (current + 1) % N_PLAYERS
        print_board(board)

if __name__ == "__main__":
    if COLS > 26 or N_PLAYERS < 2 or N_PLAYERS > 5:
        print("Invalid configuration.", file=sys.stderr); sys.exit(1)
    main()
