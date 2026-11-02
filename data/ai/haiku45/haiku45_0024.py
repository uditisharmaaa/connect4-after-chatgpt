import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, columns):
    """
    Initialize a game board with all empty spaces.
    
    Args:
        rows: Number of rows in the board
        columns: Number of columns in the board
    
    Returns:
        A 2D list representing the game board
    """
    board = [[" " for _ in range(columns)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Print the game board in the specified format.
    
    Args:
        board: The current game board
    """
    os.system('clear')
    columns = len(board[0])
    rows = len(board)
    
    # Print column labels
    print("  ", end="")
    for i in range(columns):
        print(f" {chr(ord('A') + i)}  ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        # Top border
        print("+", end="")
        for col in range(columns):
            print("---+", end="")
        print()
        
        # Row content
        print("|", end="")
        for col in range(columns):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Bottom border
    print("+", end="")
    for col in range(columns):
        print("---+", end="")
    print()


def get_column_input(columns):
    """
    Get and validate column input from the user.
    
    Args:
        columns: Number of columns in the board
    
    Returns:
        The column index (0-based) where the player wants to place their checker
    """
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
        
        if col_index < 0 or col_index >= columns:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + columns - 1)}.")
            continue
        
        return col_index


def place_checker(board, column, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The current game board
        column: The column index where to place the checker
        checker: The checker symbol to place
    
    Returns:
        True if the checker was successfully placed, False if the column is full
    """
    rows = len(board)
    
    # Find the lowest available row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    
    return False


def check_win(board, checker):
    """
    Check if the given checker has won the game.
    
    Args:
        board: The current game board
        checker: The checker symbol to check for a win
    
    Returns:
        True if the checker has won, False otherwise
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
    Check if the board is completely full.
    
    Args:
        board: The current game board
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLUMNS)
    
    # Get the checkers for each player
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    
    # Game loop
    while True:
        current_checker = player_checkers[current_player_index]
        player_number = current_player_index + 1
        
        print(f"Player {current_checker}, please enter a column:")
        
        # Get valid column input
        while True:
            column = get_column_input(COLUMNS)
            
            # Try to place the checker
            if place_checker(board, column, current_checker):
                break
            else:
                print("Column is full. Please choose another column.")
        
        # Print the updated board
        print_board(board)
        
        # Check for a win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for a draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
