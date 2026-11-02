import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def initialize_board(rows, cols):
    """
    Initialize the game board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the board
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board, cols):
    """
    Print the game board in a formatted manner.
    
    Args:
        board: The game board (2D list)
        cols: Number of columns in the board
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for i in range(cols):
        print(f" {chr(65 + i)} ", end=" ")
    print()
    
    # Print board with borders
    for row in board:
        print("+---" * cols + "+")
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
        The column index (0-based) entered by the player
    """
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column is within bounds
        if col_index < 0 or col_index >= cols:
            print(f"Invalid input. Please enter a letter between A and {chr(65 + cols - 1)}.")
            continue
        
        return col_index


def place_checker(board, col, checker, rows, cols):
    """
    Place a checker in the specified column.
    
    Args:
        board: The game board (2D list)
        col: The column index where the checker should be placed
        checker: The checker symbol (X, O, V, H, or M)
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        True if the checker was successfully placed, False otherwise
    """
    # Find the lowest available row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    print("This column is full. Please choose another column.")
    return False


def check_win(board, rows, cols, checker):
    """
    Check if the specified checker has won the game.
    
    Args:
        board: The game board (2D list)
        rows: Number of rows in the board
        cols: Number of columns in the board
        checker: The checker symbol to check for a win
    
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
    board = initialize_board(ROWS, COLS)
    
    # Get the checkers for this game
    game_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board, COLS)
    print(f"Player {game_checkers[current_player_index]} starts first!")
    
    game_over = False
    
    # Main game loop
    while not game_over:
        current_checker = game_checkers[current_player_index]
        print(f"\nPlayer {current_checker}, please enter a column: ", end="")
        
        col = get_valid_column(COLS)
        
        # Try to place the checker
        if place_checker(board, col, current_checker, ROWS, COLS):
            # Print updated board
            print_board(board, COLS)
            
            # Check for a win
            if check_win(board, ROWS, COLS, current_checker):
                print(f"Player {current_checker} won!")
                game_over = True
            # Check for a draw
            elif is_board_full(board, ROWS, COLS):
                print("It's a draw!")
                game_over = True
            else:
                # Move to next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            # Invalid move, ask for input again without changing player
            print(f"Player {current_checker}, please enter a column: ", end="")


if __name__ == "__main__":
    play_game()
