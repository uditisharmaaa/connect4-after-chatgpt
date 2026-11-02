import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize the board with empty spaces
def initialize_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    # Print column headers (A, B, C, ...)
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    # Print the board rows
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

# Check if a column is valid for placing a checker
def is_valid_column(column, board):
    col_index = ord(column) - 65
    return 0 <= col_index < COLS and board[0][col_index] == " "

# Place the checker in the chosen column
def place_checker(column, checker, board):
    col_index = ord(column) - 65
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            break

# Check for a win in all directions
def check_winner(board, checker):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col+i] == checker for i in range(4)):
                return True
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == checker for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row+i][col+i] == checker for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row-i][col+i] == checker for i in range(4)):
                return True
    return False

# Check for a draw
def check_draw(board):
    return all(row[0] != " " for row in board)

# Main game function
def play_game():
    # Initialize the board
    board = initialize_board()
    # Set players and their checkers
    player_count = 2  # For this assignment, we use 2 players only
    players = CHECKERS[:player_count]
    # Randomly select the first player
    current_player = random.randint(0, player_count - 1)
    # Game loop
    while True:
        print_board(board)
        print(f"Player {players[current_player]}, please enter a column:")
        column = input("> ").strip().upper()
        # Validate input
        if len(column) != 1 or not column.isalpha() or not is_valid_column(column, board):
            print("Invalid input. Please try again.")
            continue
        # Place the checker
        place_checker(column, players[current_player], board)
        # Check if the current player wins
        if check_winner(board, players[current_player]):
            print_board(board)
            print(f"Player {players[current_player]} won!")
            break
        # Check for a draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        # Switch to the next player
        current_player = (current_player + 1) % player_count

# Run the game
if __name__ == "__main__":
    play_game()
