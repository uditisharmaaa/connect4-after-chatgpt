import os
import random

# Global constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, columns):
    """
    Initialize the game board with all empty cells (whitespace).
    
    Args:
        rows: Number of rows in the board
        columns: Number of columns in the board
    
    Returns:
        A 2D list representing the board
    """
    board = [[" " for _ in range(columns)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Print the game board to the console.
    
    Args:
        board: The 2D list representing the game board
    """
    os.system('clear')
    columns = len(board[0])
    rows = len(board)
    
    # Print column headers (A, B, C, etc.)
    print("  ", end="")
    for col in range(columns):
        print(chr(ord('A') + col) + "   ", end="")
    print()
    
    # Print the board with borders
    for row in range(rows):
        # Print top border
        print("+---" * columns + "+")
        
        # Print row content
        print("|", end="")
        for col in range(columns):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Print bottom border
    print("+---" * columns + "+")


def get_valid_input(columns):
    """
    Get and validate player input for column selection.
    
    Args:
        columns: Number of columns in the board
    
    Returns:
        The column index (0-based) where the player wants to place their checker
    """
    while True:
        user_input = input().strip().upper()
        
        # Validate input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter (A-{}):".format(
                chr(ord('A') + columns - 1)))
            continue
        
        # Validate input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a single letter (A-{}):".format(
                chr(ord('A') + columns - 1)))
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Validate column is within board bounds
        if col_index < 0 or col_index >= columns:
            print("Invalid input. Please enter a single letter (A-{}):".format(
                chr(ord('A') + columns - 1)))
            continue
        
        return col_index


def place_checker(board, column, checker):
    """
    Place a checker in the specified column at the lowest available position.
    
    Args:
        board: The 2D list representing the game board
        column: The column index (0-based) where to place the checker
        checker: The checker symbol (X, O, V, H, or M)
    
    Returns:
        True if the checker was placed successfully, False if the column is full
    """
    rows = len(board)
    
    # Find the lowest empty cell in the column
    for row in range(rows - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    
    # Column is full
    return False


def check_winner(board, checker):
    """
    Check if the specified checker has won the game.
    
    Args:
        board: The 2D list representing the game board
        checker: The checker symbol to check for a win
    
    Returns:
        True if the checker has 4 in a row, False otherwise
    """
    rows = len(board)
    columns = len(board[0])
    
    # Check horizontal
    for row in range(rows):
        for col in range(columns - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(columns):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(columns - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, columns):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely full (draw condition).
    
    Args:
        board: The 2D list representing the game board
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in board:
        if " " in row:
            return False
    return True


def play_game():
    """
    Main game loop for Connect 4.
    Handles game initialization, turn alternation, and game end conditions.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLUMNS)
    
    # Select a random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Main game loop
    while True:
        checker = CHECKERS[current_player]
        
        # Prompt current player for input
        print("Player {}, please enter a column:".format(checker))
        column = get_valid_input(COLUMNS)
        
        # Attempt to place the checker
        if not place_checker(board, column, checker):
            print("Column is full. Please try another column.")
            continue
        
        # Print updated board
        print_board(board)
        
        # Check for a win
        if check_winner(board, checker):
            print("Player {} won!".format(checker))
            break
        
        # Check for a draw
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
