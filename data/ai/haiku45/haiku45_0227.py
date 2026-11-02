import os
import random

# Constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """Initialize the board with empty spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board, cols):
    """Print the board in the required format."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for i in range(cols):
        print(f"{chr(65 + i)}   ", end="")
    print()
    
    # Print top border
    print("+---" * cols + "+")
    
    # Print rows with content
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+---" * cols + "+")


def get_valid_input(cols):
    """Get and validate player input for column selection."""
    while True:
        try:
            user_input = input().strip().upper()
            
            # Check if input is a single character
            if len(user_input) != 1:
                print("Invalid input. Please enter a single column letter (A-{}).".format(chr(65 + cols - 1)))
                continue
            
            # Check if input is a letter
            if not user_input.isalpha():
                print("Invalid input. Please enter a column letter (A-{}).".format(chr(65 + cols - 1)))
                continue
            
            # Convert letter to column index
            col_index = ord(user_input) - ord('A')
            
            # Check if column is within bounds
            if col_index < 0 or col_index >= cols:
                print("Invalid input. Please enter a column letter (A-{}).".format(chr(65 + cols - 1)))
                continue
            
            return col_index
            
        except Exception:
            print("Invalid input. Please enter a column letter (A-{}).".format(chr(65 + cols - 1)))


def place_checker(board, col, checker, rows, cols):
    """Place a checker in the specified column. Returns True if successful, False if column is full."""
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    return False


def check_win(board, rows, cols, checker):
    """Check if the given checker has won the game."""
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


def is_board_full(board, rows, cols):
    """Check if the board is completely full."""
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """Main game loop."""
    # Initialize board
    board = initialize_board(ROWS, COLS)
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board, COLS)
    
    # Game loop
    while True:
        # Get current player's checker
        checker = PLAYER_CHECKERS[current_player]
        
        # Get player input
        print(f"Player {checker}, please enter a column:", end=" ")
        col = get_valid_input(COLS)
        
        # Try to place checker
        if not place_checker(board, col, checker, ROWS, COLS):
            print(f"Column {chr(65 + col)} is full. You lose this turn.")
            print_board(board, COLS)
        else:
            # Print updated board
            print_board(board, COLS)
            
            # Check for win
            if check_win(board, ROWS, COLS, checker):
                print(f"Player {checker} won!")
                break
            
            # Check for draw
            if is_board_full(board, ROWS, COLS):
                print("It's a draw!")
                break
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS


def main():
    """Entry point of the program."""
    play_game()


if __name__ == "__main__":
    main()
