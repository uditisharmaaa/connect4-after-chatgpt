import os
import random

# Constants for game configuration
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Supports up to 5 players

# Function to initialize the game board
def initialize_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Function to print the game board
def print_board(board):
    os.system('clear')  # Clears the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

# Function to check for invalid input
def is_valid_input(input):
    return input.isalpha() and len(input) == 1 and "A" <= input < chr(65 + COLUMNS)

# Function to place the checker in the chosen column
def place_checker(board, column, checker):
    for row in reversed(board):  # Start from bottom row
        if row[column] == " ":
            row[column] = checker
            return True
    return False  # Column is full

# Function to check for a win condition
def check_win(board, checker):
    def check_direction(x, y, dx, dy):
        count = 0
        for _ in range(4):  # Must find 4 in a direction
            if 0 <= x < ROWS and 0 <= y < COLUMNS and board[x][y] == checker:
                count += 1
            else:
                break
            x, y = x + dx, y + dy
        return count == 4

    for x in range(ROWS):
        for y in range(COLUMNS):
            if board[x][y] == checker:
                if (check_direction(x, y, 0, 1) or   # Horizontal
                    check_direction(x, y, 1, 0) or   # Vertical
                    check_direction(x, y, 1, 1) or   # Diagonal \
                    check_direction(x, y, 1, -1)):   # Diagonal /
                    return True
    return False

# Function to check for a draw condition
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main function to execute the game
def connect_4():

    board = initialize_board()
    current_player = random.randint(0, PLAYER_COUNT - 1)
    checkers_in_game = CHECKERS[:PLAYER_COUNT]

    print_board(board)

    while True:
        current_checker = checkers_in_game[current_player]
        column = None

        while column is None:
            user_input = input(f"Player {current_checker}, please enter a column: ")
            if is_valid_input(user_input):
                column_index = ord(user_input.upper()) - 65
                if place_checker(board, column_index, current_checker):
                    column = column_index
                else:
                    print("Column is full. Try a different column.")
            else:
                print("Invalid input. Please enter a valid column letter.")

        print_board(board)

        # Check if current player has won
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check if the game is a draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Alternate players
        current_player = (current_player + 1) % PLAYER_COUNT

# Start the game
connect_4()
