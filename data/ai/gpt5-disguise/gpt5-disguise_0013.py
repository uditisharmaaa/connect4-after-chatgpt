import os
import random
import string

ROWS = 6
COLS = 7
PLAYERS = 2  # between 2 and 5

tokens = ["X", "O", "V", "H", "M"][:PLAYERS]

board = []
for r in range(ROWS):
    row = []
    for c in range(COLS):
        row.append(" ")
    board.append(row)

letters = list(string.ascii_uppercase[:COLS])

def clear():
    os.system('clear')

def print_board():
    print("  " + "   ".join(letters))
    print("+" + "---+" * COLS)
    for r in range(ROWS):
        line = "|"
        for c in range(COLS):
            line += " " + board[r][c] + " |"
        print(line)
        print("+" + "---+" * COLS)

def drop_piece(col_idx, token):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = token
            return r, col_idx
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_dir(r, c, dr, dc, token):
    count = 0
    rr = r
    cc = c
    while in_bounds(rr, cc) and board[rr][cc] == token:
        count += 1
        rr += dr
        cc += dc
    return count

def check_win(r, c, token):
    # horizontal
    left = check_dir(r, c, 0, -1, token) - 1
    right = check_dir(r, c, 0, 1, token)
    if left + right >= 4: 
        return True
    # vertical
    up = check_dir(r, c, -1, 0, token) - 1
    down = check_dir(r, c, 1, 0, token)
    if up + down >= 4:
        return True
    # diag down-right / up-left
    ul = check_dir(r, c, -1, -1, token) - 1
    dr = check_dir(r, c, 1, 1, token)
    if ul + dr >= 4:
        return True
    # diag up-right / down-left
    ur = check_dir(r, c, -1, 1, token) - 1
    dl = check_dir(r, c, 1, -1, token)
    if ur + dl >= 4:
        return True
    return False

def board_full():
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

current = random.randrange(PLAYERS)

clear()
print_board()

winner = None

while True:
    t = tokens[current]
    col_input = ""
    while True:
        col_input = input("Player " + t + ", please enter a column: ").strip()
        if len(col_input) != 1:
            print("Invalid input. Enter a single letter from A to " + letters[-1] + ".")
            continue
        col_char = col_input.upper()
        if col_char not in letters:
            print("Invalid column. Enter a letter from A to " + letters[-1] + ".")
            continue
        break

    col_idx = letters.index(col_char)
    placed = drop_piece(col_idx, t)
    if placed is None:
        print("Column " + col_char + " is full. Turn lost.")
        current = (current + 1) % PLAYERS
        clear()
        print_board()
        if board_full():
            print("It's a draw!")
            break
        continue

    r, c = placed

    clear()
    print_board()

    if check_win(r, c, t):
        print("Player " + t + " won!")
        break

    if board_full():
        print("It's a draw!")
        break

    current = (current + 1) % PLAYERS
