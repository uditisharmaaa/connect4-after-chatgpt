import os
import random

# Game Constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """Initialize the game board with empty spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board, cols):
    """Print the game board to the console."""
    os.system('clear')
    
    # Print column headers
    header = "  "
    for col in range(cols):
        header += chr(ord('A') + col) + "   "
    print(header)
    
    # Print board with borders
    for row in board:
        # Top border of row
        print("+---" * cols + "+")
        # Row content
        row_str = "|"
        for cell in row:
            row_str += " " + cell + " |"
        print(row_str)
    
    # Bottom border
    print("+---" * cols + "+")


def get_valid_input(cols):
    """Get and validate user input for column selection."""
    while True:
        user_input = input().strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print(f"Invalid input. Please enter a single letter (A-{chr(ord('A') + cols - 1)}):")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print(f"Invalid input. Please enter a letter (A-{chr(ord('A') + cols - 1)}):")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column is within bounds
        if col_index < 0 or col_index >= cols:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + cols - 1)}:")
            continue
        
        return col_index


def place_checker(board, col, checker, rows, cols):
    """Place a checker in the specified column. Returns True if successful, False otherwise."""
    # Find the lowest available row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    return False


def check_win(board, rows, cols, checker):
    """Check if the specified checker has won."""
    # Check horizontal
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
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


def play_game():
    """Main game loop."""
    # Initialize the board
    board = initialize_board(ROWS, COLS)
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    checker_symbols = CHECKERS[:NUM_PLAYERS]
    
    # Print initial board
    print_board(board, COLS)
    print(f"Player {checker_symbols[current_player]}, please enter a column:")
    
    # Game loop
    while True:
        # Get valid column input from player
        col = get_valid_input(COLS)
        
        # Try to place checker
        if place_checker(board, col, checker_symbols[current_player], ROWS, COLS):
            # Print updated board
            print_board(board, COLS)
            
            # Check for win
            if check_win(board, ROWS, COLS, checker_symbols[current_player]):
                print(f"Player {checker_symbols[current_player]} won!")
                break
            
            # Check for draw
            if check_draw(board, ROWS, COLS):
                print("It's a draw!")
                break
            
            # Move to next player
            current_player = (current_player + 1) % NUM_PLAYERS
            print(f"Player {checker_symbols[current_player]}, please enter a column:")
        else:
            # Column is full, ask for another input
            print(f"Column is full. Player {checker_symbols[current_player]}, please enter a column:")


if __name__ == "__main__":
    play_game()
