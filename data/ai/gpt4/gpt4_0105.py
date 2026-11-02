import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLUMNS)]

# Function to create and initialize the board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(COLUMN_LABELS))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Function to check for a win condition
def check_winner(board, symbol):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == symbol for i in range(4)):
                return True
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - 3):
        for col in range(3, COLUMNS):
            if all(board[row + i][col - i] == symbol for i in range(4)):
                return True
    return False

# Function to check for a draw
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Function to place a checker in the chosen column
def place_checker(board, col, symbol):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = symbol
            return True
    return False

# Function to validate player input
def validate_input(input_str, board):
    if len(input_str) != 1 or input_str not in COLUMN_LABELS:
        return False
    col = COLUMN_LABELS.index(input_str)
    return board[0][col] == " "

# Main game function
def connect4():
    # Initialize game variables
    board = create_board()
    num_players = 2  # Set number of players here (changeable up to MAX_PLAYERS)
    players = [PLAYER_SYMBOLS[i] for i in range(num_players)]
    current_player_idx = random.randint(0, num_players - 1)

    # Game loop
    while True:
        print_board(board)
        current_player = players[current_player_idx]
        print(f"Player {current_player}, it's your turn!")
        
        # Get valid input from player
        while True:
            player_input = input("Please enter a column (A-G): ").upper()
            if validate_input(player_input, board):
                col = COLUMN_LABELS.index(player_input)
                break
            else:
                print("Invalid input. Try again.")

        # Place checker and check for win/draw
        if place_checker(board, col, current_player):
            if check_winner(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            if check_draw(board):
                print_board(board)
                print("It's a draw!")
                break

            # Switch to the next player
            current_player_idx = (current_player_idx + 1) % num_players
        else:
            print("Column is full. You lose your turn.")

# Run the game
if __name__ == "__main__":
    connect4()
