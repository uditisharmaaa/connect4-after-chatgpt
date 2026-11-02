import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Function to clear the console
def clear_console():
    os.system('clear')

# Function to initialize and create the board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    clear_console()
    header = "  " + "   ".join(chr(65 + i) for i in range(COLUMNS))
    print(header)
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Function to validate user input for the column choice
def validate_input(input_str):
    if len(input_str) == 1 and 'A' <= input_str <= chr(64 + COLUMNS):
        return True
    return False

# Function to place a checker in the chosen column
def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

# Function to check for horizontal, vertical, and diagonal wins
def check_win(board, checker):
    # Check horizontal win
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col] == row[col + 1] == row[col + 2] == row[col + 3] == checker:
                return True

    # Check vertical win
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] == checker:
                return True

    # Check diagonal wins
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == checker:
                return True
            if board[row + 3][col] == board[row + 2][col + 1] == board[row + 1][col + 2] == board[row][col + 3] == checker:
                return True

    return False

# Function to check if the board is filled, leading to a draw
def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

def connect4():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        current_checker = CHECKERS[current_player]
        print(f"Player {current_checker}, please enter a column:")
        column_input = input().strip().upper()

        while not validate_input(column_input):
            print("Invalid input. Please enter a column (A-G):")
            column_input = input().strip().upper()

        column_index = ord(column_input) - 65

        if not place_checker(board, column_index, current_checker):
            print("Column is full. You lose your turn.")
        else:
            print_board(board)

            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                break

            if check_draw(board):
                print("The game is a draw!")
                break

        current_player = (current_player + 1) % PLAYERS

# Start the game
if __name__ == "__main__":
    connect4()
