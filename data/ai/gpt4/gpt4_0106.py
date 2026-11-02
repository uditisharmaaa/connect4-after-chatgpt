import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2  # Change this to 3, 4, or 5 for more players
CHECKERS = ["X", "O", "V", "H", "M"]  # Checkers for up to 5 players

# Create the board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Check if input is valid
def is_valid_column(input_char, board):
    if len(input_char) != 1 or not input_char.isalpha() or ord(input_char) < 65 or ord(input_char) >= 65 + COLUMNS:
        return False
    column = ord(input_char) - 65
    if column < 0 or column >= COLUMNS or board[0][column] != " ":
        return False
    return True

# Drop a checker in the column
def drop_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False  # Shouldn't reach here since we validate the column beforehand

# Check for a win
def check_win(board, checker):
    # Check horizontal win
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col] == row[col + 1] == row[col + 2] == row[col + 3] == checker:
                return True

    # Check vertical win
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] == checker:
                return True

    # Check diagonal win (/ direction)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] == checker:
                return True

    # Check diagonal win (\ direction)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == checker:
                return True

    return False

# Check if the board is full
def is_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

# Main game loop
def connect_4():
    # Initialize the board
    board = create_board()
    # Randomly select the starting player
    current_player_index = random.randint(0, PLAYERS - 1)
    players = [CHECKERS[i] for i in range(PLAYERS)]

    print_board(board)

    while True:
        # Current player
        current_player = players[current_player_index]
        print(f"Player {current_player}, please enter a column:")

        # Get valid input
        while True:
            user_input = input().strip().upper()
            if is_valid_column(user_input, board):
                break
            print("Invalid input. Please enter a valid column:")

        column = ord(user_input) - 65
        drop_checker(board, column, current_player)

        print_board(board)

        # Check for win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Move to the next player
        current_player_index = (current_player_index + 1) % PLAYERS

# Run the game
if __name__ == "__main__":
    connect_4()
