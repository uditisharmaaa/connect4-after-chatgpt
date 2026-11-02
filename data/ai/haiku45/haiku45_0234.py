import os
import random

# ============================================================================
# CONSTANT VARIABLES - Modify these to change game configuration
# ============================================================================
ROWS = 6  # Number of rows on the board
COLS = 7  # Number of columns on the board
NUM_PLAYERS = 2  # Number of players (2-5)
WIN_LENGTH = 4  # Number of checkers in a row needed to win

# Checkers for each player in order
CHECKERS = ["X", "O", "V", "H", "M"]

# ============================================================================
# BOARD INITIALIZATION AND DISPLAY FUNCTIONS
# ============================================================================

def initialize_board():
    """
    Initialize the game board with empty spaces.
    Returns a 2D list (board) with dimensions ROWS x COLS.
    """
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board


def print_board(board):
    """
    Print the game board with proper formatting.
    Displays column labels (A-Z) and rows with grid lines.
    """
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)} ", end=" ")
    print()
    
    # Print rows with grid lines
    for row in range(ROWS):
        # Top border of each cell
        print("+", end="")
        for col in range(COLS):
            print("---+", end="")
        print()
        
        # Cell content
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Bottom border
    print("+", end="")
    for col in range(COLS):
        print("---+", end="")
    print()


# ============================================================================
# INPUT VALIDATION AND MOVE HANDLING
# ============================================================================

def get_valid_column():
    """
    Prompt the player for a column input and validate it.
    Returns the column index (0-based) if valid, otherwise re-prompts.
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
        
        # Convert letter to column index (A=0, B=1, etc.)
        col_index = ord(user_input) - ord('A')
        
        # Check if column index is within board boundaries
        if col_index < 0 or col_index >= COLS:
            print(f"Invalid input. Please enter a letter between A and {chr(65 + COLS - 1)}.")
            continue
        
        return col_index


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    The checker falls to the lowest available row.
    Returns True if placement was successful, False if column is full.
    """
    # Start from the bottom row and move up to find the first empty space
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    return False


# ============================================================================
# WIN CONDITION CHECKING FUNCTIONS
# ============================================================================

def check_horizontal_win(board, checker):
    """
    Check if the given checker has won horizontally (4 in a row).
    Returns True if a win is found, False otherwise.
    """
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            # Check if all 4 consecutive cells contain the checker
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_vertical_win(board, checker):
    """
    Check if the given checker has won vertically (4 in a column).
    Returns True if a win is found, False otherwise.
    """
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            # Check if all 4 consecutive cells contain the checker
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_diagonal_win(board, checker):
    """
    Check if the given checker has won diagonally (4 in a row).
    Checks both diagonal directions: / and \.
    Returns True if a win is found, False otherwise.
    """
    # Check diagonal direction: \ (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal direction: / (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row - i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_win(board, checker):
    """
    Check if the given checker has won in any direction.
    Returns True if a win is found, False otherwise.
    """
    return (check_horizontal_win(board, checker) or 
            check_vertical_win(board, checker) or 
            check_diagonal_win(board, checker))


def check_draw(board):
    """
    Check if the board is completely full (draw condition).
    Returns True if all cells are filled, False otherwise.
    """
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True


# ============================================================================
# MAIN GAME LOOP
# ============================================================================

def play_game():
    """
    Main game loop that controls the flow of the Connect 4 game.
    Manages player turns, input validation, and win/draw conditions.
    """
    # Initialize the board
    board = initialize_board()
    
    # Select a random player to start
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Main game loop
    while True:
        # Get the current player's checker
        current_checker = CHECKERS[current_player_index]
        
        # Prompt current player for input
        print(f"Player {current_checker}, please enter a column:")
        col = get_valid_column()
        
        # Attempt to place the checker
        if not place_checker(board, col, current_checker):
            # Column is full, player loses turn
            print("Column is full. You lose your turn.")
            print_board(board)
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue
        
        # Print updated board
        print_board(board)
        
        # Check if current player won
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check if the game is a draw
        if check_draw(board):
            print("Game is a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    play_game()
