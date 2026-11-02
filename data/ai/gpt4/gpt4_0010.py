import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]  # Checkers per player
NUM_PLAYERS = 2  # Number of players for this game, can be set to any value up to MAX_PLAYERS

# Function to clear the console screen
def clear_screen():
    os.system('clear')  # For Linux/Unix systems

# Function to create the board
def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

# Function to print the board
def print_board(board):
    clear_screen()
    # Print column headers (A, B, C, ...)
    column_headers = "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(f"  {column_headers}")
    print("+---" * len(board[0]) + "+")

    # Print rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Check if a column input is valid
def is_valid_column(input_col, board):
    if len(input_col) != 1 or not input_col.isalpha():  # Ensure single letter input
        return False
    col_idx = ord(input_col.upper()) - 65
    if col_idx < 0 or col_idx >= len(board[0]):  # Ensure within board bounds
        return False
    if board[0][col_idx] != " ":  # Ensure column is not full
        return False
    return True

# Place a checker in the correct position
def place_checker(board, col, checker):
    col_idx = ord(col.upper()) - 65
    for row in reversed(board):  # Start from the bottom of the column
        if row[col_idx] == " ":
            row[col_idx] = checker
            return

# Check for a win (horizontal, vertical, diagonal)
def check_winner(board, checker):
    rows, cols = len(board), len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if board[r][c:c+4] == [checker, checker, checker, checker]:
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True

    # Check diagonal (\ direction)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True

    # Check diagonal (/ direction)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main function to run the game
def play_game():
    # Initialize the board and start the game
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player = random.randint(0, NUM_PLAYERS - 1)  # Randomly select starting player

    while True:
        print_board(board)
        print(f"Player {players[current_player]}'s turn!")

        # Get player input
        while True:
            column = input("Please enter a column: ").strip()
            if is_valid_column(column, board):
                break
            print(f"Invalid input. Please select a valid column.")

        # Place checker and check game state
        place_checker(board, column, players[current_player])

        # Check for win
        if check_winner(board, players[current_player]):
            print_board(board)
            print(f"Player {players[current_player]} won!")
            break

        # Check for draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
