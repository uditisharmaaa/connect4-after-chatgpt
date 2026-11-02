import os
import random

# Constants
ROWS = 6
COLS = 7
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]
MAX_PLAYERS = 5
NUM_PLAYERS = 2


def initialize_board(rows, cols):
    """
    Initialize a board with given dimensions filled with empty spaces.
    
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
    Print the current state of the board in a formatted manner.
    
    Args:
        board: The game board to print
    """
    os.system('clear')
    cols = len(board[0])
    rows = len(board)
    
    # Print column headers
    print("  ", end="")
    for i in range(cols):
        print(f" {chr(65 + i)}  ", end="")
    print()
    
    # Print board with borders
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
        num_players: Total number of players
        current_player: Index of current player (0-based)
        cols: Number of columns in the board
    
    Returns:
        The column index (0-based) where the player wants to place their checker
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
            print(f"Invalid input. Please enter a column between A and {chr(65 + cols - 1)}.")
            continue
        
        return col_index


def place_checker(board, col, player_index):
    """
    Place a checker in the specified column for the given player.
    
    Args:
        board: The game board
        col: Column index (0-based)
        player_index: Index of the player (0-based)
    
    Returns:
        True if checker was successfully placed, False if column is full
    """
    rows = len(board)
    checker = CHECKERS[player_index]
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    print("This column is full. Please choose another column.")
    return False


def check_win(board, player_index):
    """
    Check if the given player has won the game.
    
    Args:
        board: The game board
        player_index: Index of the player to check (0-based)
    
    Returns:
        True if the player has 4 in a row, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    checker = CHECKERS[player_index]
    
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
        board: The game board
    
    Returns:
        True if board is full, False otherwise
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
    # Initialize board
    board = initialize_board(ROWS, COLS)
    
    # Select random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        # Get player input
        col = get_column_input(NUM_PLAYERS, current_player, COLS)
        
        # Try to place checker
        if not place_checker(board, col, current_player):
            # Column was full, player loses turn
            current_player = (current_player + 1) % NUM_PLAYERS
            print_board(board)
            continue
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_player):
            checker = CHECKERS[current_player]
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
