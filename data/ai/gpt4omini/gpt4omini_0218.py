import os
import random

# Constants for board dimensions and players
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

# Function to create the game board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Function to print the board
def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column headers
    print("+" + "---+" * COLS)  # Top border
    for row in board:  # Print each row of the board
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)  # Row border

# Function to check for a win
def check_win(board, player):
    # Check horizontal, vertical, and diagonal connections
    for r in range(ROWS):
        for c in range(COLS):
            if c <= COLS - 4 and all(board[r][c + i] == player for i in range(4)):
                return True  # Horizontal check
            if r <= ROWS - 4 and all(board[r + i][c] == player for i in range(4)):
                return True  # Vertical check
            if r <= ROWS - 4 and c <= COLS - 4 and all(board[r + i][c + i] == player for i in range(4)):
                return True  # Diagonal down-right check
            if r >= 3 and c <= COLS - 4 and all(board[r - i][c + i] == player for i in range(4)):
                return True  # Diagonal up-right check
    return False

# Function to check for a draw
def check_draw(board):
    return all(board[0][c] != " " for c in range(COLS))  # If the top row is full

# Function to place a checker and return the row index
def place_checker(board, column, player):
    for r in reversed(range(ROWS)):  # Check from bottom to top
        if board[r][column] == " ":
            board[r][column] = player  # Place the checker
            return r
    return -1  # Column is full

# Main function to start and manage the game
def main():
    board = create_board()  # Initialize the game board
    current_player_index = random.randint(0, len(PLAYERS) - 1)  # Randomly choose first player
    num_players = len(PLAYERS)
    
    while True:
        print_board(board)  # Print the current state of the board
        current_player = PLAYERS[current_player_index]
        column_input = input(f"Player {current_player}, please enter a column (A-G): ").strip().upper()

        # Input validation for column selection
        if len(column_input) != 1 or column_input < 'A' or column_input >= chr(65 + COLS):
            print("Invalid column. Please select a valid column (A-G).")
            continue
        
        column = ord(column_input) - 65  # Convert column character to index
        
        if place_checker(board, column, current_player) == -1:
            print("Column is full. Please choose another column.")
            continue
        
        # Check for win or draw after placing the checker
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player_index = (current_player_index + 1) % num_players

# Run the main function to start the game
if __name__ == "__main__":
    main()
