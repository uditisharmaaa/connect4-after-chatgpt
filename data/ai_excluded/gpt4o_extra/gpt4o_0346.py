import os
import random

# Constants for the board dimensions and number of players
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 2

# Mapping checkers for players
CHECKERS = ["X", "O", "V", "H", "M"][:MAX_PLAYERS]

# Function to initialize the board
def initialize_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

# Function to check for a win
def check_for_win(board, checker):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row][col+1] == checker and \
               board[row][col+2] == checker and board[row][col+3] == checker:
                return True

    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == checker and board[row+1][col] == checker and \
               board[row+2][col] == checker and board[row+3][col] == checker:
                return True

    # Diagonal (down-right) check
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == checker and board[row+1][col+1] == checker and \
               board[row+2][col+2] == checker and board[row+3][col+3] == checker:
                return True

    # Diagonal (down-left) check
    for row in range(ROWS - 3):
        for col in range(3, COLUMNS):
            if board[row][col] == checker and board[row+1][col-1] == checker and \
               board[row+2][col-2] == checker and board[row+3][col-3] == checker:
                return True

    return False

# Function to check for a draw
def check_for_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Function to place checker on the board
def place_checker(board, col, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False

# Function to convert column letter to index
def column_to_index(column):
    return ord(column.upper()) - ord('A')

# Main function to play the game
def play_game():
    board = initialize_board(ROWS, COLUMNS)
    current_player = random.choice(CHECKERS)  # Randomly select first player

    print_board(board)  # Initially print the board

    while True:
        print(f"Player {current_player}, please enter a column:")
        user_input = input().strip().upper()

        # Validate input
        if len(user_input) != 1 or not ('A' <= user_input <= chr(ord('A') + COLUMNS - 1)):
            print("Invalid input. Please enter a valid column.")
            continue

        col = column_to_index(user_input)

        # Place checker and check for validity
        if not place_checker(board, col, current_player):
            print("Column is full! You lose your turn.")
        else:
            print_board(board)

            # Check for win
            if check_for_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            
            # Check for draw
            if check_for_draw(board):
                print("The game is a draw!")
                break

            # Next player's turn
            current_player = CHECKERS[(CHECKERS.index(current_player) + 1) % MAX_PLAYERS]

# Run the game
if __name__ == "__main__":
    play_game()
