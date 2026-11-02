import os
import random

# Constants for board configuration
COLUMNS = 7
ROWS = 6
WIN_LENGTH = 4

# Available player checkers
CHECKERS = ["X", "O", "V", "H", "M"]

# Number of players
NUM_PLAYERS = 2


def initialize_board(rows, columns):
    """
    Initialize the game board with empty spaces.
    
    Args:
        rows: Number of rows in the board
        columns: Number of columns in the board
    
    Returns:
        A 2D list representing the board
    """
    board = [[" " for _ in range(columns)] for _ in range(rows)]
    return board


def print_board(board, columns):
    """
    Print the board to the console with proper formatting.
    
    Args:
        board: The game board
        columns: Number of columns
    """
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for i in range(columns):
        print(f" {chr(65 + i)} ", end="")
    print()
    
    # Print top border
    print("+", end="")
    for _ in range(columns):
        print("---+", end="")
    print()
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        
        # Print row separator
        print("+", end="")
        for _ in range(columns):
            print("---+", end="")
        print()


def is_valid_input(user_input, columns):
    """
    Validate the player's input.
    
    Args:
        user_input: The input provided by the player
        columns: Number of columns in the board
    
    Returns:
        True if input is valid, False otherwise
    """
    # Check if input is a single character
    if len(user_input) != 1:
        return False
    
    # Check if input is uppercase letter
    if not user_input.isupper():
        return False
    
    # Check if input is within valid column range
    column_index = ord(user_input) - ord('A')
    if column_index < 0 or column_index >= columns:
        return False
    
    return True


def get_player_move(board, player_checker, columns):
    """
    Get a valid move from the player.
    
    Args:
        board: The game board
        player_checker: The checker symbol of the current player
        columns: Number of columns in the board
    
    Returns:
        The column index (0-based) where the player wants to place their checker
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip()
        
        # Validate input format
        if not is_valid_input(user_input, columns):
            print("Invalid input. Please enter a single uppercase letter within the board range.")
            continue
        
        column_index = ord(user_input) - ord('A')
        
        # Check if column is full
        if board[0][column_index] != " ":
            print("Column is full. Please choose another column.")
            continue
        
        return column_index


def place_checker(board, column, player_checker, rows):
    """
    Place a checker in the specified column.
    
    Args:
        board: The game board
        column: Column index where the checker should be placed
        player_checker: The checker symbol of the player
        rows: Number of rows in the board
    
    Returns:
        True if placement was successful, False otherwise
    """
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = player_checker
            return True
    
    return False


def check_win(board, player_checker, rows, columns):
    """
    Check if the current player has won the game.
    
    Args:
        board: The game board
        player_checker: The checker symbol of the player to check
        rows: Number of rows in the board
        columns: Number of columns in the board
    
    Returns:
        True if the player has won, False otherwise
    """
    # Check horizontal wins
    for row in range(rows):
        for col in range(columns - WIN_LENGTH + 1):
            if all(board[row][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical wins
    for col in range(columns):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal wins (top-left to bottom-right)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(columns - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal wins (top-right to bottom-left)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, columns):
            if all(board[row + i][col - i] == player_checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board, rows, columns):
    """
    Check if the board is completely filled (draw condition).
    
    Args:
        board: The game board
        rows: Number of rows in the board
        columns: Number of columns in the board
    
    Returns:
        True if the board is full, False otherwise
    """
    for row in range(rows):
        for col in range(columns):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """
    Main game loop for Connect 4.
    """
    # Initialize the board
    board = initialize_board(ROWS, COLUMNS)
    
    # Select random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board, COLUMNS)
    
    game_over = False
    
    # Main game loop
    while not game_over:
        # Get current player's checker
        current_player_checker = CHECKERS[current_player_index]
        
        # Get player's move
        column = get_player_move(board, current_player_checker, COLUMNS)
        
        # Place the checker on the board
        place_checker(board, column, current_player_checker, ROWS)
        
        # Print updated board
        print_board(board, COLUMNS)
        
        # Check if current player won
        if check_win(board, current_player_checker, ROWS, COLUMNS):
            print(f"Player {current_player_checker} won!")
            game_over = True
        # Check if board is full (draw)
        elif is_board_full(board, ROWS, COLUMNS):
            print("It's a draw!")
            game_over = True
        else:
            # Switch to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
