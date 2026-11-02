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
        row = []
        for _ in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    clear()
    header = "  "
    for i in range(COLS):
        header += " " + chr(ord('A') + i) + "  "
    print(header)
    print("+" + "---+" * COLS)
    for r in range(ROWS):
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
        print("+" + "---+" * COLS)

def is_valid_column(col):
    if len(col) != 1:
        return False
    if col < 'A' or col >= chr(ord('A') + COLS):
        return False
    return True

def get_col_index(col):
    return ord(col) - ord('A')

def is_column_full(board, c):
    return board[0][c] != " "

def place_checker(board, c, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][c] == " ":
            board[r][c] = checker
            return r, c
    return -1, -1  # shouldn't happen if we checked full column

def check_win(board, r, c, checker):
    # directions: horizontal, vertical, / diagonal, \ diagonal
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        count = 1
        # go one way
        nr, nc = r + dr, c + dc
        while 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == checker:
            count += 1
            nr += dr
            nc += dc
        # go other way
        nr, nc = r - dr, c - dc
        while 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == checker:
            count += 1
            nr -= dr
            nc -= dc
        if count >= 4:
            return True
    return False

def board_full(board):
    for c in range(COLS):
        if not is_column_full(board, c):
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    print_board(board)
    while True:
        checker = players[current]
        print(f"Player {checker}, please enter a column:")
        col_in = input().strip()
        if not is_valid_column(col_in):
            continue
        col = get_col_index(col_in)
        if is_column_full(board, col):
            current = (current + 1) % PLAYERS  # lose turn
            print_board(board)
            continue
        r, c = place_checker(board, col, checker)
        print_board(board)
        if check_win(board, r, c, checker):
            print(f"Player {checker} won!")
            break
        if board_full(board):
            print("It's a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
