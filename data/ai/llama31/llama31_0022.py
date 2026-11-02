import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2

# Checkers for players
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize board
board = [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

# Function to print the board
def print_board():
    os.system('clear')
    print("  A B C D E F G")
    for row in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        print("|", end="")
        for col in range(NUM_COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    print("+---" * NUM_COLS + "+")
    print()

# Function to check for win
def check_win(player):
    # Check horizontal locations for win
    for c in range(NUM_COLS - 3):
        for r in range(NUM_ROWS):
            if board[r][c] == player and board[r][c + 1] == player and board[r][c + 2] == player and board[r][c + 3] == player:
                return True

    # Check vertical locations for win
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - 3):
            if board[r][c] == player and board[r + 1][c] == player and board[r + 2][c] == player and board[r + 3][c] == player:
                return True

    # Check positively sloped diagonals
    for c in range(NUM_COLS - 3):
        for r in range(NUM_ROWS - 3):
            if board[r][c] == player and board[r + 1][c + 1] == player and board[r + 2][c + 2] == player and board[r + 3][c + 3] == player:
                return True

    # Check negatively sloped diagonals
    for c in range(NUM_COLS - 3):
        for r in range(3, NUM_ROWS):
            if board[r][c] == player and board[r - 1][c + 1] == player and board[r - 2][c + 2] == player and board[r - 3][c + 3] == player:
                return True

    return False

# Function to check for draw
def check_draw():
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if board[row][col] == " ":
                return False
    return True

# Main game loop
players = CHECKERS[:NUM_PLAYERS]
current_player_index = random.randint(0, NUM_PLAYERS - 1)

while True:
    print_board()
    current_player = players[current_player_index]
    print("Player " + current_player + ", please enter a column (A-G):")
    col = input().upper()

    # Validate input
    while col < 'A' or col > 'G':
        print("Invalid input. Please enter a column (A-G):")
        col = input().upper()

    col_index = ord(col) - ord('A')

    # Check if column is full
    if board[NUM_ROWS - 1][col_index]!= " ":
        print("Column is full. Please choose another column.")
        continue

    # Place checker
    for row in range(NUM_ROWS):
        if board[row][col_index] == " ":
            board[row][col_index] = current_player
            break

    # Check for win
    if check_win(current_player):
        print_board()
        print("Player " + current_player + " won!")
        break

    # Check for draw
    if check_draw():
        print_board()
        print("It's a draw!")
        break

    # Switch to next player
    current_player_index = (current_player_index + 1) % NUM_PLAYERS
