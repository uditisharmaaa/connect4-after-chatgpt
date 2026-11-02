import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# Helper functions
def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """Creates a 2D list representing the game board."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the board to the terminal."""
    clear_screen()
    column_labels = "   ".join(chr(65 + i) for i in range(COLUMNS))
    print(f"  {column_labels}")
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column, board):
    """Checks if the entered column is valid and has space available."""
    if len(column) != 1 or not column.isalpha():
        return False
    column_index = ord(column.upper()) - 65
    if column_index < 0 or column_index >= COLUMNS:
        return False
    return board[0][column_index] == " "

def drop_checker(board, column, checker):
    """Drops the checker into the specified column."""
    column_index = ord(column.upper()) - 65
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = checker
            break

def check_winner(board, checker):
    """Checks whether the given checker has achieved a Connect 4."""
    # Check horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if all(cell == checker for cell in row[col:col + 4]):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Checks whether the game is a draw (board is full)."""
    return all(cell != " " for row in board for cell in row)

# Main function
def connect_four():
    """Main function to run the Connect 4 game."""
    # Initialize the game
    board = create_board(ROWS, COLUMNS)
    num_players = 2  # You can change this to a number between 2 and 5
    players = PLAYER_CHECKERS[:num_players]
    current_player = random.choice(players)

    print_board(board)
    print(f"Player {current_player} goes first!")

    # Game loop
    while True:
        print_board(board)
        column = input(f"Player {current_player}, please enter a column: ").strip().upper()

        # Validate the input
        if not is_valid_column(column, board):
            print("Invalid input. Please try again.")
            continue

        # Place the checker
        drop_checker(board, column, current_player)

        # Check for a winner
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        # Check for a draw
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_index = players.index(current_player)
        current_player = players[(current_index + 1) % num_players]

# Run the game
if __name__ == "__main__":
    connect_four()
