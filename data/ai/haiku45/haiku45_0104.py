import os
import random

# Configuration constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """
    Initialize the game board with empty spaces.
    Returns a 2D list representing the board.
    """
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board


def print_board(board):
    """
    Print the current state of the board with column labels and formatting.
    """
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLUMNS):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print top border
    print("+---" * COLUMNS + "+")
    
    # Print each row with borders
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+---" * COLUMNS + "+")


def is_valid_column(column_input, board):
    """
    Validate the column input.
    Returns the column index (0-based) if valid, None otherwise.
    """
    # Check if input is a single character
    if len(column_input) != 1:
        return None
    
    # Check if input is a letter
    if not column_input.isalpha():
        return None
    
    # Convert to uppercase and get column index
    column_input = column_input.upper()
    column_index = ord(column_input) - ord('A')
    
    # Check if column index is within bounds
    if column_index < 0 or column_index >= COLUMNS:
        return None
    
    # Check if column is not full
    if board[0][column_index] != " ":
        return None
    
    return column_index


def place_checker(board, column_index, checker):
    """
    Place a checker in the specified column.
    Returns True if placement was successful, False otherwise.
    """
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][column_index] == " ":
            board[row][column_index] = checker
            return True
    
    return False


def check_win(board, checker):
    """
    Check if the specified checker has won.
    Returns True if the checker has 4 in a row, False otherwise.
    """
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLUMNS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely full.
    Returns True if board is full, False otherwise.
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def get_player_input(player_checker):
    """
    Get and validate input from the current player.
    Returns the validated column index.
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ")
        column_index = is_valid_column(user_input, board)
        
        if column_index is not None:
            return column_index
        else:
            print("Invalid input. Please enter a valid column letter (A-" + 
                  chr(65 + COLUMNS - 1) + ") that is not full.")


def play_game():
    """
    Main game loop.
    """
    global board
    
    # Initialize the board
    board = initialize_board()
    
    # Select a random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get current player's checker
        current_checker = PLAYER_CHECKERS[current_player_index]
        
        # Get player input
        column_index = get_player_input(current_checker)
        
        # Place checker
        place_checker(board, column_index, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    board = initialize_board()
    play_game()
