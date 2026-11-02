import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]

def make_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear():
    os.system('clear')

def letters_for_cols(n):
    return [string.ascii_uppercase[i] for i in range(n)]

def print_board(board):
    cols = len(board[0])
    letters = letters_for_cols(cols)
    print("  " + "   ".join(letters))
    line = "+" + "+".join(["---"] * cols) + "+"
    for r in range(len(board)):
        print(line)
        row_str = "|"
        for c in range(cols):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(line)

def drop_piece(board, col, token):
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r, col
    return None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, token):
    rows = len(board)
    cols = len(board[0])
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in dirs:
                count = 1
                rr, cc = r + dr, c + dc
                while count < 4 and in_bounds(rr, cc, rows, cols) and board[rr][cc] == token:
                    count += 1
                    rr += dr
                    cc += dc
                if count == 4:
                    return True
    return False

def board_full(board):
    for r in board:
        for v in r:
            if v == " ":
                return False
    return True

def get_col_input(valid_letters):
    while True:
        s = input("Please enter a column: ").strip()
        if not s:
            print("Invalid input.")
            continue
        ch = s[0].upper()
        if ch in valid_letters:
            return ch
        else:
            print("Invalid input.")

def main():
    players = TOKENS[:NUM_PLAYERS]
    board = make_board(ROWS, COLS)
    start = random.randrange(len(players))
    turn = start
    clear()
    print_board(board)
    letters = letters_for_cols(COLS)

    while True:
        token = players[turn]
        print(f"Player {token}, please enter a column:")
        col_letter = get_col_input(letters)
        col_idx = letters.index(col_letter)

        placed = drop_piece(board, col_idx, token)
        clear()
        print_board(board)

        if placed is None:
            print("Column is full. Turn lost.")
            turn = (turn + 1) % len(players)
            continue

        if check_win(board, token):
            print(f"Player {token} won!")
            break

        if board_full(board):
            print("Game is a draw!")
            break

        turn = (turn + 1) % len(players)

if __name__ == "__main__":
    main()
