import os
import random

# Global constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the game board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the game board
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Print the game board with column labels and formatting.
    
    Args:
        board: The game board to print
    """
    os.system('clear')
    cols = len(board[0])
    rows = len(board)
    
    # Print column labels
    print("  ", end="")
    for col in range(cols):
        print(chr(ord('A') + col) + "   ", end="")
    print()
    
    # Print top border
    print("+---" * cols + "+")
    
    # Print each row
    for row in range(rows):
        print("|", end="")
        for col in range(cols):
            print(" " + board[row][col] + " |", end="")
        print()
        print("+---" * cols + "+")


def get_column_input(num_cols, current_player_checker):
    """
    Get valid column input from the current player.
    
    Args:
        num_cols: Number of columns on the board
        current_player_checker: The checker symbol of the current player
    
    Returns:
        The column index (0-based) where the player wants to place their checker
    """
    while True:
        user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col_index = ord(user_input) - ord('A')
        
        if col_index < 0 or col_index >= num_cols:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")
            continue
        
        return col_index


def place_checker(board, col, player_checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The game board
        col: The column index where the checker should be placed
        player_checker: The checker symbol to place
    
    Returns:
        True if the checker was placed successfully, False if the column is full
    """
    rows = len(board)
    
    # Find the lowest empty space in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_checker
            return True
    
    # Column is full
    print("Column is full. Please choose another column.")
    return False


def check_win(board, row, col, player_checker):
    """
    Check if the current player has won after placing a checker at (row, col).
    
    Args:
        board: The game board
        row: The row index where the checker was placed
        col: The column index where the checker was placed
        player_checker: The checker symbol of the player
    
    Returns:
        True if the player has won, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Directions: horizontal, vertical, diagonal (top-left to bottom-right), diagonal (top-right to bottom-left)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dx, dy in directions:
        count = 1  # Count the current checker
        
        # Check in the positive direction
        x, y = row + dx, col + dy
        while 0 <= x < rows and 0 <= y < cols and board[x][y] == player_checker:
            count += 1
            x += dx
            y += dy
        
        # Check in the negative direction
        x, y = row - dx, col - dy
        while 0 <= x < rows and 0 <= y < cols and board[x][y] == player_checker:
            count += 1
            x -= dx
            y -= dy
        
        if count >= WIN_LENGTH:
            return True
    
    return False


def check_draw(board):
    """
    Check if the board is full (draw condition).
    
    Args:
        board: The game board
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLUMNS)
    
    # Get player checkers based on number of players
    player_checkers = PLAYER_CHECKERS[:NUM_PLAYERS]
    
    # Select a random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_player_checker = player_checkers[current_player_index]
        
        # Get valid column input from player
        valid_placement = False
        while not valid_placement:
            col = get_column_input(COLUMNS, current_player_checker)
            valid_placement = place_checker(board, col, current_player_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        rows = len(board)
        for row in range(rows):
            if board[row][col] == current_player_checker:
                if check_win(board, row, col, current_player_checker):
                    print(f"Player {current_player_checker} won!")
                    return
        
        # Check for draw
        if check_draw(board):
            print("Draw! The board is full.")
            return
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
