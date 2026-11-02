import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Checker symbols for up to 5 players
COLUMN_LETTERS = [chr(65 + i) for i in range(COLUMNS)]  # ["A", "B", ..., "G"]

# Function to create the board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clears the screen
    print("  " + "   ".join(COLUMN_LETTERS[:COLUMNS]))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Function to drop a checker in a column
def drop_checker(board, column, checker):
    for row in reversed(board):  # Start from the bottom row
        if row[column] == " ":
            row[column] = checker
            return True
    return False  # Column is full

# Function to check for a win condition (4 in a row)
def check_win(board, checker):
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if all(row[col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

# Function to check if the board is full (draw)
def is_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main game function
def play_connect4():
    # Initialization
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    current_player_idx = random.randint(0, PLAYERS - 1)  # Randomly select the first player
    print_board(board)

    while True:
        current_player = players[current_player_idx]
        print(f"Player {current_player}, please enter a column:")
        user_input = input().upper()

        # Validate input
        if user_input not in COLUMN_LETTERS[:COLUMNS]:
            print("Invalid column. Please try again.")
            continue

        column_index = COLUMN_LETTERS.index(user_input)
        if not drop_checker(board, column_index, current_player):
            print("Column is full. Please try again.")
            continue

        # Print updated board
        print_board(board)

        # Check for win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch player
        current_player_idx = (current_player_idx + 1) % PLAYERS

# Run the game
if __name__ == "__main__":
    play_connect4()
