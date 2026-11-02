import os
import random

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """Create and initialize an empty board with whitespaces."""
    board = []
    for row in range(ROWS):
        board.append([" " for col in range(COLS)])
    return board

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
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

def get_player_input(current_player):
    """Get and validate user input for column selection."""
    while True:
        user_input = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - ord('A')
        
        # Check if column is within board bounds
        if col < 0 or col >= COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(65 + COLS - 1)}.")
            continue
        
        return col

def place_checker(board, col, current_player):
    """Place a checker in the specified column. Returns True if successful, False if column is full."""
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = CHECKERS[current_player]
            return True
    
    # Column is full
    print("Column is full. Try a different column.")
    return False

def check_horizontal_win(board, current_player):
    """Check if the current player has won horizontally."""
    checker = CHECKERS[current_player]
    
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False

def check_vertical_win(board, current_player):
    """Check if the current player has won vertically."""
    checker = CHECKERS[current_player]
    
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False

def check_diagonal_win(board, current_player):
    """Check if the current player has won diagonally."""
    checker = CHECKERS[current_player]
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False

def check_win(board, current_player):
    """Check if the current player has won."""
    if check_horizontal_win(board, current_player):
        return True
    if check_vertical_win(board, current_player):
        return True
    if check_diagonal_win(board, current_player):
        return True
    return False

def check_draw(board):
    """Check if the board is completely full (draw condition)."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True

def play_game():
    """Main game loop."""
    # Initialize board
    board = initialize_board()
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Main game loop
    while True:
        # Get valid column from player
        col = get_player_input(current_player)
        
        # Try to place checker
        if not place_checker(board, col, current_player):
            # Turn is lost if column is full
            print("Turn lost. Switching to next player.")
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_player):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS

# Run the game
if __name__ == "__main__":
    play_game()
