import os
import random
import string

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print("  A B C D E F G")
    print(" +---+---+---+---+---+---+---+")
    for row in board:
        print("|", end="")
        for col in row:
            print(" " + col + " |", end="")
        print()
        print(" +---+---+---+---+---+---+---+")
    print("Player", current_player + 1, "please enter a column:")

def is_valid_input(col):
    if col not in string.ascii_uppercase[:COLS]:
        return False
    return True

def get_next_open_row(board, col):
    for row in reversed(board):
        if row[col] == " ":
            return row

def is_valid_move(board, col):
    return board[0][col] == " "

def drop_checker(board, col, checker):
    for row in board:
        if row[col] == " ":
            row[col] = checker
            return

def winning_move(board, checker):
    # Check horizontal locations for win
    for c in range(COLS - 3):
        for r in range(ROWS):
            if board[r][c] == checker and board[r][c+1] == checker and board[r][c+2] == checker and board[r][c+3] == checker:
                return True

    # Check vertical locations for win
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == checker and board[r+1][c] == checker and board[r+2][c] == checker and board[r+3][c] == checker:
                return True

    # Check positively sloped diagonals
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == checker and board[r+1][c+1] == checker and board[r+2][c+2] == checker and board[r+3][c+3] == checker:
                return True

    # Check negatively sloped diagonals
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if board[r][c] == checker and board[r-1][c+1] == checker and board[r-2][c+2] == checker and board[r-3][c+3] == checker:
                return True

def draw(board):
    return " " not in [item for sublist in board for item in sublist]

# Initialize game
board = create_board()
current_player = random.randint(0, PLAYERS - 1)

while True:
    os.system('clear')
    print_board(board)
    col = input().strip().upper()
    if not is_valid_input(col):
        continue
    col = ord(col) - 65
    if not is_valid_move(board, col):
        continue
    drop_checker(board, col, CHECKERS[current_player])
    if winning_move(board, CHECKERS[current_player]):
        os.system('clear')
        print_board(board)
        print("Player", current_player + 1, "won!")
        break
    if draw(board):
        os.system('clear')
        print_board(board)
        print("It's a draw!")
        break
    current_player = (current_player + 1) % PLAYERS
