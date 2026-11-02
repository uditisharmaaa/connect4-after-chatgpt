import os
import random

# Constants
ROWS = 6  # Number of rows
COLUMNS = 7  # Number of columns
PLAYERS = 2  # Number of players (between 2 and 5)
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]  # Player checkers

# Function to create the game board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))  # Column letters
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Function to check if the player's move results in a win
def check_win(board, row, col, checker):
    # Directions: vertical, horizontal, diagonals
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1  # Count the current checker
        for direction in [1, -1]:  # Look in both directions
            r, c = row + dr * direction, col + dc * direction
            while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
                count += 1
                r += dr * direction
                c += dc * direction
        if count >= 4:  # Win condition
            return True
    return False

# Function to check if the board is full (draw)
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Function to validate user input
def get_valid_column(board, player):
    while True:
        column = input(f"Player {CHECKERS[player]}, please enter a column: ").strip().upper()
        
        # Validate input (must match column letters)
        if len(column) != 1 or not ('A' <= column <= chr(65 + COLUMNS - 1)):
            print("Invalid input! Please select a valid column.")
            continue
        
        col_idx = ord(column) - 65
        # Check if the column is full
        if board[0][col_idx] != " ":
            print("Column is full! Please select a different column.")
            continue
        
        return col_idx

# Function to drop a checker in the board
def drop_checker(board, col, checker):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row  # Return the row where the checker was placed

# Main function to run the game
def connect_4():
    # Initialize the board
    board = create_board()
    # Randomly select the starting player
    current_player = random.randint(0, PLAYERS - 1)
    
    # Start the game
    print_board(board)
    
    while True:
        # Get a valid column from the current player
        col = get_valid_column(board, current_player)
        # Drop the checker in the selected column
        row = drop_checker(board, col, CHECKERS[current_player])
        
        # Update the board and print it
        print_board(board)
        
        # Check for a win
        if check_win(board, row, col, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        # Check for a draw
        if check_draw(board):
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player = (current_player + 1) % PLAYERS

# Entry point
if __name__ == "__main__":
    connect_4()
