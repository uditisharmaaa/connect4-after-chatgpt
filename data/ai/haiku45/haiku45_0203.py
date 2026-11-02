import random
import os

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player symbols
SYMBOLS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the game board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the board
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board, cols):
    """
    Print the game board with proper formatting.
    
    Args:
        board: The game board (2D list)
        cols: Number of columns
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(65 + col)} ", end="")
    print()
    
    # Print board with borders
    for row in board:
        print("+---" * cols + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    
    print("+---" * cols + "+")


def get_player_input(cols):
    """
    Get valid column input from the player.
    
    Args:
        cols: Number of columns
    
    Returns:
        Column index (0-based) where the player wants to place their checker
    """
    while True:
        user_input = input().strip().upper()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col_index = ord(user_input) - ord('A')
        
        if col_index < 0 or col_index >= cols:
            print(f"Invalid input. Please enter a letter between A and {chr(65 + cols - 1)}.")
            continue
        
        return col_index


def place_checker(board, col, symbol, rows):
    """
    Place a checker in the specified column.
    
    Args:
        board: The game board (2D list)
        col: Column index where to place the checker
        symbol: Player's symbol
        rows: Number of rows
    
    Returns:
        True if placement was successful, False if column is full
    """
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = symbol
            return True
    
    return False


def check_winner(board, rows, cols, symbol):
    """
    Check if the given symbol has won the game.
    
    Args:
        board: The game board (2D list)
        rows: Number of rows
        cols: Number of columns
        symbol: Player's symbol to check
    
    Returns:
        True if the player has won, False otherwise
    """
    # Check horizontal
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + i][col - i] == symbol for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board, rows, cols):
    """
    Check if the board is completely full.
    
    Args:
        board: The game board (2D list)
        rows: Number of rows
        cols: Number of columns
    
    Returns:
        True if board is full, False otherwise
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
    # Initialize game
    board = initialize_board(ROWS, COLS)
    players = [SYMBOLS[i] for i in range(NUM_PLAYERS)]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board, COLS)
    print(f"Player {players[current_player_index]}, please enter a column:")
    
    # Game loop
    while True:
        col = get_player_input(COLS)
        
        # Try to place the checker
        if not place_checker(board, col, players[current_player_index], ROWS):
            print("This column is full. Please choose another column:")
            continue
        
        # Print the updated board
        print_board(board, COLS)
        
        # Check for winner
        if check_winner(board, ROWS, COLS, players[current_player_index]):
            print(f"Player {players[current_player_index]} won!")
            break
        
        # Check for draw
        if is_board_full(board, ROWS, COLS):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        print(f"Player {players[current_player_index]}, please enter a column:")


if __name__ == "__main__":
    play_game()
