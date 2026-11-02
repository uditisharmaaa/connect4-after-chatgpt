import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
WIN_NUM = 4

CHECKERS = ["X", "O", "V", "H", "M"]

def clear():
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
    clear()
    # print column letters
    letters = [chr(ord('A') + i) for i in range(COLS)]
    print("  " + "   ".join(letters))
    # print board
    for r in range(ROWS):
        line = "+"
        for c in range(COLS):
            line += "---+"
        print(line)
        line2 = "|"
        for c in range(COLS):
            line2 += " " + board[r][c] + " |"
        print(line2)
    line = "+"
    for c in range(COLS):
        line += "---+"
    print(line)

def valid_input(s):
    if len(s) != 1:
        return False
    s = s.upper()
    if s < 'A' or s >= chr(ord('A') + COLS):
        return False
    return True

def get_column_index(s):
    return ord(s.upper()) - ord('A')

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False  # column full

def check_win(board, checker):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS - WIN_NUM + 1):
            count = 0
            for i in range(WIN_NUM):
                if board[r][c+i] == checker:
                    count += 1
            if count == WIN_NUM:
                return True
    # vertical
    for c in range(COLS):
        for r in range(ROWS - WIN_NUM + 1):
            count = 0
            for i in range(WIN_NUM):
                if board[r+i][c] == checker:
                    count += 1
            if count == WIN_NUM:
                return True
    # diagonal down-right
    for r in range(ROWS - WIN_NUM + 1):
        for c in range(COLS - WIN_NUM + 1):
            count = 0
            for i in range(WIN_NUM):
                if board[r+i][c+i] == checker:
                    count += 1
            if count == WIN_NUM:
                return True
    # diagonal up-right
    for r in range(WIN_NUM -1, ROWS):
        for c in range(COLS - WIN_NUM + 1):
            count = 0
            for i in range(WIN_NUM):
                if board[r - i][c + i] == checker:
                    count += 1
            if count == WIN_NUM:
                return True
    return False

def check_draw(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board()
    players_checkers = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS - 1)
    print_board(board)
    while True:
        checker = players_checkers[current]
        print("Player {}, please enter a column:".format(checker))
        col_input = input()
        while not valid_input(col_input):
            print("Invalid input. Player {}, please enter a column:".format(checker))
            col_input = input()
        col = get_column_index(col_input)
        if not place_checker(board, col, checker):
            # column full lose turn
            print_board(board)
            print("Column full! Player {} loses turn.".format(checker))
        else:
            print_board(board)
            if check_win(board, checker):
                print("Player {} won!".format(checker))
                break
            if check_draw(board):
                print("The game is a draw.")
                break
        current = (current + 1) % PLAYERS

main()
