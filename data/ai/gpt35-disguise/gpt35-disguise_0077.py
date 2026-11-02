import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    clear_screen()
    letters = ""
    for c in range(COLS):
        letters += "  " + chr(ord('A') + c) + " "
    print(letters)
    print("+---" * COLS + "+")
    for r in range(ROWS):
        line = "|"
        for c in range(COLS):
            line += " " + board[r][c] + " |"
        print(line)
        print("+---" * COLS + "+")

def input_column(player):
    while True:
        col = input("Player " + CHECKERS[player] + ", please enter a column: ")
        if len(col) != 1:
            print("Invalid input. Please enter one letter.")
            continue
        if not col.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        col = col.upper()
        c = ord(col) - ord('A')
        if c < 0 or c >= COLS:
            print("Invalid column. Please enter a letter between A and " + chr(ord('A') + COLS -1))
            continue
        return c

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return -1  # column full

def check_winner(board, r, c):
    checker = board[r][c]
    if checker == " ":
        return False

    # horizontal
    count = 0
    for cc in range(COLS):
        if board[r][cc] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # vertical
    count = 0
    for rr in range(ROWS):
        if board[rr][c] == checker:
            count +=1
            if count ==4:
                return True
        else:
            count=0

    # diagonal /
    count = 0
    start_row = r
    start_col = c
    while start_row > 0 and start_col < COLS -1:
        start_row -=1
        start_col +=1
    rr = start_row
    cc = start_col
    while rr < ROWS and cc >= 0:
        if board[rr][cc] == checker:
            count +=1
            if count ==4:
                return True
        else:
            count =0
        rr +=1
        cc -=1

    # diagonal \
    count = 0
    start_row = r
    start_col = c
    while start_row >0 and start_col >0:
        start_row -=1
        start_col -=1
    rr = start_row
    cc = start_col
    while rr < ROWS and cc < COLS:
        if board[rr][cc] == checker:
            count +=1
            if count ==4:
                return True
        else:
            count =0
        rr +=1
        cc +=1

    return False

def is_draw(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS-1)
    print_board(board)
    while True:
        col = input_column(current_player)
        row = place_checker(board, col, CHECKERS[current_player])
        if row == -1:
            # column full, lose turn
            print("Column full, you lose your turn.")
        else:
            print_board(board)
            if check_winner(board, row, col):
                print("Player " + CHECKERS[current_player] + " won!")
                break
            if is_draw(board):
                print("Game ended in a draw.")
                break
            current_player = (current_player + 1) % PLAYERS

main()
