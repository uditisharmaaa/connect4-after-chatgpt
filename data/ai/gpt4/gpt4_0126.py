```python
import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

# Create the board
def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

# Print the board
def print_board(board):
    os.system('clear')  # Clear the terminal
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))  # Column headers (A, B, C, etc.)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Check for a win
def check_win(board, player_checker):
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if all(row[col + i] == player_checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player_checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player_checker for i in range(4)):
                return True

    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - 3):
        for col in range(3, COLUMNS):
            if all(board[row + i][col - i] == player_checker for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Validate user input
def is_valid_input(user_input, columns, board):
    if len(user_input) != 1 or not user_input.isalpha():
        return False
    column_index = ord(user_input.upper()) - 65
    if column_index < 0 or column_index >= columns:
        return False
    if board[0][column_index] != " ":
        return False
    return True

# Place checker on board
def place_checker(board, column, player_checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = player_checker
            return

# Main game logic
def play_game():
    # Initialize the game
    board = create_board(ROWS, COLUMNS)
    players = random.sample(range(2), 2)  # Randomly pick 2 players
    turn = random.choice(players)  # Randomly select the first player
    num_players=int
### okay user tight adjust,
