import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize board
board = [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

# Function to print board
def print_board():
    os.system('clear')
    print("  " + "   ".join([chr(65+i) for i in range(NUM_COLS)]))
    print("+" + "---+" * NUM_COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * NUM_COLS)

# Function to check if column is full
def is_column_full(column):
    return board[0][column]!= " "

# Function to place checker in column
def place_checker(column, checker):
    for row in range(NUM_ROWS-1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return

# Function to check for win
def check_win(checker):
    # Check horizontal
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == checker and board[row][col+1] == checker and board[row][col+2] == checker and board[row][col+3] == checker:
                return True

    # Check vertical
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS):
            if board[row][col] == checker and board[row+1][col] == checker and board[row+2][col] == checker and board[row+3][col] == checker:
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if board[row][col] == checker and board[row+1][col+1] == checker and board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == checker and board[row-1][col+1] == checker and board[row-2][col+2] == checker and board[row-3][col+3] == checker:
                return True

    return False

# Main game loop
current_player = random.randint(0, NUM_PLAYERS-1)
while True:
    print_board()
    print("Player " + CHECKERS[current_player] + ", please enter a column (A-" + chr(64+NUM_COLS) + "): ")
    column = input().strip().upper()
    if column < 'A' or column > chr(64+NUM_COLS) or is_column_full(ord(column)-65):
        print("Invalid input. Please try again.")
        input("Press enter to continue...")
        continue
    place_checker(ord(column)-65, CHECKERS[current_player])
    if check_win(CHECKERS[current_player]):
        print_board()
        print("Player " + CHECKERS[current_player] + " won!")
        break
    if all(all(cell!= " " for cell in row) for row in board):
        print_board()
        print("It's a draw!")
        break
    current_player = (current_player + 1) % NUM_PLAYERS
