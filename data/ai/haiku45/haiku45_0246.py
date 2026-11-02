import os
import random

# Constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Create and return an empty board with dimensions COLUMNS x ROWS."""
    board = []
    for row in range(ROWS):
        board.append([" " for col in range(COLUMNS)])
    return board


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLUMNS):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print top border
    print("+---" * COLUMNS + "+")
    
    # Print each row
    for row in range(ROWS):
        print("|", end="")
        for col in range(COLUMNS):
            print(" " + board[row][col] + " |", end="")
        print()
        print("+---" * COLUMNS + "+")


def column_letter_to_index(letter):
    """Convert a column letter to its index (A=0, B=1, etc)."""
    return ord(letter.upper()) - ord('A')


def get_valid_input(board):
    """Get and validate player input for column selection."""
    while True:
        try:
            user_input = input("Please enter a column: ").strip()
            
            # Check if input is a single character
            if len(user_input) != 1:
                print("Invalid input. Please enter a single letter.")
                continue
            
            # Check if input is a letter
            if not user_input.isalpha():
                print("Invalid input. Please enter a letter.")
                continue
            
            # Convert to column index
            col = column_letter_to_index(user_input)
            
            # Check if column is within bounds
            if col < 0 or col >= COLUMNS:
                print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + COLUMNS - 1)}.")
                continue
            
            # Check if column is full
            if board[0][col] != " ":
                print("This column is full. Please choose another column.")
                continue
            
            return col
        
        except Exception:
            print("Invalid input. Please try again.")


def place_checker(board, col, checker):
    """Place a checker in the specified column. Return True if successful."""
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    return False


def check_win(board, checker):
    """Check if the specified checker has won. Return True if won."""
    # Check horizontal wins
    for row in range(ROWS):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical wins
    for col in range(COLUMNS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal wins (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal wins (top-right to bottom-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLUMNS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board):
    """Check if the board is full. Return True if full."""
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """Main game loop."""
    # Initialize board
    board = initialize_board()
    
    # Select random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    print(f"Player {CHECKERS[current_player_index]} will start first.")
    input("Press Enter to continue...")
    
    # Game loop
    game_over = False
    
    while not game_over:
        # Print board and ask for input
        print_board(board)
        current_checker = CHECKERS[current_player_index]
        print(f"Player {current_checker}, please enter a column:")
        
        # Get valid input and place checker
        col = get_valid_input(board)
        place_checker(board, col, current_checker)
        
        # Check for win
        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
        
        # Check for draw
        elif is_board_full(board):
            print_board(board)
            print("The board is full. It's a draw!")
            game_over = True
        
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


# Main entry point
if __name__ == "__main__":
    play_game()
