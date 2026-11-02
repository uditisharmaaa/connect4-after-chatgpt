import os
import random

# Global constants for board configuration
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """
    Initialize the game board with empty spaces.
    
    Returns:
        A 2D list representing the board with all cells containing spaces.
    """
    board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    return board


def print_board(board):
    """
    Print the current state of the board with column labels and borders.
    
    Args:
        board: The 2D list representing the game board.
    """
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(BOARD_COLS):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print board rows with borders
    for row in range(BOARD_ROWS):
        print("+---" * BOARD_COLS + "+")
        print("|", end="")
        for col in range(BOARD_COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    print("+---" * BOARD_COLS + "+")


def get_valid_input(current_player_checker):
    """
    Get and validate player input for column selection.
    
    Args:
        current_player_checker: The checker symbol of the current player.
    
    Returns:
        The column index (0-based) where the player wants to place their checker.
    """
    while True:
        user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter within board range
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col = ord(user_input) - ord('A')
        
        # Check if column is within board boundaries
        if col < 0 or col >= BOARD_COLS:
            print(f"Invalid input. Please enter a column between A and {chr(65 + BOARD_COLS - 1)}.")
            continue
        
        return col


def place_checker(board, col, checker):
    """
    Place a checker in the specified column at the lowest available row.
    
    Args:
        board: The 2D list representing the game board.
        col: The column index (0-based) where to place the checker.
        checker: The checker symbol to place.
    
    Returns:
        True if the checker was successfully placed, False if the column is full.
    """
    # Find the lowest empty row in the column (start from bottom)
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    return False


def check_win(board, checker):
    """
    Check if the specified checker has won the game.
    
    Args:
        board: The 2D list representing the game board.
        checker: The checker symbol to check for a win.
    
    Returns:
        True if the checker has 4 in a row, False otherwise.
    """
    # Check horizontal wins
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical wins
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal wins (top-left to bottom-right)
    for row in range(BOARD_ROWS - WIN_LENGTH + 1):
        for col in range(BOARD_COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal wins (top-right to bottom-left)
    for row in range(BOARD_ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, BOARD_COLS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_draw(board):
    """
    Check if the board is completely filled (draw condition).
    
    Args:
        board: The 2D list representing the game board.
    
    Returns:
        True if the board is full, False otherwise.
    """
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """
    Main game loop that controls the flow of the Connect 4 game.
    """
    # Initialize the board
    board = initialize_board()
    
    # Randomly select the first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    current_checker = CHECKERS[current_player]
    
    # Print the initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get valid column input from current player
        col = get_valid_input(current_checker)
        
        # Try to place the checker
        if not place_checker(board, col, current_checker):
            print("This column is full. Please choose another column.")
            continue
        
        # Print updated board
        print_board(board)
        
        # Check if current player won
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check if the game is a draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS
        current_checker = CHECKERS[current_player]


# Main entry point
if __name__ == "__main__":
    play_game()
