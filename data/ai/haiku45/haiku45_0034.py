import os
import random

# Global constants
COLUMNS = 7
ROWS = 6
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def initialize_board():
    """
    Creates and returns a 2D board initialized with empty spaces.
    
    Returns:
        list: A 2D list representing the game board with dimensions ROWS x COLUMNS
    """
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board


def print_board(board):
    """
    Prints the game board in a formatted manner with column labels and grid lines.
    
    Args:
        board (list): The 2D game board to print
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLUMNS):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print each row with grid lines
    for row in range(ROWS):
        print("+---" * COLUMNS + "+")
        print("|", end="")
        for col in range(COLUMNS):
            print(f" {board[row][col]} |", end="")
        print()
    
    print("+---" * COLUMNS + "+")


def get_valid_column(current_player):
    """
    Gets a valid column input from the current player.
    Validates that the input is a single letter, within board range, and column is not full.
    
    Args:
        current_player (str): The checker symbol of the current player
    
    Returns:
        int: The column index (0-based) where the checker will be placed
    """
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        
        # Validate input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Validate input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - ord('A')
        
        # Validate column is within board range
        if col < 0 or col >= COLUMNS:
            print(f"Invalid input. Please enter a letter between A and {chr(65 + COLUMNS - 1)}.")
            continue
        
        # Validate column is not full
        if board[0][col] != " ":
            print("This column is full. Please choose another column.")
            continue
        
        return col


def place_checker(board, col, checker):
    """
    Places a checker in the specified column at the lowest available row.
    
    Args:
        board (list): The 2D game board
        col (int): The column index where the checker will be placed
        checker (str): The checker symbol to place
    
    Returns:
        int: The row index where the checker was placed
    """
    # Find the lowest empty row in the column (start from bottom)
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    
    return -1  # Column is full (should not happen due to validation)


def check_win(board, row, col, checker):
    """
    Checks if the player has won by checking horizontal, vertical, and diagonal directions.
    
    Args:
        board (list): The 2D game board
        row (int): The row index of the last placed checker
        col (int): The column index of the last placed checker
        checker (str): The checker symbol to check for
    
    Returns:
        bool: True if the player has won, False otherwise
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
    Checks if there are 4 checkers in a row in a specific direction.
    
    Args:
        board (list): The 2D game board
        row (int): The row index of the checker to start from
        col (int): The column index of the checker to start from
        checker (str): The checker symbol to look for
        row_delta (int): Direction along rows (-1, 0, or 1)
        col_delta (int): Direction along columns (-1, 0, or 1)
    
    Returns:
        bool: True if 4 checkers are found in the specified direction, False otherwise
    """
    count = 1  # Count the placed checker itself
    
    # Check in positive direction
    r, c = row + row_delta, col + col_delta
    while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
        count += 1
        r += row_delta
        c += col_delta
    
    # Check in negative direction
    r, c = row - row_delta, col - col_delta
    while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
        count += 1
        r -= row_delta
        c -= col_delta
    
    return count >= WIN_LENGTH


def is_board_full(board):
    """
    Checks if the board is completely full.
    
    Args:
        board (list): The 2D game board
    
    Returns:
        bool: True if the board is full, False otherwise
    """
    for col in range(COLUMNS):
        if board[0][col] == " ":
            return False
    return True


def play_game():
    """
    Main game loop that manages the Connect 4 game flow.
    Initializes the board, randomly selects the first player, and handles turns until win or draw.
    """
    # Initialize board and select starting player
    board = initialize_board()
    player_checkers = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_checker = player_checkers[current_player_index]
        
        # Get valid column and place checker
        col = get_valid_column(current_checker)
        row = place_checker(board, col, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % PLAYERS


if __name__ == "__main__":
    play_game()
