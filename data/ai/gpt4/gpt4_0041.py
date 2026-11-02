import random
import os

# Constants for board dimensions and player count
ROWS = 6
COLUMNS = 7
PLAYERS = 2

# Checkers for players
CHECKERS = ["X", "O", "V", "H", "M"]

# Function to initialize the game board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Function to print the game board
def print_board(board):
    os.system('clear')
    print("  ", end="")
    for i in range(COLUMNS):
        print(f"{chr(65 + i)}   ", end="")
    print()
    for row in board:
        print("+---" * COLUMNS + "+")
        for cell in row:
            print(f"| {cell} ", end="")
        print("|")
    print("+---" * COLUMNS + "+")

# Function to check for valid input
def is_valid_input(column):
    return len(column) == 1 and column.isalpha() and "A" <= column < chr(65 + COLUMNS)

# Function to drop checker in the specified column
def drop_checker(board, column, checker):
    col_idx = ord(column.upper()) - 65
    for row in reversed(board):  # Start from bottom of the column
        if row[col_idx] == " ":
            row[col_idx] = checker
            return True
    return False

# Function to check for a win
def check_winner(board, checker):
    for row in range(ROWS):
        for col in range(COLUMNS):
            if col + 3 < COLUMNS and all([board[row][col + i] == checker for i in range(4)]):  # Horizontal
                return True
            if row + 3 < ROWS and all([board[row + i][col] == checker for i in range(4)]):  # Vertical
                return True
            if col + 3 < COLUMNS and row + 3 < ROWS and all([board[row + i][col + i] == checker for i in range(4)]):  # Diagonal /
                return True
            if col - 3 >= 0 and row + 3 < ROWS and all([board[row + i][col - i] == checker for i in range(4)]):  # Diagonal \
                return True
    return False

# Function to check if the board is full (draw)
def is_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main game function
def play_game():
    # Initialize the board
    board = create_board()

    # Randomly choose starting player
    current_player = random.randint(0, PLAYERS - 1)
    
    # Players' checkers
    player_checkers = CHECKERS[:PLAYERS]

    # Game loop
    while True:
        print_board(board)
        print(f"Player {player_checkers[current_player]}'s turn.")
        column = input("Enter a column: ").strip().upper()

        if not is_valid_input(column):  # Validate input
            print("Invalid input. Please enter a valid column (A-G).")
            continue

        if not drop_checker(board, column, player_checkers[current_player]):  # Place checker
            print("Column is full. Please choose another column.")
            continue

        if check_winner(board, player_checkers[current_player]):  # Check for a win
            print_board(board)
            print(f"Player {player_checkers[current_player]} won!")
            break

        if is_draw(board):  # Check for a draw
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % PLAYERS

# Run the game
if __name__ == "__main__":
    play_game()
