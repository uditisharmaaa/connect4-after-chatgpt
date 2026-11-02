import os
import random

# Constants for game settings
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create and return a board initialized with empty spaces."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    # Print column labels
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column):
    """Check if the column is within valid range and not full."""
    return 0 <= column < COLUMNS and board[0][column] == ' '

def place_checker(board, column, checker):
    """Place a checker in the chosen column."""
    for row in reversed(range(ROWS)):
        if board[row][column] == ' ':
            board[row][column] = checker
            return

def check_win(board, checker):
    """Check if the checker has won the game."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    # Check diagonal (bottom left to top right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    # Check diagonal (top left to bottom right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    """Check if the board is full, resulting in a draw."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# Initialize
board = create_board()
num_players = 2  # Set this for initial submission
player_checkers = PLAYERS[:num_players]
current_player_index = random.randint(0, num_players - 1)

# Main game loop
while True:
    print_board(board)
    current_player_checker = player_checkers[current_player_index]
    print(f"Player {current_player_checker}, please enter a column:")

    column_input = input().strip().upper()

    if len(column_input) == 1 and 'A' <= column_input <= chr(65 + COLUMNS - 1):
        column = ord(column_input) - 65
        if is_valid_column(column):
            place_checker(board, column, current_player_checker)

            if check_win(board, current_player_checker):
                print_board(board)
                print(f"Player {current_player_checker} won!")
                break

            if is_draw(board):
                print_board(board)
                print("The game is a draw!")
                break

            # Switch player
            current_player_index = (current_player_index + 1) % num_players
        else:
            print("Invalid column! The column is either full or out of range.")
    else:
        print("Invalid input! Please enter a valid column letter.")
