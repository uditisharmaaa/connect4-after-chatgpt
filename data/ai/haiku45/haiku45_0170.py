import os
import random

# Constants for the game
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the game board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        A 2D list representing the board filled with spaces
    """
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board):
    """
    Print the Connect 4 board to the console.
    
    Args:
        board: The 2D list representing the game board
    """
    os.system('clear')
    
    cols = len(board[0])
    rows = len(board)
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print each row with borders
    for row in range(rows):
        print("+---" * cols + "+")
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    print("+---" * cols + "+")


def get_column_input(num_players, current_player, cols):
    """
    Get valid column input from the current player.
    
    Args:
        num_players: Number of players in the game
        current_player: Index of the current player (0-indexed)
        cols: Number of columns in the board
    
    Returns:
        The column index (0-indexed) where the player wants to place their checker
    """
    checker = CHECKERS[current_player]
    valid_input = False
    
    while not valid_input:
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
            print(f"Invalid column. Please enter a letter between A and {chr(65 + cols - 1)}.")
            continue
        
        valid_input = True
    
    return col_index


def place_checker(board, col, current_player):
    """
    Place a checker in the specified column.
    
    Args:
        board: The 2D list representing the game board
        col: The column index where the checker should be placed
        current_player: Index of the current player (0-indexed)
    
    Returns:
        True if the checker was successfully placed, False if the column is full
    """
    checker = CHECKERS[current_player]
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    print("This column is full. Please choose another column.")
    return False


def check_win(board, current_player):
    """
    Check if the current player has won the game.
    
    Args:
        board: The 2D list representing the game board
        current_player: Index of the current player (0-indexed)
    
    Returns:
        True if the current player has won, False otherwise
    """
    checker = CHECKERS[current_player]
    rows = len(board)
    cols = len(board[0])
    
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


def is_board_full(board):
    """
    Check if the board is completely full.
    
    Args:
        board: The 2D list representing the game board
    
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
    board = initialize_board(ROWS, COLS)
    
    # Randomly select the first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    print(f"Player {CHECKERS[current_player]} starts first!")
    input("Press Enter to continue...")
    
    game_over = False
    
    # Main game loop
    while not game_over:
        print_board(board)
        
        # Get valid column input from the current player
        col = get_column_input(NUM_PLAYERS, current_player, COLS)
        
        # Try to place the checker
        if place_checker(board, col, current_player):
            # Check if the current player has won
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {CHECKERS[current_player]} won!")
                game_over = True
            # Check if the board is full (draw)
            elif is_board_full(board):
                print_board(board)
                print("The board is full. It's a draw!")
                game_over = True
            else:
                # Move to the next player
                current_player = (current_player + 1) % NUM_PLAYERS
        # If placement failed, the player gets to try again (turn not lost)


if __name__ == "__main__":
    play_game()
