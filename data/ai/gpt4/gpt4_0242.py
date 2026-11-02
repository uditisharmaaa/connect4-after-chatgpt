import os
import random

# Constants for game configuration
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# Function to initialize the board
def initialize_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    col_labels = "   ".join(chr(65 + i) for i in range(COLS))  # Column letters A-G
    print("  " + col_labels)
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

# Function to check for a win
def check_win(board, player):
    # Check horizontal, vertical, and diagonal directions
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for row in range(ROWS):
        for col in range(COLS):
            for dr, dc in directions:
                if all(0 <= row + dr * i < ROWS and 0 <= col + dc * i < COLS and 
                       board[row + dr * i][col + dc * i] == player for i in range(4)):
                    return True
    return False

# Function to check for a draw
def check_draw(board):
    # If all cells are filled, it's a draw
    return all(board[0][col] != " " for col in range(COLS))

# Function to place a checker in the specified column
def place_checker(board, col, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player
            return row, col
    return None, None

# Function to validate user input
def validate_input(input_str, board):
    if len(input_str) != 1 or not input_str.isalpha() or not input_str.isupper():
        return False
    col = ord(input_str) - 65
    return 0 <= col < COLS and board[0][col] == " "

# Main function to run the game
def main():
    # Game setup
    board = initialize_board(ROWS, COLS)
    num_players = 2  # Fixed to 2 players for this assignment
    players = PLAYER_SYMBOLS[:num_players]
    random.shuffle(players)
    current_player_index = 0

    # Print initial board
    print_board(board)

    # Game loop
    while True:
        current_player = players[current_player_index]
        print(f"Player {current_player}, please enter a column:")
        
        # Input handling
        while True:
            user_input = input().strip()
            if validate_input(user_input, board):
                col = ord(user_input) - 65
                break
            print("Invalid input. Please enter a valid column (A-G).")

        # Place the checker
        row, col = place_checker(board, col, current_player)
        print_board(board)

        # Check for win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % num_players

# Run the game
if __name__ == "__main__":
    main()
