import os
import random
import string

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize the board
board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board():
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| {} | {} | {} | {} | {} | {} | {} |".format(*row))
    print("+---+---+---+---+---+---+---+")

def validate_input(player, input_char):
    if not input_char.isalpha():
        return False
    if input_char.upper() not in string.ascii_uppercase[:BOARD_COLS]:
        return False
    if board[0][string.ascii_uppercase.index(input_char.upper())]!= " ":
        return False
    return True

def drop_checker(player, col):
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = CHECKERS[player]
            return

def check_win(player):
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == CHECKERS[player] and \
               board[row][col + 1] == CHECKERS[player] and \
               board[row][col + 2] == CHECKERS[player] and \
               board[row][col + 3] == CHECKERS[player]:
                return True
    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS):
            if board[row][col] == CHECKERS[player] and \
               board[row + 1][col] == CHECKERS[player] and \
               board[row + 2][col] == CHECKERS[player] and \
               board[row + 3][col] == CHECKERS[player]:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == CHECKERS[player] and \
               board[row + 1][col + 1] == CHECKERS[player] and \
               board[row + 2][col + 2] == CHECKERS[player] and \
               board[row + 3][col + 3] == CHECKERS[player]:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == CHECKERS[player] and \
               board[row - 1][col + 1] == CHECKERS[player] and \
               board[row - 2][col + 2] == CHECKERS[player] and \
               board[row - 3][col + 3] == CHECKERS[player]:
                return True
    return False

def check_draw():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == " ":
                return False
    return True

def game():
    player = random.randint(0, PLAYERS - 1)
    print_board()
    while True:
        print("Player {}, please enter a column:".format(CHECKERS[player]))
        input_char = input().strip().upper()
        if not validate_input(player, input_char):
            print("Invalid input. Please try again.")
            continue
        col = string.ascii_uppercase.index(input_char)
        drop_checker(player, col)
        print_board()
        if check_win(player):
            print("Player {} won!".format(CHECKERS[player]))
            return
        if check_draw():
            print("It's a draw!")
            return
        player = (player + 1) % PLAYERS

game()
