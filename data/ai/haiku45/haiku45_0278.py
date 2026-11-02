import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Checkers for each player
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Create and initialize the game board with empty spaces."""
    board = []
    for row in range(ROWS):
        board.append([" " for col in range(COLS)])
    return board


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(chr(65 + col), end="   ")
    print()
    
    # Print board with borders
    for row in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    print("+---" * COLS + "+")


def get_column_input(player_checker):
    """Get and validate column input from the player."""
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ")
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert to uppercase
        user_input = user_input.upper()
        
        # Check if letter is within valid range
        col_index = ord(user_input) - ord('A')
        if col_index < 0 or col_index >= COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(65 + COLS - 1)}.")
            continue
        
        return col_index


def place_checker(board, col, player_checker):
    """Place a checker in the specified column. Returns True if successful."""
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_checker
            return True
    
    # Column is full
    print("This column is full. Please choose another column.")
    return False


def check_win(board, player_checker):
    """Check if the player has won the game."""
    
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLS):
            if all(board[row + i][col - i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_draw(board):
    """Check if the board is full (draw)."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True


def main():
    """Main game loop."""
    # Initialize the board
    board = initialize_board()
    
    # Get the list of player checkers
    players = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    
    # Game loop
    while True:
        current_player_checker = players[current_player_index]
        
        # Get valid input and place checker
        while True:
            col = get_column_input(current_player_checker)
            if place_checker(board, col, current_player_checker):
                break
        
        # Print the board
        print_board(board)
        
        # Check for win
        if check_win(board, current_player_checker):
            print(f"Player {current_player_checker} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
