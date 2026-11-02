import os
import random

# Constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the game board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the game board
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board, cols):
    """
    Print the game board in a formatted manner.
    
    Args:
        board: The 2D list representing the game board
        cols: Number of columns in the board
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print board with borders
    for row in board:
        print("+---" * cols + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    
    print("+---" * cols + "+")


def is_valid_input(column_letter, cols):
    """
    Validate if the input is a valid column letter.
    
    Args:
        column_letter: The input from the player
        cols: Number of columns in the board
    
    Returns:
        True if valid, False otherwise
    """
    if len(column_letter) != 1:
        return False
    
    if not column_letter.isalpha():
        return False
    
    column_index = ord(column_letter.upper()) - ord('A')
    
    if column_index < 0 or column_index >= cols:
        return False
    
    return True


def get_column_input(cols):
    """
    Get and validate column input from the player.
    
    Args:
        cols: Number of columns in the board
    
    Returns:
        The column index (0-based)
    """
    while True:
        column_letter = input("Please enter a column: ").strip().upper()
        
        if not is_valid_input(column_letter, cols):
            print(f"Invalid input. Please enter a letter from A to {chr(65 + cols - 1)}.")
            continue
        
        column_index = ord(column_letter) - ord('A')
        return column_index


def can_place_checker(board, col, rows):
    """
    Check if a checker can be placed in the given column.
    
    Args:
        board: The 2D list representing the game board
        col: The column index
        rows: Number of rows in the board
    
    Returns:
        True if a checker can be placed, False otherwise
    """
    return board[0][col] == " "


def place_checker(board, col, checker, rows):
    """
    Place a checker in the given column.
    
    Args:
        board: The 2D list representing the game board
        col: The column index
        checker: The checker symbol (X, O, etc.)
        rows: Number of rows in the board
    
    Returns:
        True if successful, False otherwise
    """
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    return False


def check_winner(board, rows, cols, checker):
    """
    Check if the given checker has won the game.
    
    Args:
        board: The 2D list representing the game board
        rows: Number of rows in the board
        cols: Number of columns in the board
        checker: The checker symbol to check for
    
    Returns:
        True if the checker has won, False otherwise
    """
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
    """
    Check if the board is completely full.
    
    Args:
        board: The 2D list representing the game board
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        True if board is full, False otherwise
    """
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == " ":
                return False
    
    return True


def play_connect4():
    """
    Main function to run the Connect 4 game.
    """
    # Initialize board
    board = initialize_board(ROWS, COLUMNS)
    
    # Get player checkers
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board, COLUMNS)
    print(f"Player {player_checkers[current_player_index]} starts the game!\n")
    
    # Game loop
    game_over = False
    
    while not game_over:
        current_checker = player_checkers[current_player_index]
        
        print(f"Player {current_checker}, please enter a column:")
        
        # Get valid column input
        while True:
            col = get_column_input(COLUMNS)
            
            # Check if column is not full
            if not can_place_checker(board, col, ROWS):
                print("Column is full. Please choose another column.")
                continue
            
            break
        
        # Place checker
        place_checker(board, col, current_checker, ROWS)
        
        # Print updated board
        print_board(board, COLUMNS)
        
        # Check for winner
        if check_winner(board, ROWS, COLUMNS, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        
        # Check for draw
        elif is_board_full(board, ROWS, COLUMNS):
            print("It's a draw!")
            game_over = True
        
        else:
            # Switch to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_connect4()
