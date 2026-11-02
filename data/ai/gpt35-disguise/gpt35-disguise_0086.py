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
    letters = ""
    for i in range(COLS):
        letters += "  " + chr(ord('A') + i) + " "
    print(letters)
    print("+---" * COLS + "+")
    for r in range(ROWS):
        line = "|"
        for c in range(COLS):
            line += " " + board[r][c] + " |"
        print(line)
        print("+---" * COLS + "+")

def get_column_number(input_col):
    if len(input_col) != 1:
        return -1
    c = ord(input_col)
    if c < ord('A') or c >= ord('A') + COLS:
        return -1
    return c - ord('A')

def place_checker(board, col, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

def check_winner(board, checker):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True
    # vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True
    # diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True
    return False

def is_draw(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    turn = random.randint(0, PLAYERS -1)
    while True:
        print_board(board)
        print("Player " + players[turn] + ", please enter a column:")
        col_input = input()
        col = get_column_number(col_input)
        if col == -1:
            continue
        if not place_checker(board, col, players[turn]):
            turn = (turn +1) % PLAYERS
            continue
        if check_winner(board, players[turn]):
            print_board(board)
            print("Player " + players[turn] + " won!")
            break
        if is_draw(board):
            print_board(board)
            print("Draw!")
            break
        turn = (turn +1) % PLAYERS

main()
