import os, random

# Constants (submission requires 6x7 and 2 players)
ROWS, COLS = 6, 7
PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"][:PLAYERS]
WIN_LEN = 4

def clear():
    os.system('clear')

def letters(n):
    return [chr(ord('A') + i) for i in range(n)]

def print_board(board):
    clear()
    hdr = "  " + "   ".join(letters(COLS))
    sep = "+" + "+".join(["---"] * COLS) + "+"
    print(hdr)
    for r in range(ROWS):
        print(sep)
        print("|" + "|".join(f" {board[r][c]} " for c in range(COLS)) + "|")
    print(sep)

def drop_checker(board, col, token):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r, col
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_dir(board, r, c, dr, dc, token):
    count = 0
    i, j = r, c
    while in_bounds(i, j) and board[i][j] == token:
        count += 1
        i += dr
        j += dc
    return count

def is_winner(board, token):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != token:
                continue
            # Check 4 directions (avoid double counting by only checking forward)
            if (check_dir(board, r, c, 0, 1, token) >= WIN_LEN or
                check_dir(board, r, c, 1, 0, token) >= WIN_LEN or
                check_dir(board, r, c, 1, 1, token) >= WIN_LEN or
                check_dir(board, r, c, 1, -1, token) >= WIN_LEN):
                return True
    return False

def is_draw(board):
    return all(board[r][c] != " " for r in range(ROWS) for c in range(COLS))

def get_valid_column():
    valid_letters = set(letters(COLS))
    while True:
        s = input().strip().upper()
        if len(s) == 1 and s in valid_letters:
            return ord(s) - ord('A')
        print("Invalid input. Please enter a valid column letter:")

def main():
    if COLS > 26 or PLAYERS < 2 or PLAYERS > 5:
        print("Configuration out of allowed range.")
        return
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    current = random.randrange(PLAYERS)
    print_board(board)
    while True:
        token = TOKENS[current]
        print(f"Player {token}, please enter a column:")
        col = get_valid_column()
        placed = drop_checker(board, col, token)
        print_board(board)
        if not placed:
            print("Column is full. Turn lost.")
        else:
            if is_winner(board, token):
                print(f"Player {token} won!")
                break
            if is_draw(board):
                print("It's a draw!")
                break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
