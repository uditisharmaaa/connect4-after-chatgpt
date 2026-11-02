import os
import random

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN = 4
TOKENS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

board = [[" " for _ in range(COLS)] for _ in range(ROWS)]

def clear():
    os.system('clear')

def show():
    clear()
    labels = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(labels))
    sep = "+" + ("---+" * COLS)
    for r in range(ROWS):
        print(sep)
        line = ""
        for c in range(COLS):
            line += "| " + board[r][c] + " "
        line += "|"
        print(line)
    print(sep)

def place(col, token):
    if board[0][col] != " ":
        return False
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return True
    return False

def win(token):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != token:
                continue
            # right
            if c + WIN - 1 < COLS and all(board[r][c + k] == token for k in range(WIN)):
                return True
            # down
            if r + WIN - 1 < ROWS and all(board[r + k][c] == token for k in range(WIN)):
                return True
            # diag down-right
            if r + WIN - 1 < ROWS and c + WIN - 1 < COLS and all(board[r + k][c + k] == token for k in range(WIN)):
                return True
            # diag down-left
            if r + WIN - 1 < ROWS and c - (WIN - 1) >= 0 and all(board[r + k][c - k] == token for k in range(WIN)):
                return True
    return False

def draw():
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

current = random.randrange(NUM_PLAYERS)
show()

while True:
    token = TOKENS[current]
    col_idx = None
    while True:
        s = input(f"Player {token}, please enter a column: ").strip()
        if len(s) == 1 and 'A' <= s <= chr(ord('A') + COLS - 1):
            col_idx = ord(s) - ord('A')
            break
    if not place(col_idx, token):
        show()
        current = (current + 1) % NUM_PLAYERS
        continue
    show()
    if win(token):
        print(f"Player {token} won!")
        break
    if draw():
        print("It's a draw!")
        break
    current = (current + 1) % NUM_PLAYERS
