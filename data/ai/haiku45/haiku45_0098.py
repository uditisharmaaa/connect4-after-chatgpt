import os
import random

# ============================================================================
# CONSTANT VARIABLES - Modify these to change game configuration
# ============================================================================
COLS = 7  # Number of columns (max 26)
ROWS = 6  # Number of rows
NUM_PLAYERS = 2  # Number of players (2-5)
WIN_LENGTH = 4  # Number of checkers needed in a row to win

# List of checker symbols for each player
CHECKERS = ["X", "O", "V", "H", "M"]


# ============================================================================
# BOARD FUNCTIONS
# ============================================================================

def initialize_board():
    """
    Initialize the game board with all empty cells (whitespace).
    Returns a 2D list representing the board.
    """
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board


def print_board(board):
    """
    Print the current state of the game board with column labels and borders.
    Clears the screen before printing.
    """
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)} ", end="")
    print()
    
    # Print each row with borders
    for row in range(ROWS):
        # Top border
        print("+---" * COLS + "+")
        # Row content
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Bottom border
    print("+---" * COLS + "+")


# ============================================================================
# INPUT VALIDATION AND PLACEMENT FUNCTIONS
# ============================================================================

def is_valid_input(user_input, board):
    """
    Validate user input. Returns True if input is valid, False otherwise.
    Valid input must be:
    - A single uppercase letter
    - Within the column range (A to G for 7 columns, etc.)
    - The column must not be completely filled
    """
    # Check if input is a single character
    if len(user_input) != 1:
        return False
    
    # Check if input is an uppercase letter
    if not user_input.isupper() or not user_input.isalpha():
        return False
    
    # Check if input is within valid column range
    col_index = ord(user_input) - ord('A')
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if the column is not completely filled
    if board[0][col_index] != " ":
        return False
    
    return True


def get_player_input(board, player_checker):
    """
    Get valid input from the player. Keeps asking until valid input is provided.
    Returns the column index (0-based) where the player wants to place their checker.
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip()
        
        if is_valid_input(user_input, board):
            col_index = ord(user_input) - ord('A')
            return col_index
        else:
            print("Invalid input. Please enter a valid column letter (A-{}).".format(
                chr(65 + COLS - 1)))


def place_checker(board, col_index, player_checker):
    """
    Place the player's checker in the specified column.
    The checker falls to the lowest available position in that column.
    Returns True if placement was successful, False if column is full.
    """
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = player_checker
            return True
    
    return False


# ============================================================================
# WIN CHECKING FUNCTIONS
# ============================================================================

def check_horizontal_win(board, player_checker):
    """
    Check if the player has won with 4 checkers in a row horizontally.
    """
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            # Check if all 4 consecutive checkers in this row are the player's
            if all(board[row][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_vertical_win(board, player_checker):
    """
    Check if the player has won with 4 checkers in a row vertically.
    """
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            # Check if all 4 consecutive checkers in this column are the player's
            if all(board[row + i][col] == player_checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_diagonal_win(board, player_checker):
    """
    Check if the player has won with 4 checkers in a row diagonally.
    Checks both diagonal directions: top-left to bottom-right and 
    top-right to bottom-left.
    """
    # Check diagonals going down-right
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonals going down-left
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLS):
            if all(board[row + i][col - i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_win(board, player_checker):
    """
    Check if the current player has won by checking all possible directions.
    """
    return (check_horizontal_win(board, player_checker) or
            check_vertical_win(board, player_checker) or
            check_diagonal_win(board, player_checker))


def check_draw(board):
    """
    Check if the board is completely filled (draw condition).
    A draw occurs when all cells are filled and no player has won.
    """
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True


# ============================================================================
# GAME CONTROL FUNCTIONS
# ============================================================================

def get_next_player(current_player_index):
    """
    Get the index of the next player in turn order.
    """
    return (current_player_index + 1) % NUM_PLAYERS


def play_game():
    """
    Main game loop that controls the flow of the Connect 4 game.
    """
    # Initialize the board
    board = initialize_board()
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Get the checker symbol for the current player
    current_player_checker = CHECKERS[current_player_index]
    
    # Print the initial board
    print_board(board)
    print(f"Player {current_player_checker} will start first!\n")
    
    # Main game loop
    while True:
        # Get valid input from the current player
        col_index = get_player_input(board, current_player_checker)
        
        # Place the checker
        place_checker(board, col_index, current_player_checker)
        
        # Print the updated board
        print_board(board)
        
        # Check if the current player has won
        if check_win(board, current_player_checker):
            print(f"Player {current_player_checker} won!\n")
            break
        
        # Check if the board is full (draw)
        if check_draw(board):
            print("It's a draw!\n")
            break
        
        # Move to the next player
        current_player_index = get_next_player(current_player_index)
        current_player_checker = CHECKERS[current_player_index]


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    play_game()
