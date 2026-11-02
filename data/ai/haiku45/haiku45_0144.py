import os
import random

# Constants for board configuration
NUM_COLS = 7
NUM_ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Checker symbols for up to 5 players
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

def print_board(board):
    """
    Print the Connect 4 board in a formatted way.
    
    Args:
        board: The current game board
    """
    os.system('clear')
    
    rows = len(board)
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(chr(ord('A') + col), end="   ")
    print()
    
    # Print each row
    for row in range(rows):
        print("+---" * cols + "+")
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+---" * cols + "+")

def get_column_input(num_players, current_player, cols):
    """
    Get valid column input from the current player.
    
    Args:
        num_players: Total number of players
        current_player: Index of current player (0-based)
        cols: Number of columns in the board
    
    Returns:
        Column index (0-based) where the checker will be placed
    """
    checker = CHECKERS[current_player]
    
    while True:
        user_input = input(f"Player {checker}, please enter a column: ").strip().upper()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col_index = ord(user_input) - ord('A')
        
        if col_index < 0 or col_index >= cols:
            print(f"Invalid input. Please enter a column between A and {chr(ord('A') + cols - 1)}.")
            continue
        
        return col_index

def place_checker(board, col, current_player):
    """
    Place a checker in the specified column.
    
    Args:
        board: The current game board
        col: Column index (0-based)
        current_player: Index of current player (0-based)
    
    Returns:
        True if checker was placed successfully, False if column is full
    """
    rows = len(board)
    checker = CHECKERS[current_player]
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    return False

def check_win(board, current_player):
    """
    Check if the current player has won the game.
    
    Args:
        board: The current game board
        current_player: Index of current player (0-based)
    
    Returns:
        True if the current player has 4 in a row, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    checker = CHECKERS[current_player]
    
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

def check_draw(board):
    """
    Check if the board is full (draw condition).
    
    Args:
        board: The current game board
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def get_next_player(current_player, num_players):
    """
    Get the index of the next player.
    
    Args:
        current_player: Index of current player (0-based)
        num_players: Total number of players
    
    Returns:
        Index of next player (0-based)
    """
    return (current_player + 1) % num_players

def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(NUM_ROWS, NUM_COLS)
    
    # Select a random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get column input from current player
        col = get_column_input(NUM_PLAYERS, current_player, NUM_COLS)
        
        # Try to place the checker
        if not place_checker(board, col, current_player):
            print("That column is full. Please choose another column.")
            continue
        
        # Print the updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_player):
            checker = CHECKERS[current_player]
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player = get_next_player(current_player, NUM_PLAYERS)

if __name__ == "__main__":
    play_game()
