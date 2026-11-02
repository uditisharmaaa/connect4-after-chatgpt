import os
import random

# Constants for board dimensions and players
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def initialize_board(rows, cols):
    """
    Initialize the board with all empty cells (whitespaces).
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the Connect 4 board
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Print the Connect 4 board with proper formatting.
    
    Args:
        board: The 2D list representing the board
    """
    os.system('clear')
    cols = len(board[0])
    rows = len(board)
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print top border
    print("+", end="")
    for col in range(cols):
        print("---+", end="")
    print()
    
    # Print each row
    for row in range(rows):
        print("|", end="")
        for col in range(cols):
            print(" " + board[row][col] + " |", end="")
        print()
        
        # Print horizontal border
        print("+", end="")
        for col in range(cols):
            print("---+", end="")
        print()


def get_valid_input(board, num_players, current_player, checkers):
    """
    Get and validate user input for column selection.
    
    Args:
        board: The 2D list representing the board
        num_players: Number of players in the game
        current_player: Index of the current player (0-based)
        checkers: List of checker symbols for each player
    
    Returns:
        The column index (0-based) where the player wants to place their checker
    """
    cols = len(board[0])
    
    while True:
        user_input = input(f"Player {checkers[current_player]}, please enter a column: ").strip().upper()
        
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
            print(f"Invalid input. Please enter a column between A and {chr(ord('A') + cols - 1)}.")
            continue
        
        # Check if column is not full
        if board[0][col_index] != " ":
            print("Column is full. Please choose another column.")
            continue
        
        return col_index


def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The 2D list representing the board
        col_index: The column index (0-based) where to place the checker
        checker: The checker symbol to place
    
    Returns:
        The row index where the checker was placed, or -1 if placement failed
    """
    rows = len(board)
    
    # Find the lowest available row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    
    return -1


def check_win(board, row, col, checker):
    """
    Check if the last placed checker resulted in a win.
    
    Args:
        board: The 2D list representing the board
        row: The row index of the last placed checker
        col: The column index of the last placed checker
        checker: The checker symbol to check for win
    
    Returns:
        True if the player won, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Directions: horizontal, vertical, diagonal1, diagonal2
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal (top-left to bottom-right)
        (1, -1)   # Diagonal (top-right to bottom-left)
    ]
    
    for dr, dc in directions:
        count = 1  # Count the current checker
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= WIN_LENGTH:
            return True
    
    return False


def check_draw(board):
    """
    Check if the board is full (draw condition).
    
    Args:
        board: The 2D list representing the board
    
    Returns:
        True if the board is full, False otherwise
    """
    for col in range(len(board[0])):
        if board[0][col] == " ":
            return False
    return True


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLUMNS)
    
    # Get the checkers for the current number of players
    checkers = CHECKERS[:NUM_PLAYERS]
    
    # Select a random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board)
    
    # Main game loop
    while True:
        # Get valid input from current player
        col_index = get_valid_input(board, NUM_PLAYERS, current_player, checkers)
        
        # Place the checker
        row_index = place_checker(board, col_index, checkers[current_player])
        
        # Print the updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row_index, col_index, checkers[current_player]):
            print(f"Player {checkers[current_player]} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
