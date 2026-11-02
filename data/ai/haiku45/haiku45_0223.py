import os
import random

# Global constants
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
        A 2D list representing the board
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board, cols):
    """
    Print the game board in a formatted manner.
    
    Args:
        board: The current game board
        cols: Number of columns in the board
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(chr(65 + col), end="   ")
    print()
    
    # Print board with borders
    for row in board:
        print("+---" * cols + "+")
        print("|", end="")
        for cell in row:
            print(" " + cell + " |", end="")
        print()
    
    print("+---" * cols + "+")


def get_valid_input(cols):
    """
    Get a valid column input from the player.
    
    Args:
        cols: Number of columns in the board
    
    Returns:
        The column index (0-based) where the player wants to place their checker
    """
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Check if input is within valid range
        col_index = ord(user_input) - ord('A')
        if col_index < 0 or col_index >= cols:
            print(f"Invalid input. Please enter a letter between A and {chr(65 + cols - 1)}.")
            continue
        
        return col_index


def can_place_checker(board, col, rows):
    """
    Check if a checker can be placed in the given column.
    
    Args:
        board: The current game board
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
        board: The current game board
        col: The column index
        checker: The player's checker symbol
        rows: Number of rows in the board
    
    Returns:
        The row index where the checker was placed, or -1 if placement failed
    """
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1


def check_win(board, row, col, checker, rows, cols):
    """
    Check if the last placed checker results in a win.
    
    Args:
        board: The current game board
        row: The row of the last placed checker
        col: The column of the last placed checker
        checker: The player's checker symbol
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        True if the player has won, False otherwise
    """
    # Check horizontal
    count = 1
    # Check left
    j = col - 1
    while j >= 0 and board[row][j] == checker:
        count += 1
        j -= 1
    # Check right
    j = col + 1
    while j < cols and board[row][j] == checker:
        count += 1
        j += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    # Check up
    i = row - 1
    while i >= 0 and board[i][col] == checker:
        count += 1
        i -= 1
    # Check down
    i = row + 1
    while i < rows and board[i][col] == checker:
        count += 1
        i += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Check up-left
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0 and board[i][j] == checker:
        count += 1
        i -= 1
        j -= 1
    # Check down-right
    i, j = row + 1, col + 1
    while i < rows and j < cols and board[i][j] == checker:
        count += 1
        i += 1
        j += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    i, j = row - 1, col + 1
    while i >= 0 and j < cols and board[i][j] == checker:
        count += 1
        i -= 1
        j += 1
    # Check down-left
    i, j = row + 1, col - 1
    while i < rows and j >= 0 and board[i][j] == checker:
        count += 1
        i += 1
        j -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False


def check_draw(board, rows, cols):
    """
    Check if the board is completely filled (draw condition).
    
    Args:
        board: The current game board
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
    
    # Get the list of checkers for the number of players
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board, COLUMNS)
    
    # Game loop
    while True:
        current_checker = player_checkers[current_player_index]
        print(f"Player {current_checker}, please enter a column: ", end="")
        
        # Get valid input
        col = get_valid_input(COLUMNS)
        
        # Check if column is full
        if not can_place_checker(board, col, ROWS):
            print("This column is full. Please try another column.")
            continue
        
        # Place the checker
        row = place_checker(board, col, current_checker, ROWS)
        
        # Print the board
        print_board(board, COLUMNS)
        
        # Check for win
        if check_win(board, row, col, current_checker, ROWS, COLUMNS):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if check_draw(board, ROWS, COLUMNS):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
