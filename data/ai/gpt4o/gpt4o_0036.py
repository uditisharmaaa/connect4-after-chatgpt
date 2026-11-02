import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Supports up to 5 players

def create_board():
    """Creates and returns a board initialized with spaces."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def get_first_player():
    """Randomly select the first player."""
    return random.randint(0, NUM_PLAYERS - 1)

def valid_input(input_str):
    """Check if the input is a valid column."""
    return input_str.isalpha() and len(input_str) == 1 and 'A' <= input_str <= chr(65 + COLUMNS - 1)

def column_not_full(board, column):
    """Check if a column is not full."""
    return board[0][column] == ' '

def place_checker(board, column, checker):
    """Places checker in the lowest available row of the given column."""
    for row in reversed(range(ROWS)):
        if board[row][column] == ' ':
            board[row][column] = checker
            return

def check_for_win(board, checker):
    """Check for a win in the board for the current checker."""
    # Horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Diagonal /
    for col in range(COLUMNS - 3):
        for row in range(3, ROWS):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    # Diagonal \
    for col in range(COLUMNS - 3):
        for row in range(ROWS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    return False

def board_full(board):
    """Check if the board is full."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def connect_4():
    """Main function to run the Connect 4 game."""
    board = create_board()
    current_player = get_first_player()
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        user_input = input().strip().upper()

        if not valid_input(user_input):
            print("Invalid input. Please enter a valid column letter.")
            continue

        column = ord(user_input) - 65  # Convert letter to index

        if not column_not_full(board, column):
            print("Column is full. Please choose another column.")
            continue

        place_checker(board, column, CHECKERS[current_player])
        print_board(board)

        if check_for_win(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break

        if board_full(board):
            print("It's a draw!")
            break

        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    connect_4()
