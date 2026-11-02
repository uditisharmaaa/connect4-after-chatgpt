import os
import random

# Constants for board dimensions and player symbols
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O']

def create_board():
    """Create a board with defined rows and columns."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the console (Linux/Unix)
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A-G
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def get_valid_column():
    """Get a valid column input from the player."""
    while True:
        col_input = input(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
        if len(col_input) == 1 and 'A' <= col_input <= chr(65 + COLS - 1):
            col_index = ord(col_input) - 65
            if board[0][col_index] == ' ':  # Check if the column is not full
                return col_index
            else:
                print("Column is full. Please choose another column.")
        else:
            print("Invalid input. Please choose a valid column.")

def place_checker(col_index):
    """Place the current player's checker in the chosen column."""
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = current_player
            return

def check_win():
    """Check if the current player has won."""
    # Check horizontal, vertical, and diagonal wins
    return (check_lines() or check_columns() or check_diagonals())

def check_lines():
    """Check for horizontal win."""
    for row in board:
        for col in range(COLS - 3):
            if all(cell == current_player for cell in row[col:col + 4]):
                return True
    return False

def check_columns():
    """Check for vertical win."""
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == current_player for i in range(4)):
                return True
    return False

def check_diagonals():
    """Check for diagonal win."""
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == current_player for i in range(4)):
                return True
        for col in range(3, COLS):
            if all(board[row + i][col - i] == current_player for i in range(4)):
                return True
    return False

def check_draw():
    """Check if the board is full and there is no winner."""
    return all(board[0][col] != ' ' for col in range(COLS))

# Main game loop
board = create_board()
current_player = random.choice(PLAYERS)
print_board(board)

while True:
    col_index = get_valid_column()
    place_checker(col_index)
    print_board(board)

    if check_win():
        print(f"Player {current_player} won!")
        break

    if check_draw():
        print("The game is a draw!")
        break

    # Switch players
    current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
