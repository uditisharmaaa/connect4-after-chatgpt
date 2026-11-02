import os, random, string, sys

# Config (submission must use 6 rows x 7 cols and 2 players)
ROWS, COLS = 6, 7
PLAYERS = 2  # supports 2..5
TOKENS = list("XOVHM")[:PLAYERS]
WIN_LEN = 4

def clear():
    os.system('clear')

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(b):
    letters = [string.ascii_uppercase[i] for i in range(len(b[0]))]
    print("  " + "   ".join(letters))
    sep = "+" + "+".join(["---"] * len(b[0])) + "+"
    for r in range(len(b)):
        print(sep)
        print("|" + "|".join(f" {b[r][c]} " for c in range(len(b[0]))) + "|")
    print(sep)

def col_from_input(s, maxc):
    s = s.strip().upper()
    if len(s) != 1 or s < "A" or ord(s) - ord("A") >= maxc:
        return None
    return ord(s) - ord("A")

def drop(b, col, token):
    for r in range(len(b) - 1, -1, -1):
        if b[r][col] == " ":
            b[r][col] = token
            return r
    return None  # full

def in_bounds(r, c, R, C):
    return 0 <= r < R and 0 <= c < C

def win(b, token):
    R, C = len(b), len(b[0])
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(R):
        for c in range(C):
            if b[r][c] != token: continue
            for dr, dc in dirs:
                ok = True
                for k in range(1, WIN_LEN):
                    nr, nc = r + dr*k, c + dc*k
                    if not in_bounds(nr, nc, R, C) or b[nr][nc] != token:
                        ok = False
                        break
                if ok:
                    return True
    return False

def draw(b):
    return all(cell != " " for row in b for cell in row)

def main():
    if not (2 <= PLAYERS <= 5) or not (1 <= COLS <= 26):
        print("Invalid configuration."); sys.exit(1)
    board = make_board(ROWS, COLS)
    player = random.randrange(PLAYERS)

    while True:
        clear()
        print_board(board)
        cur = TOKENS[player]
        # prompt and validate input (invalid input does not lose turn)
        col = None
        while col is None:
            try:
                col = col_from_input(input(f"Player {cur}, please enter a column: "), COLS)
            except EOFError:
                print(); return
        # attempt to drop (full column loses turn)
        row = drop(board, col, cur)
        if row is not None:
            if win(board, cur):
                clear(); print_board(board); print(f"Player {cur} won!")
                return
            if draw(board):
                clear(); print_board(board); print("It's a draw!")
                return
        # next player's turn (even if lost by full column)
        player = (player + 1) % PLAYERS

if __name__ == "__main__":
    main()
