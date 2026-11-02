import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O"]  # Players' checkers

# Create an empty board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A, B, C, ...
    print("+" + "---+" * COLS)  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Row content
        print("+" + "---+" * COLS)  # Row border

# Check for a win
def check_win(board, player):
    # Check horizontal, vertical, and diagonal win conditions
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player:
                # Check horizontally
                if c + 3 < COLS and all(board[r][c + i] == player for i in range(4)):
                    return True
                # Check vertically
                if r + 3 < ROWS and all(board[r + i][c] == player for i in range(4)):
                    return True
                # Check diagonal \
                if r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == player for i in range(4)):
                    return True
                # Check diagonal /
                if r - 3 >= 0 and c + 3 < COLS and all(board[r - i][c + i] == player for i in range(4)):
                    return True
    return False

# Check for a draw
def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))

# Place a checker in the selected column
def place_checker(board, column, player):
    for r in range(ROWS - 1, -1, -1):  # Start from the bottom row
        if board[r][column] == " ":
            board[r][column] = player
            return True
    return False

# Get a valid column input from the user
def get_column_input():
    while True:
        column_input = input(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
        if len(column_input) == 1 and 'A' <= column_input <= chr(65 + COLS - 1):
            column = ord(column_input) - 65
            return column
        print("Invalid input. Please try again.")

# Main game loop
if __name__ == "__main__":
    board = create_board()
    current_player = random.choice(PLAYERS)  # Randomly select first player

    while True:
        print_board(board)
        column = get_column_input()

        if not place_checker(board, column, current_player):
            print("Column is full! Please choose another column.")
            continue

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
