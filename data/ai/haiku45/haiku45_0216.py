import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Valid checkers for up to 5 players
CHECKERS = ['X', 'O', 'V', 'H', 'M']


def initialize_board(rows, cols):
    """Initialize the board with empty spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board, cols):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print board with borders
    for row in board:
        # Top border
        print("+---" * cols + "+")
        # Cell content
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    
    # Bottom border
    print("+---" * cols + "+")


def get_valid_input(cols):
    """Get and validate player input for column selection."""
    while True:
        user_input = input().strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Check if the letter corresponds to a valid column
        col_index = ord(user_input) - ord('A')
        if col_index < 0 or col_index >= cols:
            print(f"Invalid column. Please enter a letter between A and {chr(65 + cols - 1)}.")
            continue
        
        return col_index


def place_checker(board, col, checker, rows, cols):
    """Place a checker in the specified column. Return True if successful, False otherwise."""
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    
    # Column is full
    print("This column is full. Please choose another column.")
    return False


def check_win(board, rows, cols, checker):
    """Check if the specified checker has won."""
    
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


def is_board_full(board, rows, cols):
    """Check if the board is full (draw condition)."""
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == ' ':
                return False
    return True


def play_game():
    """Main game loop."""
    # Initialize board
    board = initialize_board(ROWS, COLS)
    
    # Print initial board
    print_board(board, COLS)
    
    # Randomly select starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Game loop
    while True:
        current_checker = CHECKERS[current_player_index]
        current_player_number = current_player_index + 1
        
        print(f"Player {current_checker}, please enter a column:")
        col = get_valid_input(COLS)
        
        # Try to place the checker
        if place_checker(board, col, current_checker, ROWS, COLS):
            # Check for win
            if check_win(board, ROWS, COLS, current_checker):
                print_board(board, COLS)
                print(f"Player {current_checker} won!")
                break
            
            # Check for draw
            if is_board_full(board, ROWS, COLS):
                print_board(board, COLS)
                print("It's a draw!")
                break
            
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board, COLS)
        else:
            # Invalid move, same player tries again
            print_board(board, COLS)


if __name__ == "__main__":
    play_game()
