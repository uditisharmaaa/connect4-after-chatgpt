import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
INITIAL_PLAYER = random.randint(0, PLAYERS - 1)  # Choose a random first player

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Creates and initializes the two-dimensional game board."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the game board."""
    clear_screen()
    # Print column headers
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def get_column_input():
    """Prompts the current player to enter a column."""
    while True:
        column = input(f"Player {CHECKERS[current_player]}, please enter a column: ").upper()
        if column in [chr(i) for i in range(65, 65 + COLUMNS)]:
            return ord(column) - 65
        else:
            print("Invalid input. Please enter a valid column.")

def place_checker(board, col, checker):
    """Places a checker in the specified column."""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False

def check_win(board, checker):
    """Checks for a win condition (4 in a row vertically, horizontally, or diagonally)."""
    # Check horizontal, vertical, and diagonal win conditions
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (
                col <= COLUMNS - 4 and all(board[row][col + i] == checker for i in range(4)) or
                row <= ROWS - 4 and all(board[row + i][col] == checker for i in range(4)) or
                row <= ROWS - 4 and col <= COLUMNS - 4 and all(board[row + i][col + i] == checker for i in range(4)) or
                row >= 3 and col <= COLUMNS - 4 and all(board[row - i][col + i] == checker for i in range(4))
            ):
                return True
    return False

def check_draw(board):
    """Checks if the game is a draw (no empty cells left)."""
    return all(cell != ' ' for row in board for cell in row)

# Create and print initial board
board = create_board()
print_board(board)

# Set the initial current player
current_player = INITIAL_PLAYER

# Game loop
while True:
    # Get valid column input from the current player
    selected_column = get_column_input()

    # Attempt to place the checker in the selected column
    if place_checker(board, selected_column, CHECKERS[current_player]):
        print_board(board)

        # Check for win or draw conditions
        if check_win(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        elif check_draw(board):
            print("Game is a draw!")
            break

        # Change turn
        current_player = (current_player + 1) % PLAYERS
    else:
        print("Column is full. Turn is lost. Next player's turn.")
