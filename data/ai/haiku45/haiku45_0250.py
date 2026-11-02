import os
import random

# Constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
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
        A 2D list representing the board with all spaces empty
    """
    board = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(" ")
        board.append(row)
    return board


def print_board(board, cols):
    """
    Print the game board in a formatted manner.
    
    Args:
        board: The 2D list representing the board
        cols: Number of columns in the board
    """
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(chr(ord('A') + col) + "   ", end="")
    print()
    
    # Print top border
    print("+---" * cols + "+")
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(" " + cell + " |", end="")
        print()
        print("+---" * cols + "+")


def get_valid_column(cols):
    """
    Get a valid column input from the player.
    
    Args:
        cols: Number of columns in the board
    
    Returns:
        The column index (0-based) chosen by the player
    """
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        
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


def place_checker(board, col, checker, rows, cols):
    """
    Place a checker in the specified column.
    
    Args:
        board: The 2D list representing the board
        col: The column index where the checker should be placed
        checker: The checker symbol (X, O, V, H, or M)
        rows: Number of rows in the board
        cols: Number of columns in the board
    
    Returns:
        True if the checker was placed successfully, False if the column is full
    """
    # Find the lowest empty space in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    # Column is full
    return False


def check_win(board, rows, cols, checker):
    """
    Check if the current player has won the game.
    
    Args:
        board: The 2D list representing the board
        rows: Number of rows in the board
        cols: Number of columns in the board
        checker: The checker symbol to check for a win
    
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
    Check if the board is completely full (draw condition).
    
    Args:
        board: The 2D list representing the board
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
    Main game loop that manages the Connect 4 game flow.
    """
    # Initialize the board
    board = initialize_board(BOARD_ROWS, BOARD_COLUMNS)
    
    # Get the list of player checkers based on number of players
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print the initial board
    print_board(board, BOARD_COLUMNS)
    
    # Game loop
    game_over = False
    while not game_over:
        current_player_checker = players[current_player_index]
        print(f"Player {current_player_checker}, please enter a column:")
        
        # Get a valid column from the player
        col = get_valid_column(BOARD_COLUMNS)
        
        # Try to place the checker
        if place_checker(board, col, current_player_checker, BOARD_ROWS, BOARD_COLUMNS):
            # Checker was placed successfully
            print_board(board, BOARD_COLUMNS)
            
            # Check if the current player won
            if check_win(board, BOARD_ROWS, BOARD_COLUMNS, current_player_checker):
                print(f"Player {current_player_checker} won!")
                game_over = True
            # Check if the board is full (draw)
            elif is_board_full(board, BOARD_ROWS, BOARD_COLUMNS):
                print("It's a draw!")
                game_over = True
            else:
                # Move to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            # Column is full, player loses the turn
            print("Column is full! You lose your turn.")
            print_board(board, BOARD_COLUMNS)
            
            # Move to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
