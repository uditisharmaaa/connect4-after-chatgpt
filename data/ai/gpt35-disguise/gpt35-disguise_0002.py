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
    clear()
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    header = "  "
    for i in range(COLS):
        header += " " + letters[i] + "  "
    print(header)
    for r in range(ROWS):
        print("+" + "---+" * COLS)
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+" + "---+" * COLS)

def valid_column(col):
    if len(col) != 1:
        return False
    if not col.isalpha():
        return False
    col = col.upper()
    if ord(col) < ord("A") or ord(col) >= ord("A") + COLS:
        return False
    return True

def column_index(col):
    return ord(col.upper()) - ord("A")

def place_checker(board, col, checker):
    c = column_index(col)
    # place at lowest empty row in column c
    for r in range(ROWS - 1, -1, -1):
        if board[r][c] == " ":
            board[r][c] = checker
            return True
    return False  # column full

def check_win(board, checker):
    # horizontal check
    for r in range(ROWS):
        count = 0
        for c in range(COLS):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    # vertical check
    for c in range(COLS):
        count = 0
        for r in range(ROWS):
            if board[r][c] == checker:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    # diagonal down-right check
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True
    # diagonal up-right check
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True
    return False

def board_full(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def game():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS - 1)
    print_board(board)
    while True:
        player = players[current]
        print("Player " + player + ", please enter a column:")
        inp = input()
        while not valid_column(inp):
            print("Invalid input. Player " + player + ", please enter a column:")
            inp = input()
        placed = place_checker(board, inp, player)
        if not placed:
            # turn lost if column full
            current = (current + 1) % PLAYERS
            print_board(board)
            continue
        print_board(board)
        if check_win(board, player):
            print("Player " + player + " won!")
            break
        if board_full(board):
            print("The game is a draw.")
            break
        current = (current + 1) % PLAYERS

game()
