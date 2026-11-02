import os
import random

# Constants
COLS = 7
ROWS = 6
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def initialize_board(rows, cols):
    """Create and initialize the game board with empty spaces."""
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board, cols):
    """Display the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print board with separators
    for row in board:
        print("+---" * cols + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * cols + "+")


def get_valid_column(cols):
    """Get a valid column input from the player."""
    while True:
        user_input = input("Player {}, please enter a column: ".format(current_player_checker))
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is uppercase letter
        if not user_input.isupper():
            print("Invalid input. Please enter an uppercase letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column is within bounds
        if col_index < 0 or col_index >= cols:
            print(f"Invalid input. Please enter a letter between A and {chr(65 + cols - 1)}.")
            continue
        
        return col_index


def place_checker(board, col, checker, rows, cols):
    """Place a checker in the specified column. Return True if successful, False otherwise."""
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    print("Column is full. Please choose another column.")
    return False


def check_win(board, rows, cols, checker):
    """Check if the specified checker has won the game."""
    
    # Check horizontal
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_draw(board, rows, cols):
    """Check if the board is full (draw condition)."""
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == " ":
                return False
    return True


def play_game(rows, cols, num_players):
    """Main game loop."""
    global current_player_checker
    
    board = initialize_board(rows, cols)
    player_checkers = CHECKERS[:num_players]
    
    # Randomly select starting player
    current_player_index = random.randint(0, num_players - 1)
    
    print_board(board, cols)
    
    # Game loop
    while True:
        current_player_checker = player_checkers[current_player_index]
        
        # Get valid column from player
        valid_placement = False
        while not valid_placement:
            col = get_valid_column(cols)
            valid_placement = place_checker(board, col, current_player_checker, rows, cols)
        
        print_board(board, cols)
        
        # Check for win
        if check_win(board, rows, cols, current_player_checker):
            print(f"Player {current_player_checker} won!")
            break
        
        # Check for draw
        if check_draw(board, rows, cols):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % num_players


# Global variable to track current player checker
current_player_checker = ""


def main():
    """Main function to start the game."""
    play_game(ROWS, COLS, PLAYERS)


if __name__ == "__main__":
    main()
