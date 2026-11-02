import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']


def initialize_board():
    """Create and return an empty board with all spaces."""
    board = []
    for row in range(NUM_ROWS):
        board.append([' ' for col in range(NUM_COLS)])
    return board


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(NUM_COLS):
        print(chr(65 + col) + "   ", end="")
    print()
    
    # Print each row
    for row in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        print("|", end="")
        for col in range(NUM_COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    print("+---" * NUM_COLS + "+")


def get_column_input(current_player_checker):
    """Get valid column input from the current player."""
    while True:
        user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
        
        # Check if input is valid
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col_index = ord(user_input) - 65
        
        if col_index < 0 or col_index >= NUM_COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(65 + NUM_COLS - 1)}.")
            continue
        
        return col_index


def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column.
    Return True if successful, False if column is full.
    """
    # Find the lowest empty row in the column
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    
    # Column is full
    print("That column is full. Please try another column.")
    return False


def check_horizontal_win(board, checker):
    """Check if there is a horizontal win for the given checker."""
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_vertical_win(board, checker):
    """Check if there is a vertical win for the given checker."""
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_diagonal_win(board, checker):
    """Check if there is a diagonal win for the given checker."""
    # Check diagonals going down-right
    for row in range(NUM_ROWS - WIN_LENGTH + 1):
        for col in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonals going down-left
    for row in range(NUM_ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, NUM_COLS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_win(board, checker):
    """Check if the given checker has won."""
    return (check_horizontal_win(board, checker) or
            check_vertical_win(board, checker) or
            check_diagonal_win(board, checker))


def check_draw(board):
    """Check if the board is full (draw condition)."""
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if board[row][col] == ' ':
                return False
    return True


def play_game():
    """Main game loop."""
    # Initialize the board
    board = initialize_board()
    
    # Get player checkers
    player_checkers = PLAYER_CHECKERS[:NUM_PLAYERS]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get current player's checker
        current_checker = player_checkers[current_player_index]
        
        # Get valid column input
        col_index = get_column_input(current_checker)
        
        # Try to place checker
        if not place_checker(board, col_index, current_checker):
            # Column was full, ask for input again (turn not lost)
            continue
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


# Run the game
if __name__ == "__main__":
    play_game()
