import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]

def make_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    os.system('clear')

def header(cols):
    letters = list(string.ascii_uppercase[:cols])
    print("  " + "   ".join(letters))

def sep(cols):
    print("+" + ("---+" * cols))

def show(board):
    clear_screen()
    header(len(board[0]))
    sep(len(board[0]))
    for r in range(len(board)):
        row = "|"
        for c in range(len(board[0])):
            row += " " + board[r][c] + " |"
        print(row)
        sep(len(board[0]))

def drop(board, col, token):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r, col
    return None

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_four(board, r, c, dr, dc, token):
    count = 0
    for i in range(4):
        nr = r + dr * i
        nc = c + dc * i
        if not in_bounds(nr, nc):
            return False
        if board[nr][nc] != token:
            return False
        count += 1
    return count == 4

def check_win(board, token):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != token:
                continue
            if check_four(board, r, c, 0, 1, token):
                return True
            if check_four(board, r, c, 1, 0, token):
                return True
            if check_four(board, r, c, 1, 1, token):
                return True
            if check_four(board, r, c, 1, -1, token):
                return True
    return False

def board_full(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def valid_col_input(s):
    if len(s) != 1:
        return False
    if s < "A" or s > chr(ord("A") + COLS - 1):
        return False
    return True

def main():
    players = TOKENS[:NUM_PLAYERS]
    board = make_board(ROWS, COLS)
    current = random.randint(0, NUM_PLAYERS - 1)
    show(board)

    while True:
        token = players[current]
        print(f"Player {token}, please enter a column:")
        user = input().strip().upper()

        while not valid_col_input(user):
            show(board)
            print("Invalid input. Please enter a valid column letter.")
            print(f"Player {token}, please enter a column:")
            user = input().strip().upper()

        col = ord(user) - ord("A")
        placed = drop(board, col, token)

        if placed is None:
            show(board)
            print(f"Column {user} is full. Turn lost.")
            current = (current + 1) % NUM_PLAYERS
            continue

        show(board)

        if check_win(board, token):
            print(f"Player {token} won!")
            break

        if board_full(board):
            print("It's a draw!")
            break

        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
