import os
import random

# Constants for board dimensions and players
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
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
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board, cols):
    """
    Print the current state of the board.
    
    Args:
        board: The game board (2D list)
        cols: Number of columns in the board
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print top border
    print("+---" * cols + "+")
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+---" * cols + "+")


def get_valid_column(cols):
    """
    Get a valid column input from the player.
    
    Args:
        cols: Number of columns in the board
    
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
        
        if col_index < 0 or col_index >= cols:
            print(f"Invalid input. Please enter a column between A and {chr(65 + cols - 1)}.")
            continue
        
        return col_index


def place_checker(board, col, checker, rows, cols):
    """
    Place a checker in the specified column.
    
    Args:
        board: The game board (2D list)
        col: The column index (0-based) where the checker should be placed
        checker: The player's checker symbol
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        True if the checker was successfully placed, False if the column is full
    """
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    return False


def check_winner(board, rows, cols, checker):
    """
    Check if the specified player has won.
    
    Args:
        board: The game board (2D list)
        rows: Number of rows in the board
        cols: Number of columns in the board
        checker: The player's checker symbol to check for winning
    
    Returns:
        True if the player has won, False otherwise
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
    Check if the board is completely full (draw condition).
    
    Args:
        board: The game board (2D list)
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLUMNS)
    
    # Get player checkers
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board, COLUMNS)
    
    # Main game loop
    while True:
        current_checker = player_checkers[current_player_index]
        player_number = current_player_index + 1
        
        print(f"Player {current_checker}, please enter a column: ", end="")
        col = get_valid_column(COLUMNS)
        
        # Try to place the checker
        if not place_checker(board, col, current_checker, ROWS, COLUMNS):
            print("Column is full. You lose your turn.")
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board, COLUMNS)
            continue
        
        # Print the board after the move
        print_board(board, COLUMNS)
        
        # Check for a win
        if check_winner(board, ROWS, COLUMNS, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for a draw
        if is_board_full(board, ROWS, COLUMNS):
            print("It's a draw!")
            break
        
        # Move to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


def main():
    """
    Entry point of the program.
    """
    play_game()


if __name__ == "__main__":
    main()
