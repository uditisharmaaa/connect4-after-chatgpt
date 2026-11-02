import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        board.append([" "] * COLS)
    return board

def print_board(board):
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_column(col_letter):
    if len(col_letter) != 1:
        return False
    if col_letter < 'A' or col_letter >= chr(ord('A') + COLS):
        return False
    return True

def get_col_index(col_letter):
    return ord(col_letter) - ord('A')

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return -1, -1

def check_win(board, r, c, checker):
    # check horizontal
    count = 0
    for cc in range(max(0, c - 3), min(COLS, c + 4)):
        if board[r][cc] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # check vertical
    count = 0
    for rr in range(max(0, r - 3), min(ROWS, r + 4)):
        if board[rr][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # check diagonal /
    count = 0
    start_r = r + min(3, COLS - 1 - c)
    start_c = c - min(3, COLS - 1 - c)
    while start_r >= 3 and start_c < COLS - 3:
        start_r -= 1
        start_c += 1
    r1, c1 = start_r, start_c
    while r1 >= 0 and c1 < COLS:
        if board[r1][c1] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r1 -= 1
        c1 += 1
    # check diagonal \
    count = 0
    start_r = r - min(3, r)
    start_c = c - min(3, c)
    r1, c1 = start_r, start_c
    while r1 < ROWS and c1 < COLS:
        if board[r1][c1] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r1 += 1
        c1 += 1
    return False

def board_full(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    cur = random.randint(0, PLAYERS-1)
    checkers = CHECKERS[:PLAYERS]
    clear()
    print_board(board)
    while True:
        checker = checkers[cur]
        print(f"Player {checker}, please enter a column:")
        inp = input().strip().upper()
        if not is_valid_column(inp):
            continue
        col = get_col_index(inp)
        r, c = place_checker(board, col, checker)
        if r == -1:
            # column full, lose turn
            cur = (cur + 1) % PLAYERS
            continue
        clear()
        print_board(board)
        if check_win(board, r, c, checker):
            print(f"Player {checker} won!")
            break
        if board_full(board):
            print("Game ends in a draw!")
            break
        cur = (cur + 1) % PLAYERS

if __name__ == "__main__":
    main()
