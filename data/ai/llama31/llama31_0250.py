import os
import random
import string

# Constants for game settings
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = "XOVHM"

# Function to create the game board
def create_board():
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

# Function to print the game board
def print_board(board):
    os.system('clear')
    print("  " + " ".join(string.ascii_uppercase[:NUM_COLS]))
    for row in board:
        print("+---" * NUM_COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * NUM_COLS + "+")

# Function to check if a column is valid
def is_valid_column(col):
    return 0 <= col < NUM_COLS

# Function to get the next available row in a column
def get_next_available_row(board, col):
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1

# Function to check for a win
def check_win(board, player):
    # Check horizontal wins
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == player and \
               board[row][col + 1] == player and \
               board[row][col + 2] == player and \
               board[row][col + 3] == player:
                return True

    # Check vertical wins
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS):
            if board[row][col] == player and \
               board[row + 1][col] == player and \
               board[row + 2][col] == player and \
               board[row + 3][col] == player:
                return True

    # Check diagonal wins (top-left to bottom-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if board[row][col] == player and \
               board[row + 1][col + 1] == player and \
               board[row + 2][col + 2] == player and \
               board[row + 3][col + 3] == player:
                return True

    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if board[row][col] == player and \
               board[row - 1][col + 1] == player and \
               board[row - 2][col + 2] == player and \
               board[row - 3][col + 3] == player:
                return True

    return False

# Function to check for a draw
def check_draw(board):
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if board[row][col] == " ":
                return False
    return True

# Main game loop
def play_game():
    board = create_board()
    players = list(CHECKERS[:NUM_PLAYERS])
    current_player = random.choice(players)
    print_board(board)
    print("Player", current_player, "starts the game.")

    while True:
        print("Player", current_player, "turn.")
        col = input("Enter a column (A-{}): ".format(string.ascii_uppercase[NUM_COLS - 1]))
        col = ord(col.upper()) - ord('A')
        if not is_valid_column(col):
            print("Invalid column. Try again.")
            continue
        row = get_next_available_row(board, col)
        if row == -1:
            print("Column is full. Try again.")
            continue
        board[row][col] = current_player
        print_board(board)
        if check_win(board, current_player):
            print("Player", current_player, "won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % len(players)]

play_game()
