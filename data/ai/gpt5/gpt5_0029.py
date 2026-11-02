import os, random, string

# Constants (submission: 6x7 board, 2 players)
ROWS = 6
COLS = 7   # max 26
NUM_PLAYERS = 2  # 2..5
TOKENS = "XOVHM"[:NUM_PLAYERS]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear_and_print(board):
    os.system('clear')
    letters = string.ascii_uppercase[:len(board[0])]
    print("  " + "   ".join(letters))
    sep = "+" + "+".join(["---"] * len(board[0])) + "+"
    for r in range(len(board)):
        print(sep)
        row = "|" + "|".join(f" {board[r][c]} " for c in range(len(board[0]))) + "|"
        print(row)
    print(sep)

def valid_col_input(s):
    return len(s) == 1 and 'A' <= s <= chr(ord('A') + COLS - 1)

def drop_token(board, col, token):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r, col
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win_from(board, r, c, token, dr, dc):
    count = 0
    rr, cc = r, c
    while in_bounds(rr, cc) and board[rr][cc] == token:
        count += 1
        rr -= dr; cc -= dc
    rr, cc = r + dr, c + dc
    while in_bounds(rr, cc) and board[rr][cc] == token:
        count += 1
        rr += dr; cc += dc
    return count >= 4

def check_win(board, r, c, token):
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    return any(check_win_from(board, r, c, token, dr, dc) for dr, dc in dirs)

def is_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    if COLS > 26 or NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Invalid configuration."); return
    board = make_board(ROWS, COLS)
    current = random.randrange(NUM_PLAYERS)
    clear_and_print(board)
    while True:
        token = TOKENS[current]
        col_input = input(f"Player {token}, please enter a column: ").strip().upper()
        while not valid_col_input(col_input):
            col_input = input("Invalid input. Please enter a valid column letter: ").strip().upper()
        col = ord(col_input) - ord('A')
        placed = drop_token(board, col, token)
        if placed is None:
            print("Column is full. Turn lost.")
            current = (current + 1) % NUM_PLAYERS
            continue
        r, c = placed
        clear_and_print(board)
        if check_win(board, r, c, token):
            print(f"Player {token} won!")
            break
        if is_draw(board):
            print("It's a draw!")
            break
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
