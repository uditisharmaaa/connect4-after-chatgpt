import os
import random

# Configuration constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """
    Initialize an empty board with all cells containing whitespace.
    
    Returns:
        list: A 2D list representing the board (ROWS x COLS)
    """
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board


def print_board(board):
    """
    Print the board to the console with proper formatting.
    
    Args:
        board (list): The 2D board to print
    """
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(ord('A') + col)}  ", end="")
    print()
    
    # Print board with separators
    for row in range(ROWS):
        # Print top border
        print("+---" * COLS + "+")
        
        # Print row content
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+---" * COLS + "+")


def get_valid_input(current_player):
    """
    Get a valid column input from the current player.
    Keep asking until valid input is provided.
    
    Args:
        current_player (str): The current player's checker
    
    Returns:
        int: The column index (0 to COLS-1) where the checker will be placed
    """
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        
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
        
        # Check if column is within board range
        if col < 0 or col >= COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + COLS - 1)}.")
            continue
        
        return col


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    The checker falls to the lowest available space.
    
    Args:
        board (list): The 2D board
        col (int): The column index
        checker (str): The player's checker
    
    Returns:
        bool: True if placement was successful, False if column is full
    """
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    print("Column is full. Please choose another column.")
    return False


def check_win(board, checker):
    """
    Check if the specified player has won the game.
    A player wins by getting WIN_LENGTH checkers in a row
    (horizontally, vertically, or diagonally).
    
    Args:
        board (list): The 2D board
        checker (str): The player's checker to check for
    
    Returns:
        bool: True if the player has won, False otherwise
    """
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
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


def check_draw(board):
    """
    Check if the board is full (draw condition).
    
    Args:
        board (list): The 2D board
    
    Returns:
        bool: True if all cells are filled, False otherwise
    """
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board()
    
    # Create list of player checkers
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_player = players[current_player_index]
        
        # Get valid column input
        col = get_valid_input(current_player)
        
        # Try to place the checker
        if not place_checker(board, col, current_player):
            # Column was full, player keeps trying
            continue
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
