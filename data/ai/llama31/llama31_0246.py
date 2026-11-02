import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2

# Checkers for each player
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Create the board
board = [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

# Function to print the board
def print_board():
    os.system('clear')
    print('  ' + ' '.join(chr(65 + i) for i in range(COLUMNS)))
    for row in board:
        print('+---' * COLUMNS + '+')
        print('| ' + ' | '.join(row) + ' |')
    print('+---' * COLUMNS + '+')

# Function to check for a win
def check_win(player):
    # Check horizontal locations for win
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player:
                return True

    # Check vertical locations for win
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True

    # Check positively sloped diagonals
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True

    # Check negatively sloped diagonals
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True

    return False

# Function to check for a draw
def check_draw():
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == ' ':
                return False
    return True

# Choose a random player to start
current_player = random.randint(0, PLAYERS - 1)

while True:
    print_board()
    print("Player", CHECKERS[current_player], "please enter a column (A-", chr(65 + COLUMNS - 1), "):")
    col = input().strip().upper()

    # Validate user input
    while not col.isalpha() or not 'A' <= col <= chr(65 + COLUMNS - 1):
        print("Invalid input. Please enter a column (A-", chr(65 + COLUMNS - 1), "):")
        col = input().strip().upper()

    col = ord(col) - 65

    # Place the checker in the chosen column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = CHECKERS[current_player]
            break
    else:
        print("Column is full. Please choose another column.")
        continue

    # Check for a win
    if check_win(CHECKERS[current_player]):
        print_board()
        print("Player", CHECKERS[current_player], "won!")
        break

    # Check for a draw
    if check_draw():
        print_board()
        print("It's a draw!")
        break

    # Switch to the next player
    current_player = (current_player + 1) % PLAYERS
