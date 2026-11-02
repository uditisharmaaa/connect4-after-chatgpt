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
    Initialize the board with all empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the game board
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board, cols):
    """
    Print the current state of the board.
    
    Args:
        board: The 2D list representing the game board
        cols: Number of columns in the board
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print top border
    print(" +", end="")
    for _ in range(cols):
        print("---+", end="")
    print()
    
    # Print each row
    for row in board:
        print(" |", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        
        print(" +", end="")
        for _ in range(cols):
            print("---+", end="")
        print()


def get_column_input(cols, board):
    """
    Get and validate the column input from the player.
    
    Args:
        cols: Number of columns in the board
        board: The 2D list representing the game board
    
    Returns:
        The column index (0-based) where the player wants to place their checker
    """
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        
        # Validate input length
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Validate input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Validate column is within board bounds
        if col_index < 0 or col_index >= cols:
            print(f"Invalid input. Please enter a letter between A and {chr(65 + cols - 1)}.")
            continue
        
        # Validate column is not full
        if board[0][col_index] != " ":
            print("This column is full. Please choose another column.")
            continue
        
        return col_index


def place_checker(board, col, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The 2D list representing the game board
        col: The column index where the checker should be placed
        checker: The checker symbol to place
    
    Returns:
        The row index where the checker was placed, or -1 if placement failed
    """
    rows = len(board)
    
    # Find the lowest available row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    
    return -1


def check_win(board, row, col, checker, rows, cols):
    """
    Check if the current player has won the game.
    
    Args:
        board: The 2D list representing the game board
        row: The row index of the last placed checker
        col: The column index of the last placed checker
        checker: The checker symbol to check for
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        True if the player has won, False otherwise
    """
    # Directions: horizontal, vertical, and two diagonals
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal (top-left to bottom-right)
        (1, -1)   # Diagonal (top-right to bottom-left)
    ]
    
    for dx, dy in directions:
        count = 1
        
        # Check in positive direction
        x, y = row + dx, col + dy
        while 0 <= x < rows and 0 <= y < cols and board[x][y] == checker:
            count += 1
            x += dx
            y += dy
        
        # Check in negative direction
        x, y = row - dx, col - dy
        while 0 <= x < rows and 0 <= y < cols and board[x][y] == checker:
            count += 1
            x -= dx
            y -= dy
        
        # If we have 4 or more in a row, player wins
        if count >= WIN_LENGTH:
            return True
    
    return False


def check_draw(board, cols):
    """
    Check if the game is a draw (board is full).
    
    Args:
        board: The 2D list representing the game board
        cols: Number of columns in the board
    
    Returns:
        True if the board is full, False otherwise
    """
    for col in range(cols):
        if board[0][col] == " ":
            return False
    return True


def play_game():
    """
    Main game loop for Connect 4.
    """
    rows = ROWS
    cols = COLUMNS
    num_players = NUM_PLAYERS
    
    # Validate parameters
    if cols > 26:
        print("Error: Maximum 26 columns allowed.")
        return
    if num_players < 2 or num_players > 5:
        print("Error: Number of players must be between 2 and 5.")
        return
    
    # Initialize the board
    board = initialize_board(rows, cols)
    
    # Get player checkers
    player_checkers = CHECKERS[:num_players]
    
    # Randomly select the first player
    current_player = random.randint(0, num_players - 1)
    
    # Print initial board
    print_board(board, cols)
    print(f"Player {player_checkers[current_player]} starts the game!")
    input("Press Enter to continue...")
    
    # Game loop
    game_over = False
    
    while not game_over:
        print_board(board, cols)
        current_checker = player_checkers[current_player]
        print(f"Player {current_checker}, please enter a column:")
        
        # Get valid column input
        col = get_column_input(cols, board)
        
        # Place the checker
        row = place_checker(board, col, current_checker)
        
        # Check for win
        if check_win(board, row, col, current_checker, rows, cols):
            print_board(board, cols)
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board, cols):
            print_board(board, cols)
            print("The game is a draw!")
            game_over = True
        else:
            # Move to next player
            current_player = (current_player + 1) % num_players


if __name__ == "__main__":
    play_game()
