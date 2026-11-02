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
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    line = "+---" * COLS + "+"
    for row in board:
        print(line)
        s = "|"
        for c in row:
            s += " " + c + " |"
        print(s)
    print(line)

def is_valid_column(col):
    if len(col) != 1:
        return False
    if not ('A' <= col <= chr(ord('A') + COLS - 1)):
        return False
    return True

def column_index(col):
    return ord(col) - ord('A')

def is_column_full(board, col):
    return board[0][col] != " "

def place_checker(board, col, checker):
    for r in reversed(range(ROWS)):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return -1

def check_win(board, r, c, checker):
    # check horizontal
    count = 0
    for col in range(COLS):
        if board[r][col] == checker:
            count +=1
            if count == 4:
                return True
        else:
            count =0
    # check vertical
    count = 0
    for row in range(ROWS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # check diagonal /
    count = 0
    start_r = r
    start_c = c
    while start_r > 0 and start_c < COLS -1:
        start_r -=1
        start_c +=1
    rr = start_r
    cc = start_c
    while rr < ROWS and cc >= 0:
        if board[rr][cc] == checker:
            count +=1
            if count ==4:
                return True
        else:
            count = 0
        rr +=1
        cc -=1
    # check diagonal \
    count =0
    start_r = r
    start_c = c
    while start_r >0 and start_c >0:
        start_r -=1
        start_c -=1
    rr = start_r
    cc = start_c
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

def board_full(board):
    for c in range(COLS):
        if not is_column_full(board, c):
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS -1)
    print_board(board)
    while True:
        player = players[current]
        print("Player {}, please enter a column:".format(player))
        col = input().strip().upper()
        while not is_valid_column(col):
            print("Invalid input. Please enter a column:")
            col = input().strip().upper()
        c = column_index(col)
        if is_column_full(board, c):
            print("Column full, you lose your turn.")
            current = (current +1) % PLAYERS
            print_board(board)
            continue
        r = place_checker(board, c, player)
        print_board(board)
        if check_win(board, r, c, player):
            print("Player {} won!".format(player))
            break
        if board_full(board):
            print("Draw!")
            break
        current = (current +1) % PLAYERS

main()
