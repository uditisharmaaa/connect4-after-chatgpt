import os
import random

# Constants for game configuration
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]  # List of possible checkers for players
NUM_PLAYERS = 2  # Number of players in the game, must be <= MAX_PLAYERS

# Function to clear the terminal screen
def clear_screen():
    os.system('clear')

# Function to create and initialize the board
def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

# Function to print the game board
def print_board(board):
    clear_screen()
    # Print column labels
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))
    print("+---" * len(board[0]) + "+")
    # Print rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# Function to validate user input for column selection
def is_valid_column(input_col, columns):
    return input_col.isalpha() and len(input_col) == 1 and 65 <= ord(input_col.upper()) < 65 + columns

# Function to get the lowest available row in a column
def get_available_row(board, column):
    for row in range(len(board) - 1, -1, -1):
        if board[row][column] == " ":
            return row
    return None

# Function to check for a win condition
def check_winner(board, player_checker):
    # Check horizontal win
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player_checker for i in range(4)):
                return True

    # Check vertical win
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player_checker for i in range(4)):
                return True

    # Check diagonal win (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player_checker for i in range(4)):
                return True

    # Check diagonal win (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player_checker for i in range(4)):
                return True

    return False

# Function to check if the board is full (draw)
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

# Main function for gameplay
def play_connect4():
    # Initialize the board
    board = create_board(ROWS, COLUMNS)
    
    # Randomly select the first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    # Game loop
    while True:
        print_board(board)
        
        current_player_checker = PLAYER_CHECKERS[current_player_idx]
        print(f"Player {current_player_checker}, it's your turn!")
        
        # Get input from the current player
        column = None
        while True:
            user_input = input("Please enter a column (A-G): ").upper()
            if not is_valid_column(user_input, COLUMNS):
                print("Invalid input. Please enter a valid column letter.")
                continue
            
            column = ord(user_input) - 65  # Convert letter to index
            available_row = get_available_row(board, column)
            
            if available_row is not None:
                break
            else:
                print("Column is full. Choose another column.")
        
        # Place the checker in the first available row in the selected column
        board[available_row][column] = current_player_checker
        
        # Check for a win
        if check_winner(board, current_player_checker):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            break
        
        # Check for a draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

# Start the game
if __name__ == "__main__":
    play_connect4()
