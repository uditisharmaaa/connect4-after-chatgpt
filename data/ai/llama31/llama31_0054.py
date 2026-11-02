import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
PLAYERS_CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize the board
board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Function to print the board
def print_board():
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for row in range(BOARD_ROWS):
        print("+---+---+---+---+---+---+---+")
        print("|", end=" ")
        for col in range(BOARD_COLS):
            print(board[row][col], end=" | ")
        print()
    print("+---+---+---+---+---+---+---+")

# Function to validate user input
def validate_input(column):
    if not column.isalpha():
        return False
    if column.upper() not in "ABCDEFG":
        return False
    column = ord(column.upper()) - ord('A')
    for row in range(BOARD_ROWS):
        if board[row][column] == " ":
            return True
    return False

# Function to place a checker
def place_checker(column, checker):
    column = ord(column.upper()) - ord('A')
    for row in range(BOARD_ROWS-1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return

# Function to check for a win
def check_win(checker):
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS-3):
            if board[row][col] == checker and board[row][col+1] == checker and board[row][col+2] == checker and board[row][col+3] == checker:
                return True
    # Check vertical
    for row in range(BOARD_ROWS-3):
        for col in range(BOARD_COLS):
            if board[row][col] == checker and board[row+1][col] == checker and board[row+2][col] == checker and board[row+3][col] == checker:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS-3):
        for col in range(BOARD_COLS-3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS-3):
            if board[row][col] == checker and board[row-1][col+1] == checker and board[row-2][col+2] == checker and board[row-3][col+3] == checker:
                return True
    return False

# Function to check for a draw
def check_draw():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == " ":
                return False
    return True

# Main game loop
num_players = 2
players = PLAYERS_CHECKERS[:num_players]
current_player = random.choice(players)

while True:
    print_board()
    print("Player", current_player, "please enter a column:")
    column = input().upper()
    while not validate_input(column):
        print("Invalid input. Please try again.")
        column = input().upper()
    place_checker(column, current_player)
    if check_win(current_player):
        print_board()
        print("Player", current_player, "won!")
        break
    elif check_draw():
        print_board()
        print("It's a draw!")
        break
    current_player = players[(players.index(current_player) + 1) % num_players]
