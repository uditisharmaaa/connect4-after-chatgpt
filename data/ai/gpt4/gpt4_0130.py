import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# Functions
def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """Creates an empty board with the given dimensions."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the current state of the board."""
    clear_screen()

    # Print column labels
    column_labels = "   ".join([chr(65 + col) for col in range(len(board[0]))])
    print(f"  {column_labels}")
    print("+---" * len(board[0]) + "+")

    # Print rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(column, board):
    """Checks if the chosen column is valid."""
    if column < 0 or column >= len(board[0]) or board[0][column] != " ":
        return False
    return True

def drop_checker(board, column, symbol):
    """Drops a checker into the specified column."""
    for row in range(len(board) - 1, -1, -1):  # Start from the bottom row
        if board[row][column] == " ":
            board[row][column] = symbol
            return row, column

def check_winner(board, symbol):
    """Checks if the given symbol has 4 in a row (horizontally, vertically, or diagonally)."""
    rows, columns = len(board), len(board[0])

    # Check horizontal
    for row in range(rows):
        for col in range(columns - 3):
            if all(board[row][col + i] == symbol for i in range(4)):
                return True

    # Check vertical
    for col in range(columns):
        for row in range(rows - 3):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(rows - 3):
        for col in range(columns - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, rows):
        for col in range(columns - 3):
            if all(board[row - i][col + i] == symbol for i in range(4)):
                return True

    return False

def is_draw(board):
    """Checks if the board is completely filled without a winner."""
    return all(board[0][col] != " " for col in range(len(board[0])))

def get_column_input(board, current_player):
    """Prompts the current player for a column input and validates it."""
    while True:
        try:
            column_letter = input(f"Player {current_player}, please enter a column: ").strip().upper()
            column = ord(column_letter) - 65  # Convert letter to column index

            if is_valid_column(column, board):
                return column
            else:
                print("Invalid column. Please try again.")
        except (ValueError, IndexError):
            print("Invalid input. Please try again.")

# Main game function
def connect_4():
    """Runs the Connect 4 game."""
    # Initialize game settings
    board = create_board(ROWS, COLUMNS)
    num_players = 2  # Fixed to 2 for the assignment
    players = PLAYER_SYMBOLS[:num_players]

    # Randomly select the first player
    current_player_index = random.randint(0, num_players - 1)
    current_player = players[current_player_index]

    # Game loop
    print_board(board)
    while True:
        # Get and validate input
        column = get_column_input(board, current_player)

        # Drop the checker
        drop_checker(board, column, current_player)

        # Print updated board
        print_board(board)

        # Check for a win
        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for a draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % num_players
        current_player = players[current_player_index]

# Start the game
if __name__ == "__main__":
    connect_4()
