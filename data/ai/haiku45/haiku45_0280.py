import os
import random

# Game constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """Initialize the board with all empty spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board, cols):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print top border
    print("+---" * cols + "+")
    
    # Print rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+---" * cols + "+")


def get_column_input(cols):
    """Get and validate column input from the player."""
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col_index = ord(user_input) - ord('A')
        
        if col_index < 0 or col_index >= cols:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")
            continue
        
        return col_index


def place_checker(board, col, player_checker, rows, cols):
    """Place a checker in the specified column. Returns True if successful."""
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_checker
            return True
    
    # Column is full
    print("That column is full. Try another column.")
    return False


def check_win(board, rows, cols, player_checker):
    """Check if the specified player has won the game."""
    
    # Check horizontal
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + i][col - i] == player_checker for i in range(WIN_LENGTH)):
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
    # Initialize board
    board = initialize_board(ROWS, COLUMNS)
    
    # Select a random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board, COLUMNS)
    
    # Main game loop
    while True:
        # Get current player's checker
        current_checker = PLAYER_CHECKERS[current_player_index]
        
        # Prompt for input
        print(f"Player {current_checker}, please enter a column: ", end="")
        col = get_column_input(COLUMNS)
        
        # Place checker
        if not place_checker(board, col, current_checker, ROWS, COLUMNS):
            # Invalid move (column full), player loses turn
            print_board(board, COLUMNS)
            continue
        
        # Print updated board
        print_board(board, COLUMNS)
        
        # Check for win
        if check_win(board, ROWS, COLUMNS, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if check_draw(board, ROWS, COLUMNS):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
