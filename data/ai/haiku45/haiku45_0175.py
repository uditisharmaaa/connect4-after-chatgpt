import os
import random

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(width, height):
    """
    Initialize the board with empty spaces.
    
    Args:
        width: Number of columns
        height: Number of rows
    
    Returns:
        A 2D list representing the board
    """
    return [[" " for _ in range(width)] for _ in range(height)]


def print_board(board):
    """
    Print the current state of the board.
    
    Args:
        board: 2D list representing the board
    """
    os.system('clear')
    
    width = len(board[0])
    height = len(board)
    
    # Print column headers
    print("  ", end="")
    for col in range(width):
        print(chr(65 + col) + "   ", end="")
    print()
    
    # Print top border
    print("+---" * width + "+")
    
    # Print rows
    for row in range(height):
        print("|", end="")
        for col in range(width):
            print(" " + board[row][col] + " |", end="")
        print()
        print("+---" * width + "+")


def get_valid_input(width):
    """
    Get and validate player input for column selection.
    
    Args:
        width: Number of columns on the board
    
    Returns:
        The column index (0-indexed) where the player wants to place their checker
    """
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column index is within bounds
        if col_index < 0 or col_index >= width:
            print(f"Invalid input. Please enter a letter between A and {chr(65 + width - 1)}.")
            continue
        
        return col_index


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: 2D list representing the board
        col: Column index (0-indexed)
        checker: The checker symbol to place
    
    Returns:
        True if checker was placed successfully, False if column is full
    """
    height = len(board)
    
    # Find the lowest empty row in the column
    for row in range(height - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    print("Column is full. Please choose another column.")
    return False


def check_win(board, checker):
    """
    Check if the specified checker has won.
    
    Args:
        board: 2D list representing the board
        checker: The checker symbol to check for a win
    
    Returns:
        True if the checker has won, False otherwise
    """
    height = len(board)
    width = len(board[0])
    
    # Check horizontal
    for row in range(height):
        for col in range(width - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(width):
        for row in range(height - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(height - WIN_LENGTH + 1):
        for col in range(width - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(height - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, width):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_draw(board):
    """
    Check if the board is full (game is a draw).
    
    Args:
        board: 2D list representing the board
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def play_game(width, height, num_players):
    """
    Main game loop for Connect 4.
    
    Args:
        width: Number of columns
        height: Number of rows
        num_players: Number of players
    """
    # Initialize the board
    board = initialize_board(width, height)
    
    # Randomly select the first player
    current_player = random.randint(0, num_players - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        checker = CHECKERS[current_player]
        print(f"Player {checker}, please enter a column: ", end="")
        
        # Get valid column input
        col = get_valid_input(width)
        
        # Try to place the checker
        if not place_checker(board, col, checker):
            # Column was full, ask again without switching player
            continue
        
        # Print the updated board
        print_board(board)
        
        # Check for win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % num_players


def main():
    """Main entry point for the Connect 4 game."""
    play_game(BOARD_WIDTH, BOARD_HEIGHT, NUM_PLAYERS)


if __name__ == "__main__":
    main()
