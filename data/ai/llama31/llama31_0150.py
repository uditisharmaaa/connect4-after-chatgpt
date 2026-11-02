import os
import random

# Constant variables
BOARD_COLUMNS = 7
BOARD_ROWS = 6
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize the board
board = [[" " for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]

# Choose a random first player
current_player = random.randint(0, PLAYERS - 1)

def print_board():
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for row in range(BOARD_ROWS):
        print("+---+---+---+---+---+---+---+")
        print("| ", end="")
        for col in range(BOARD_COLUMNS):
            print(board[row][col], end=" | ")
        print()
    print("+---+---+---+---+---+---+---+")

def validate_input(column):
    if not column.isalpha():
        return False
    column = ord(column.upper()) - ord('A')
    if column < 0 or column >= BOARD_COLUMNS:
        return False
    return True

def place_checker(column):
    column = ord(column.upper()) - ord('A')
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = CHECKERS[current_player]
            return True
    return False

def check_win():
    # Check horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS - 3):
            if board[row][col]!= " " and board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3]:
                return True
    # Check vertical
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLUMNS):
            if board[row][col]!= " " and board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col]:
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLUMNS - 3):
            if board[row][col]!= " " and board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3]:
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLUMNS - 3):
            if board[row][col]!= " " and board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3]:
                return True
    return False

def check_draw():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLUMNS):
            if board[row][col] == " ":
                return False
    return True

while True:
    print_board()
    print("Player", CHECKERS[current_player], "please enter a column:")
    column = input().upper()
    while not validate_input(column):
        print("Invalid input. Please enter a column letter (A-G):")
        column = input().upper()
    if not place_checker(column):
        print("Column is full. Please enter another column.")
        continue
    if check_win():
        print_board()
        print("Player", CHECKERS[current_player], "won!")
        break
    if check_draw():
        print_board()
        print("It's a draw!")
        break
    current_player = (current_player + 1) % PLAYERS
