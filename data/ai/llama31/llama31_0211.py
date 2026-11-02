import os
import random
import string

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = "XOVHM"

# Initialize board
board = [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board():
    os.system('clear')
    print("  " + " ".join(string.ascii_uppercase[:COLS]))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def validate_input(player, col):
    if not col.isalpha():
        print("Invalid input. Please enter a letter.")
        return False
    if col.upper() not in string.ascii_uppercase[:COLS]:
        print("Invalid input. Column out of range.")
        return False
    if board[0][string.ascii_uppercase[:COLS].index(col.upper())]!= " ":
        print("Invalid input. Column is full.")
        return False
    return True

def place_checker(player, col):
    for row in reversed(board):
        if row[string.ascii_uppercase[:COLS].index(col.upper())] == " ":
            row[string.ascii_uppercase[:COLS].index(col.upper())] = CHECKERS[player]
            break

def check_win(player):
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == row[i + 1] == row[i + 2] == row[i + 3] == CHECKERS[player]:
                return True

    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col] == board[i + 1][col] == board[i + 2][col] == board[i + 3][col] == CHECKERS[player]:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == CHECKERS[player]:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] == CHECKERS[player]:
                return True

    return False

def check_draw():
    for row in board:
        if " " in row:
            return False
    return True

# Randomly select first player
current_player = random.randint(0, PLAYERS - 1)

while True:
    print_board()
    print("Player", CHECKERS[current_player], "turn.")
    col = input("Enter a column: ").upper()
    while not validate_input(current_player, col):
        col = input("Enter a column: ").upper()
    place_checker(current_player, col)
    if check_win(current_player):
        print_board()
        print("Player", CHECKERS[current_player], "won!")
        break
    if check_draw():
        print_board()
        print("It's a draw!")
        break
    current_player = (current_player + 1) % PLAYERS
