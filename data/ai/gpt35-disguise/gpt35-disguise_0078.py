import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
WIN_CONDITION = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
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
    clear_screen()
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print("  " + "   ".join(letters[:COLS]))
    print("+---" * COLS + "+")
    for r in range(ROWS):
        line = "| "
        for c in range(COLS):
            line += board[r][c] + " | "
        print(line)
        print("+---" * COLS + "+")

def valid_input(s):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if len(s) != 1:
        return False
    if s not in letters[:COLS]:
        return False
    return True

def column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return -1, -1

def check_win(board, row, col, checker):
    # horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count += 1
            if count == WIN_CONDITION:
                return True
        else:
            count = 0
    # vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count == WIN_CONDITION:
                return True
        else:
            count = 0
    # diagonal /
    count = 0
    start_r = row
    start_c = col
    while start_r > 0 and start_c < COLS - 1:
        start_r -= 1
        start_c += 1
    r = start_r
    c = start_c
    count = 0
    while r < ROWS and c >= 0:
        if board[r][c] == checker:
            count += 1
            if count == WIN_CONDITION:
                return True
        else:
            count = 0
        r += 1
        c -= 1
    # diagonal \
    start_r = row
    start_c = col
    while start_r > 0 and start_c > 0:
        start_r -= 1
        start_c -= 1
    r = start_r
    c = start_c
    count = 0
    while r < ROWS and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count == WIN_CONDITION:
                return True
        else:
            count = 0
        r += 1
        c += 1
    return False

def board_full(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS -1)
    while True:
        print_board(board)
        print("Player " + players[current] + ", please enter a column:")
        col_letter = input().strip().upper()
        if not valid_input(col_letter):
            continue
        col = ord(col_letter) - ord('A')
        if column_full(board, col):
            # turn lost
            current = (current +1) % PLAYERS
            continue
        row, col = place_checker(board, col, players[current])
        if check_win(board, row, col, players[current]):
            print_board(board)
            print("Player " + players[current] + " won!")
            break
        if board_full(board):
            print_board(board)
            print("The game is a draw.")
            break
        current = (current +1) % PLAYERS

if __name__ == "__main__":
    main()
