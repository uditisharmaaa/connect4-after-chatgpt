import os
import random

# Constants for the game
ROWS = 6
COLS = 7
PLAYER_COUNT = 2
CHECKERS = ["X", "O", "V", "H", "M"]
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Initialize the board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(ALPHABET[:COLS]))  # Print column headers
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+\n")

# Validate player input
def is_valid_input(column_input, board):
    if len(column_input) != 1 or column_input not in ALPHABET[:COLS]:
        return False
    col = ALPHABET.index(column_input)
    return board[0][col] == " "  # Check if the column is not full

# Place the checker in the lowest available position in the column
def place_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):  # Start from the bottom row
        if board[row][col] == " ":
            board[row][col] = checker
            return

# Check for a win condition
def check_win(board, checker):
    # Check horizontal win
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical win
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

# Check for a draw (if the board is full)
def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

# Main game loop
def connect_4():
    # Initialize the board
    board = create_board()
    
    # Select players and assign checkers
    players = CHECKERS[:PLAYER_COUNT]
    
    # Randomly choose the starting player
    current_player_idx = random.randint(0, PLAYER_COUNT - 1)
    
    print_board(board)

    while True:
        # Get current player and checker
        current_player = players[current_player_idx]
        
        # Prompt input for the current player
        column_input = ""
        while True:
            column_input = input(f"Player {current_player}, please enter a column: ").upper()
            if is_valid_input(column_input, board):
                break
            else:
                print("Invalid input. Please try again.")

        # Place checker in the chosen column
        column_index = ALPHABET.index(column_input)
        place_checker(board, column_index, current_player)
        
        # Print updated board
        print_board(board)

        # Check for win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Move to the next player
        current_player_idx = (current_player_idx + 1) % PLAYER_COUNT

# Start the game
if __name__ == "__main__":
    connect_4()
