import os
import random

# Constants for board dimensions and players
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']  # Checkers for 2 players

# Function to create and initialize the board
def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clear the console (Linux/Unix terminal)
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels
    print("+" + "---+" * COLS)  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Row contents
        print("+" + "---+" * COLS)  # Row border

# Function to place checker in the board
def place_checker(board, column, checker):
    for row in reversed(board):  # Start from the bottom of the column
        if row[column] == ' ':
            row[column] = checker
            return True
    return False  # Column is full

# Function to check for a win (horizontally, vertically, diagonally)
def check_win(board, checker):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):  # Only check till col 3 to avoid out of bounds
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):  # Only check till row 3 to avoid out of bounds
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

# Function to check for a draw
def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

# Main game loop
def main():
    board = create_board()  # Initialize the board
    current_player_index = random.randint(0, len(PLAYERS) - 1)  # Randomly select first player
    turns = 0  # Track number of turns

    while True:
        print_board(board)  # Display the current board
        current_player = PLAYERS[current_player_index]  # Get current player's checker

        # Input validation loop
        while True:
            column_input = input(f"Player {current_player}, please enter a column (A-G): ").strip().upper()
            if len(column_input) == 1 and 'A' <= column_input <= 'G':
                column = ord(column_input) - 65  # Convert letter to column index
                if place_checker(board, column, current_player):
                    break  # Valid placement, exit loop
                else:
                    print("Column is full, please choose another column.")
            else:
                print("Invalid input. Please enter a letter from A to G.")

        # Check for win
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Alternate players
        current_player_index = (current_player_index + 1) % len(PLAYERS)
        turns += 1

if __name__ == "__main__":
    main()
