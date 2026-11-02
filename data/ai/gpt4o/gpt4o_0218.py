import os
import random

# Constants for board dimensions and number of players
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2

# Player checkers
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Initialize the board with whitespace
def initialize_board():
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

# Function to print the current state of the board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    # Print column labels
    print("  " + "   ".join([chr(ord('A') + i) for i in range(NUM_COLS)]))
    print("+---" * NUM_COLS + "+")

    # Print each row of the board
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * NUM_COLS + "+")

# Validate user input
def validate_input(input_value):
    return input_value.isalpha() and 'A' <= input_value < chr(ord('A') + NUM_COLS)

# Place the checker in the chosen column
def place_checker(board, col, checker):
    # Iterate from the bottom of the chosen column to find the first empty row
    for row in reversed(range(NUM_ROWS)):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False  # Column is full

# Check for win conditions
def check_win(board, checker):
    # Check horizontal
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

# Check for a draw condition
def check_draw(board):
    return all(all(cell != ' ' for cell in row) for row in board)

def main():
    board = initialize_board()
    print_board(board)
    
    # Choose a random starting player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        current_player_checker = CHECKERS[current_player_idx]
        print(f"Player {current_player_checker}, please enter a column:")
        user_input = input().strip().upper()

        while not validate_input(user_input):
            print("Invalid input! Please enter a valid column letter:")
            user_input = input().strip().upper()

        col = ord(user_input) - ord('A')
        
        if not place_checker(board, col, current_player_checker):
            print("Column full! You lose the turn.")
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        print_board(board)

        if check_win(board, current_player_checker):
            print(f"Player {current_player_checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
