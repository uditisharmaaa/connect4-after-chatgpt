import os
import random

# Game configuration constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Available player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the game board with all empty cells (whitespaces).
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the board
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Print the current state of the board with column labels and formatting.
    
    Args:
        board: The game board (2D list)
    """
    os.system("clear")
    
    rows = len(board)
    cols = len(board[0])
    
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


def get_valid_column_input(board, player_checker):
    """
    Get and validate column input from the player.
    Keep asking until valid input is provided.
    
    Args:
        board: The game board (2D list)
        player_checker: The current player's checker symbol
    
    Returns:
        The column index (0-based) where the player wants to place their checker
    """
    cols = len(board[0])
    
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        # Validate input length
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Validate input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - ord("A")
        
        # Validate column is within bounds
        if col < 0 or col >= cols:
            print(f"Invalid input. Please enter a letter between A and {chr(65 + cols - 1)}.")
            continue
        
        # Validate column is not full
        if board[0][col] != " ":
            print("This column is full. Please choose another column.")
            continue
        
        return col


def place_checker(board, col, checker):
    """
    Place a checker in the specified column at the lowest available row.
    
    Args:
        board: The game board (2D list)
        col: The column index (0-based) where to place the checker
        checker: The checker symbol to place
    
    Returns:
        The row index (0-based) where the checker was placed, or -1 if column is full
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    
    return -1


def check_win(board, row, col, checker):
    """
    Check if the player has won after placing a checker at (row, col).
    Checks horizontally, vertically, and diagonally.
    
    Args:
        board: The game board (2D list)
        row: The row index of the last placed checker
        col: The column index of the last placed checker
        checker: The checker symbol to check for
    
    Returns:
        True if the player has won, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Direction vectors: horizontal, vertical, diagonal /, diagonal \
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, -1),  # Diagonal /
        (1, 1)    # Diagonal \
    ]
    
    for dr, dc in directions:
        count = 1
        
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
        
        # Check if we have 4 or more in a row
        if count >= WIN_LENGTH:
            return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely full (draw condition).
    
    Args:
        board: The game board (2D list)
    
    Returns:
        True if the board is full, False otherwise
    """
    return all(cell != " " for cell in board[0])


def play_game():
    """
    Main game loop that orchestrates the Connect 4 game.
    """
    # Initialize the board
    board = initialize_board(BOARD_ROWS, BOARD_COLS)
    
    # Get player checkers
    players = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Main game loop
    while True:
        # Get current player's checker
        current_checker = players[current_player_idx]
        
        # Get valid column input from player
        col = get_valid_column_input(board, current_checker)
        
        # Place the checker
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
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
