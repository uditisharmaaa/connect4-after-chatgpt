import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize board
board = [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Function to print the board
def print_board():
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| {} | {} | {} | {} | {} | {} | {} |".format(*row))
    print("+---+---+---+---+---+---+---+")

# Function to check if a column is valid
def is_valid_column(col):
    return 0 <= col < COLS and board[0][col] == " "

# Function to get the next available row in a column
def get_next_available_row(col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1

# Function to check for a win
def check_win(player):
    # Check horizontal locations for win
    for row in range(ROWS):
        for col in range(COLS - 3):
            if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player:
                return True

    # Check vertical locations for win
    for col in range(COLS):
        for row in range(ROWS - 3):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True

    # Check positively sloped diagonals
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True

    # Check negatively sloped diagonals
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True

    return False

# Randomly select the first player
current_player = random.randint(0, PLAYERS - 1)

while True:
    print_board()
    print("Player {}, please enter a column:".format(CHECKERS[current_player]))

    while True:
        col = input().upper()
        if col in "ABCDEFG":
            col = ord(col) - 65
            if is_valid_column(col):
                row = get_next_available_row(col)
                if row!= -1:
                    board[row][col] = CHECKERS[current_player]
                    break
                else:
                    print("Column is full, please choose another column.")
            else:
                print("Invalid column, please choose another column.")
        else:
            print("Invalid input, please enter a letter.")

    # Check for a win
    if check_win(CHECKERS[current_player]):
        print_board()
        print("Player {} won!".format(CHECKERS[current_player]))
        break

    # Check for a draw
    if all(board[0][col]!= " " for col in range(COLS)):
        print_board()
        print("It's a draw!")
        break

    # Switch player
    current_player = (current_player + 1) % PLAYERS
