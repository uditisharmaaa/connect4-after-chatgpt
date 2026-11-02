import os
import random

# Global constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

def initialize_board():
    """Create and return an empty board with all cells initialized to spaces."""
    board = []
    for row in range(ROWS):
        board.append([" " for col in range(COLUMNS)])
    return board

def print_board(board):
    """Print the board in the required format."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLUMNS):
        letter = chr(ord('A') + col)
        print(f" {letter}  ", end="")
    print()
    
    # Print each row with borders
    for row in range(ROWS):
        print("+---" * COLUMNS + "+")
        print("|", end="")
        for col in range(COLUMNS):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+---" * COLUMNS + "+")

def get_valid_column():
    """Get a valid column input from the player."""
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        
        # Check if input is a single letter
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column is within board bounds
        if col_index < 0 or col_index >= COLUMNS:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + COLUMNS - 1)}.")
            continue
        
        return col_index

def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    Return True if placement was successful, False if column is full.
    """
    # Find the lowest available row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    print("This column is full. Please choose another column.")
    return False

def check_winner(board, checker):
    """Check if the player with the given checker has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLUMNS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is completely full."""
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == " ":
                return False
    return True

def main():
    """Main game loop."""
    # Initialize the board
    board = initialize_board()
    
    # Get the checkers for this game
    game_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    print(f"Player {game_checkers[current_player_index]} starts!")
    print()
    
    # Game loop
    game_over = False
    winner = None
    
    while not game_over:
        current_checker = game_checkers[current_player_index]
        
        # Get valid column from player
        col = get_valid_column()
        
        # Try to place the checker
        if place_checker(board, col, current_checker):
            # Print updated board
            print_board(board)
            
            # Check for win
            if check_winner(board, current_checker):
                print(f"Player {current_checker} won!")
                game_over = True
                winner = current_checker
            # Check for draw
            elif is_board_full(board):
                print("It's a draw!")
                game_over = True
            else:
                # Move to next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
                current_checker = game_checkers[current_player_index]
                print(f"Player {current_checker}, please enter a column:")
        else:
            # Invalid placement (column full), ask again
            print(f"Player {current_checker}, please enter a column:")

if __name__ == "__main__":
    main()
