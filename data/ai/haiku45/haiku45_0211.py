import os
import random

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ['X', 'O', 'V', 'H', 'M']


def create_board(rows, cols):
    """
    Create and initialize the game board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the game board
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Print the current state of the game board with formatting.
    
    Args:
        board: The game board to print
    """
    os.system('clear')
    cols = len(board[0])
    rows = len(board)
    
    # Print column labels
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(65 + col)} ", end=" ")
    print()
    
    # Print board with borders
    for row in range(rows):
        print("+---" * cols + "+")
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    print("+---" * cols + "+")


def get_column_input(board, player_checker):
    """
    Get and validate column input from the player.
    
    Args:
        board: The game board
        player_checker: The checker symbol for the current player
    
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
        col = ord(user_input) - ord('A')
        
        # Validate column is within bounds
        if col < 0 or col >= cols:
            print(f"Invalid column. Please enter a letter between A and {chr(65 + cols - 1)}.")
            continue
        
        # Validate column is not full
        if board[0][col] != ' ':
            print("Column is full. Please choose another column.")
            continue
        
        return col


def place_checker(board, col, checker):
    """
    Place a checker in the specified column at the lowest available row.
    
    Args:
        board: The game board
        col: The column index where the checker should be placed
        checker: The checker symbol to place
    
    Returns:
        The row index where the checker was placed, or -1 if placement failed
    """
    rows = len(board)
    for row in range(rows - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1


def check_winner(board, row, col, checker):
    """
    Check if the player has won by placing a checker at the given position.
    
    Args:
        board: The game board
        row: The row where the checker was placed
        col: The column where the checker was placed
        checker: The checker symbol that was placed
    
    Returns:
        True if the player has won, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    
    # Directions: horizontal, vertical, diagonal (down-right), diagonal (down-left)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
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
        
        # If we have 4 or more in a row, player has won
        if count >= WIN_LENGTH:
            return True
    
    return False


def check_draw(board):
    """
    Check if the board is completely filled (draw condition).
    
    Args:
        board: The game board
    
    Returns:
        True if the board is full, False otherwise
    """
    return all(board[0][col] != ' ' for col in range(len(board[0])))


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Create and initialize the board
    board = create_board(ROWS, COLS)
    
    # Select a random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get current player's checker
        current_checker = CHECKERS[current_player_index]
        
        # Get valid column input
        col = get_column_input(board, current_checker)
        
        # Place checker and get row
        row = place_checker(board, col, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_winner(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
