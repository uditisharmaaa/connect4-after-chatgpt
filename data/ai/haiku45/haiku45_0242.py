import os
import random

# Constants for board configuration
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checker symbols
CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board():
    """
    Initialize a board with all empty spaces.
    
    Returns:
        A 2D list representing the game board, with dimensions ROWS x COLUMNS
    """
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board

def print_board(board):
    """
    Print the game board in a formatted manner.
    
    Args:
        board: The 2D list representing the game board
    """
    os.system('clear')
    
    # Print column headers (A, B, C, ...)
    print("  ", end="")
    for col in range(COLUMNS):
        print(f" {chr(ord('A') + col)} ", end=" ")
    print()
    
    # Print top border
    print("+", end="")
    for _ in range(COLUMNS):
        print("---+", end="")
    print()
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        
        # Print row separator
        print("+", end="")
        for _ in range(COLUMNS):
            print("---+", end="")
        print()

def is_valid_column(column_input, board):
    """
    Validate if the input column is valid and not full.
    
    Args:
        column_input: The user input (should be a single letter)
        board: The 2D list representing the game board
    
    Returns:
        True if the input is valid and the column is not full, False otherwise
    """
    # Check if input is a single character
    if len(column_input) != 1:
        return False
    
    # Check if input is a letter
    if not column_input.isalpha():
        return False
    
    # Convert to uppercase and get column index
    column_input = column_input.upper()
    column_index = ord(column_input) - ord('A')
    
    # Check if column index is within bounds
    if column_index < 0 or column_index >= COLUMNS:
        return False
    
    # Check if column is not full (top cell is empty)
    if board[0][column_index] != " ":
        return False
    
    return True

def get_column_index(column_input):
    """
    Convert column letter input to column index.
    
    Args:
        column_input: The user input letter (e.g., 'A', 'B')
    
    Returns:
        The column index as an integer
    """
    return ord(column_input.upper()) - ord('A')

def place_checker(board, column_index, checker):
    """
    Place a checker in the specified column.
    The checker falls to the lowest available space.
    
    Args:
        board: The 2D list representing the game board
        column_index: The column where the checker should be placed
        checker: The checker symbol ('X', 'O', etc.)
    
    Returns:
        The row index where the checker was placed, or -1 if placement failed
    """
    # Start from the bottom and move up to find the first empty space
    for row in range(ROWS - 1, -1, -1):
        if board[row][column_index] == " ":
            board[row][column_index] = checker
            return row
    
    # Column is full
    return -1

def check_win(board, row, col, checker):
    """
    Check if the last placed checker resulted in a win.
    Checks horizontally, vertically, and diagonally.
    
    Args:
        board: The 2D list representing the game board
        row: The row index of the last placed checker
        col: The column index of the last placed checker
        checker: The checker symbol to check for
    
    Returns:
        True if there's a win, False otherwise
    """
    # Check horizontal
    if check_direction(board, row, col, checker, 0, 1):
        return True
    
    # Check vertical
    if check_direction(board, row, col, checker, 1, 0):
        return True
    
    # Check diagonal (top-left to bottom-right)
    if check_direction(board, row, col, checker, 1, 1):
        return True
    
    # Check diagonal (top-right to bottom-left)
    if check_direction(board, row, col, checker, 1, -1):
        return True
    
    return False

def check_direction(board, row, col, checker, row_delta, col_delta):
    """
    Check if there are 4 checkers in a row in a specific direction.
    
    Args:
        board: The 2D list representing the game board
        row: Starting row index
        col: Starting column index
        checker: The checker symbol to check for
        row_delta: The direction to move in rows (-1, 0, or 1)
        col_delta: The direction to move in columns (-1, 0, or 1)
    
    Returns:
        True if 4 checkers in a row are found, False otherwise
    """
    count = 1  # Count the checker at (row, col)
    
    # Check in the positive direction
    r, c = row + row_delta, col + col_delta
    while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
        count += 1
        r += row_delta
        c += col_delta
    
    # Check in the negative direction
    r, c = row - row_delta, col - col_delta
    while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
        count += 1
        r -= row_delta
        c -= col_delta
    
    return count >= WIN_LENGTH

def is_board_full(board):
    """
    Check if the board is completely full (draw condition).
    
    Args:
        board: The 2D list representing the game board
    
    Returns:
        True if the board is full, False otherwise
    """
    for cell in board[0]:
        if cell == " ":
            return False
    return True

def get_valid_column_input(player_checker):
    """
    Get valid column input from the player.
    Keep asking until a valid input is provided.
    
    Args:
        player_checker: The checker symbol of the current player
    
    Returns:
        The column index where the player wants to place their checker
    """
    while True:
        column_input = input(f"Player {player_checker}, please enter a column: ")
        
        if is_valid_column(column_input, board):
            return get_column_index(column_input)
        else:
            print("Invalid input. Please enter a valid column letter (A-G) "
                  "for a column that is not full.")

def play_game():
    """
    Main game loop for Connect 4.
    Handles player turns, input validation, checker placement, 
    and win/draw detection.
    """
    # Initialize the board
    global board
    board = initialize_board()
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    
    # Game loop
    game_won = False
    
    while not game_won:
        # Get current player's checker
        current_checker = CHECKERS[current_player_index]
        
        # Get valid column input from the player
        column_index = get_valid_column_input(current_checker)
        
        # Place the checker
        row_index = place_checker(board, column_index, current_checker)
        
        # Print the updated board
        print_board(board)
        
        # Check if the current player won
        if check_win(board, row_index, column_index, current_checker):
            print(f"Player {current_checker} won!")
            game_won = True
        # Check if the board is full (draw)
        elif is_board_full(board):
            print("It's a draw!")
            game_won = True
        else:
            # Move to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Main entry point
if __name__ == "__main__":
    board = None
    play_game()
