import os
import random

# Constants for the game
ROWS = 6         # Number of rows
COLS = 7         # Number of columns
PLAYERS = 2      # Number of players
CHECKERS = ["X", "O", "V", "H", "M"]  # Checkers for players

# Function to clear screen
def clear_screen():
    os.system('clear')

# Create the game board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the game board
def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(chr(ord('A') + c) for c in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

# Validate column input
def validate_column(col, board):
    if len(col) != 1 or not ('A' <= col <= chr(ord('A') + COLS - 1)):
        return False
    col_index = ord(col) - ord('A')
    return board[0][col_index] == " "  # Check if column is not full

# Place the checker on the board
def place_checker(col, board, checker):
    col_index = ord(col) - ord('A')
    for row in range(ROWS - 1, -1, -1):  # Start from the bottom
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            break

# Check for a win
def check_win(board, checker):
    # Check horizontal win
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertical win
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

# Check for a draw
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

# Main game loop
def play_game():
    # Initialize game variables
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)  # Choose random start player
    player_checkers = CHECKERS[:PLAYERS]  # Get checkers for the number of players
    game_over = False

    # Print initial board
    print_board(board)
    print(f"Player {player_checkers[current_player]} starts!")

    while not game_over:
        # Ask current player for a column
        print(f"Player {player_checkers[current_player]}, please enter a column:")
        col = input().strip().upper()

        # Validate input
        if not validate_column(col, board):
            print("Invalid input. Please try again.")
            continue

        # Place checker
        place_checker(col, board, player_checkers[current_player])

        # Print updated board
        print_board(board)

        # Check for a win
        if check_win(board, player_checkers[current_player]):
            print(f"Player {player_checkers[current_player]} won!")
            game_over = True
            continue

        # Check for a draw
        if check_draw(board):
            print("The game is a draw!")
            game_over = True
            continue

        # Switch players
        current_player = (current_player + 1) % PLAYERS

# Run the game
if __name__ == "__main__":
    play_game()
