import os, random, string

# Config (submission requires ROWS=6, COLS=7, NUM_PLAYERS=2)
ROWS, COLS = 6, 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
letters = string.ascii_uppercase[:COLS]

def clear():
    os.system('clear')

def print_board():
    clear()
    print("  " + "   ".join(letters))
    print("+---" * COLS + "+")
    for r in range(ROWS):
        print("| " + " | ".join(board[r]) + " |")
        print("+---" * COLS + "+")

def drop(col, token):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r, col
    return None

def won(token):
    dirs = [(0,1),(1,0),(1,1),(-1,1)]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != token: continue
            for dr, dc in dirs:
                cnt = 0
                rr, cc = r, c
                while 0 <= rr < ROWS and 0 <= cc < COLS and board[rr][cc] == token:
                    cnt += 1
                    if cnt == 4: return True
                    rr += dr; cc += dc
    return False

def full():
    for r in board:
        for v in r:
            if v == " ": return False
    return True

cur = random.randrange(NUM_PLAYERS)
print_board()
while True:
    token = TOKENS[cur]
    # input validation (must be a single letter within board)
    while True:
        s = input(f"Player {token}, please enter a column: ").strip().upper()
        if len(s) == 1 and s in letters:
            col = letters.index(s)
            break
    res = drop(col, token)
    if res is None:
        # column full, lose the turn
        cur = (cur + 1) % NUM_PLAYERS
        print_board()
        continue
    print_board()
    if won(token):
        print(f"Player {token} won!")
        break
    if full():
        print("The game is a draw.")
        break
    cur = (cur + 1) % NUM_PLAYERS
