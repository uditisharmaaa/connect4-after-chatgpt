import os
import random

# Game constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

def initialize_board(rows, cols):
    """
    Initialize a board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the board
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board, cols):
    """
    Print the board to the console.
    
    Args:
        board: The game board (2D list)
        cols: Number of columns in the board
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(65 + col)} ", end=" ")
    print()
    
    # Print top border
    print("+" + "+".join(["---"] * cols) + "+")
    
    # Print rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+" + "+".join(["---"] * cols) + "+")

def get_valid_column(cols):
    """
    Get a valid column input from the player.
    
    Args:
        cols: Number of columns in the board
    
    Returns:
        The column index (0-based)
    """
    while True:
        user_input = input().strip().upper()
        
        # Validate input
        if len(user_input) != 1:
            print(f"Invalid input. Please enter a single letter (A-{chr(65 + cols - 1)}):")
            continue
        
        if not user_input.isalpha():
            print(f"Invalid input. Please enter a letter (A-{chr(65 + cols - 1)}):")
            continue
        
        col_index = ord(user_input) - ord('A')
        
        if col_index < 0 or col_index >= cols:
            print(f"Invalid input. Please enter a letter (A-{chr(65 + cols - 1)}):")
            continue
        
        return col_index

def place_checker(board, col, checker, rows, cols):
    """
    Place a checker in the specified column.
    
    Args:
        board: The game board (2D list)
        col: Column index (0-based)
        checker: The player's checker character
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        True if the checker was placed successfully, False otherwise
    """
    # Find the lowest empty cell in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    return False

def check_win(board, rows, cols, checker):
    """
    Check if the current player has won.
    
    Args:
        board: The game board (2D list)
        rows: Number of rows in the board
        cols: Number of columns in the board
        checker: The player's checker character
    
    Returns:
        True if the player has won, False otherwise
    """
    # Check horizontal
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False

def is_board_full(board, rows, cols):
    """
    Check if the board is full (draw condition).
    
    Args:
        board: The game board (2D list)
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
    
    # Get player checkers
    players = [PLAYER_CHECKERS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board, COLUMNS)
    print(f"Player {players[current_player_index]}, please enter a column:")
    
    # Game loop
    while True:
        col = get_valid_column(COLUMNS)
        checker = players[current_player_index]
        
        # Try to place the checker
        if not place_checker(board, col, checker, ROWS, COLUMNS):
            print(f"Column is full. Please choose another column:")
            continue
        
        # Print the updated board
        print_board(board, COLUMNS)
        
        # Check for win
        if check_win(board, ROWS, COLUMNS, checker):
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if is_board_full(board, ROWS, COLUMNS):
            print("It's a draw!")
            break
        
        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        print(f"Player {players[current_player_index]}, please enter a column:")

def main():
    """
    Entry point for the Connect 4 game.
    """
    play_game()

if __name__ == "__main__":
    main()
