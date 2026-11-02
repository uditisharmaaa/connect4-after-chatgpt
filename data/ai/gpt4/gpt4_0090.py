import os
import random

# Constants for game settings
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = 2  # Set to 2 players as per assignment
CHECKERS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LETTERS = [chr(i) for i in range(ord('A'), ord('A') + COLUMNS)]  # ['A', 'B', ..., 'G']

# Function to create an empty game board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Function to clear console screen
def clear_screen():
    os.system('clear')

# Function to print the board
def print_board(board):
    clear_screen()
    # Print column headers
    print("  " + "   ".join(COLUMN_LETTERS))
    print("+" + "---+" * COLUMNS)

    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

# Function to check if input column is valid
def is_valid_column(column, board):
    if column not in COLUMN_LETTERS:
        return False
    col_index = COLUMN_LETTERS.index(column)
    return any(row[col_index] == " " for row in board)

# Function to place a checker in the chosen column
def place_checker(column, checker, board):
    col_index = COLUMN_LETTERS.index(column)
    for row in reversed(board):  # Start from bottom row
        if row[col_index] == " ":
            row[col_index] = checker
            break

# Function to check for a win
def check_win(board, checker):
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col] == row[col+1] == row[col+2] == row[col+3] == checker:
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if (board[row][col] == board[row+1][col] == 
                    board[row+2][col] == board[row+3][col] == checker):
                return True

    # Check diagonals (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if (board[row][col] == board[row+1][col+1] == 
                    board[row+2][col+2] == board[row+3][col+3] == checker):
                return True

    # Check diagonals (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if (board[row][col] == board[row-1][col+1] == 
                    board[row-2][col+2] == board[row-3][col+3] == checker):
                return True

    return False

# Function to check for a draw
def check_draw(board):
    return all(all(cell != " " for cell in row) for row in board)

# Main game logic
def connect4():
    # Initialize board and players
    board = create_board()
    current_players = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)  # Randomly select first player

    while True:
        print_board(board)
        current_player = current_players[current_player_index]
        print(f"Player {current_player}, please enter a column:")

        # Get and validate user input
        while True:
            column = input().upper()
            if is_valid_column(column, board):
                break
            print("Invalid input. Please enter a valid column:")

        # Place the checker
        place_checker(column, current_player, board)

        # Check for win condition
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        # Check for draw condition
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to next player
        current_player_index = (current_player_index + 1) % PLAYERS

# Run the game
if __name__ == "__main__":
    connect4()
