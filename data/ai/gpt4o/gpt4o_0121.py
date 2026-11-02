import os
import random

# Constants for board dimensions and player settings
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]

# Function to create an empty game board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Function to print the game board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join([chr(65 + i) for i in range(COLUMNS)]))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

# Function to validate input
def valid_input(choice):
    if len(choice) == 1 and choice.isalpha():
        choice = choice.upper()
        if ord(choice) - 65 < COLUMNS:
            return True
    return False

# Function to place a checker on the board
def place_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

# Function to check for a win condition
def check_win(board, checker):
    return check_horizontal(board, checker) or check_vertical(board, checker) or check_diagonal(board, checker)

def check_horizontal(board, checker):
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col] == checker and row[col + 1] == checker and row[col + 2] == checker and row[col + 3] == checker:
                return True
    return False

def check_vertical(board, checker):
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True
    return False

def check_diagonal(board, checker):
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True
        for col in range(3, COLUMNS):
            if board[row][col] == checker and board[row + 1][col - 1] == checker and board[row + 2][col - 2] == checker and board[row + 3][col - 3] == checker:
                return True
    return False

# Function to check for a draw condition
def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

# Function to get column number from choice
def get_column(choice):
    return ord(choice.upper()) - 65

# Main game function
def play_game():
    board = create_board()
    current_player = random.choice(CHECKERS)
    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column:")
        choice = input().strip()

        while not valid_input(choice):
            print("Invalid input. Try again:")
            choice = input().strip()

        col = get_column(choice)

        if place_checker(board, col, current_player):
            print_board(board)
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
            current_player = CHECKERS[(CHECKERS.index(current_player) + 1) % PLAYERS]
        else:
            print("Column is full. You lose the turn.")

if __name__ == "__main__":
    play_game()
