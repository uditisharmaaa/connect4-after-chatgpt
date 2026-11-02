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
        row = [" "]*COLS
        board.append(row)
    return board

def print_board(board):
    clear()
    header = "  "
    for i in range(COLS):
        header += " " + chr(ord('A')+i) + "  "
    print(header)
    for r in range(ROWS):
        line = "+"
        for c in range(COLS):
            line += "---+"
        print(line)
        row_line = "|"
        for c in range(COLS):
            row_line += " " + board[r][c] + " |"
        print(row_line)
    line = "+"
    for c in range(COLS):
        line += "---+"
    print(line)

def valid_input(s):
    if len(s) != 1:
        return False
    if not ('A' <= s <= chr(ord('A')+COLS-1)):
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

def check_win(board, checker):
    # horizontal
    for r in range(ROWS):
        count = 0
        for c in range(COLS):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    # vertical
    for c in range(COLS):
        count = 0
        for r in range(ROWS):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    # diagonal \
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if (board[r][c] == checker and board[r+1][c+1] == checker and
                board[r+2][c+2] == checker and board[r+3][c+3] == checker):
                return True
    # diagonal /
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if (board[r][c] == checker and board[r-1][c+1] == checker and
                board[r-2][c+2] == checker and board[r-3][c+3] == checker):
                return True
    return False

def check_draw(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

board = create_board()
players = CHECKERS[:PLAYERS]

current = random.randint(0, PLAYERS-1)

print_board(board)

while True:
    print("Player {}, please enter a column:".format(players[current]))
    s = input()
    while True:
        if not valid_input(s):
            print("Invalid input. Try again:")
        else:
            col = ord(s) - ord('A')
            if column_full(board, col):
                print("Column full. You lose your turn.")
                col = -1
                break
            else:
                break
        s = input()
    if col != -1:
        r, c = place_checker(board, col, players[current])
        print_board(board)
        if check_win(board, players[current]):
            print("Player {} won!".format(players[current]))
            break
        if check_draw(board):
            print("The game is a draw!")
            break
    else:
        print_board(board)
    current = (current + 1) % PLAYERS
