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
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print(" ", end=" ")
    for c in range(COLS):
        print(letters[c], end="   ")
    print()
    line = "+---"*COLS + "+"
    for r in range(ROWS):
        print(line)
        print("|", end="")
        for c in range(COLS):
            print(" " + board[r][c] + " |", end="")
        print()
    print(line)

def valid_column(col):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if len(col) != 1:
        return False
    if col not in letters[:COLS]:
        return False
    return True

def get_column_index(col):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return letters.index(col)

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False

def board_full(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def check_winner(board, checker):
    # horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == checker and 
                board[r][c+1] == checker and 
                board[r][c+2] == checker and 
                board[r][c+3] == checker):
                return True
    # vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if (board[r][c] == checker and
                board[r+1][c] == checker and
                board[r+2][c] == checker and
                board[r+3][c] == checker):
                return True
    # diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if (board[r][c] == checker and
                board[r+1][c+1] == checker and
                board[r+2][c+2] == checker and
                board[r+3][c+3] == checker):
                return True
    # diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == checker and
                board[r-1][c+1] == checker and
                board[r-2][c+2] == checker and
                board[r-3][c+3] == checker):
                return True
    return False

board = create_board()
current_player = random.randint(0, PLAYERS -1)

print_board(board)

while True:
    print("Player " + CHECKERS[current_player] + ", please enter a column:")
    col = input().strip().upper()
    if not valid_column(col):
        continue
    col_index = get_column_index(col)
    if not place_checker(board, col_index, CHECKERS[current_player]):
        # column full, lose turn
        current_player = (current_player + 1) % PLAYERS
        print_board(board)
        continue
    if check_winner(board, CHECKERS[current_player]):
        print_board(board)
        print("Player " + CHECKERS[current_player] + " won!")
        break
    if board_full(board):
        print_board(board)
        print("Draw!")
        break
    current_player = (current_player + 1) % PLAYERS
    print_board(board)
