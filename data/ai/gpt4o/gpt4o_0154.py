import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Extendable to more players

def initialize_board(rows, columns):
    """Creates an empty game board."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Clears the screen and prints the game board."""
    os.system('clear')  # Clears the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))  # Column labels A to G
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def get_valid_column_input():
    """Get a valid column letter input from the player."""
    while True:
        choice = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip().upper()
        if len(choice) == 1 and 'A' <= choice <= chr(64 + COLUMNS):
            column = ord(choice) - 65
            if board[0][column] == ' ':
                return column
            else:
                print("Column is full. Choose another column.")
        else:
            print("Invalid input. Please enter a valid column letter.")

def place_checker(board, column, checker):
    """Places a checker in the selected column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            break

def check_for_win(board, checker):
    """Check all win conditions: horizontal, vertical, diagonal."""
    # Check horizontal win
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col:col + 4] == [checker] * 4:
                return True
    
    # Check vertical win
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonal win (bottom left to top right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal win (top left to bottom right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True
    
    return False

def check_for_draw(board):
    """Check if the board is completely filled."""
    return all(cell != ' ' for row in board for cell in row)

# Initialize board and select random starting player
board = initialize_board(ROWS, COLUMNS)
current_player = random.randint(0, PLAYERS - 1)

# Game loop
while True:
    print_board(board)
    column = get_valid_column_input()
    place_checker(board, column, CHECKERS[current_player])

    if check_for_win(board, CHECKERS[current_player]):
        print_board(board)
        print(f"Player {CHECKERS[current_player]} won!")
        break
    elif check_for_draw(board):
        print_board(board)
        print("The game is a draw!")
        break

    # Switch to the next player
    current_player = (current_player + 1) % PLAYERS
