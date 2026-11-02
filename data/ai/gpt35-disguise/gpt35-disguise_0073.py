import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def create_board():
    board = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    os.system('clear')
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    row_str = "  "
    for i in range(COLS):
        row_str += "  " + letters[i] + " "
    print(row_str)
    for r in range(ROWS):
        line = "+"
        for c in range(COLS):
            line += "---+"
        print(line)
        line = "|"
        for c in range(COLS):
            line += " " + board[r][c] + " |"
        print(line)
    line = "+"
    for c in range(COLS):
        line += "---+"
    print(line)

def valid_column(col):
    if len(col) != 1:
        return False
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if col not in letters[:COLS]:
        return False
    return True

def place_checker(board, col, checker):
    col_index = ord(col) - ord('A')
    for r in range(ROWS-1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True
    return False

def check_win(board, checker):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS - WIN_COUNT +1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r][c+i] == checker:
                    count +=1
            if count == WIN_COUNT:
                return True
    # vertical
    for c in range(COLS):
        for r in range(ROWS - WIN_COUNT +1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r+i][c] == checker:
                    count += 1
            if count == WIN_COUNT:
                return True
    # diagonal down-right
    for r in range(ROWS - WIN_COUNT +1):
        for c in range(COLS - WIN_COUNT +1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r+i][c+i] == checker:
                    count += 1
            if count == WIN_COUNT:
                return True
    # diagonal up-right
    for r in range(WIN_COUNT -1, ROWS):
        for c in range(COLS - WIN_COUNT +1):
            count = 0
            for i in range(WIN_COUNT):
                if board[r - i][c + i] == checker:
                    count +=1
            if count == WIN_COUNT:
                return True
    return False

def board_full(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

board = create_board()
players_checkers = CHECKERS[:PLAYERS]
turn = random.randint(0, PLAYERS-1)

print_board(board)

while True:
    p_checker = players_checkers[turn]
    col = input("Player {}, please enter a column: ".format(p_checker))
    col = col.strip().upper()
    if not valid_column(col):
        continue
    if not place_checker(board, col, p_checker):
        # column full and player loses turn
        turn = (turn + 1) % PLAYERS
        print_board(board)
        continue
    print_board(board)
    if check_win(board, p_checker):
        print("Player {} won!".format(p_checker))
        break
    if board_full(board):
        print("The game is a draw.")
        break
    turn = (turn + 1) % PLAYERS
