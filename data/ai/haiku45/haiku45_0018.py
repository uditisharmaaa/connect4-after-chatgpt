import os
import random

# Global constants
BOARD_COLS = 7
BOARD_ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """
    Initialize the game board with all cells containing whitespace.
    
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
    Print the current state of the game board.
    
    Args:
        board: The 2D list representing the game board
    """
    os.system('clear')
    
    cols = len(board[0])
    rows = len(board)
    
    # Print column labels
    print("  ", end="")
    for col in range(cols):
        print(chr(ord('A') + col), end="   ")
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


def get_valid_input(board, num_players, current_player_index):
    """
    Get and validate user input for column selection.
    
    Args:
        board: The current game board
        num_players: Number of players in the game
        current_player_index: Index of the current player
    
    Returns:
        The column index (0-indexed) where the player wants to place their checker
    """
    cols = len(board[0])
    checker = PLAYER_CHECKERS[current_player_index]
    
    while True:
        try:
            user_input = input(f"Player {checker}, please enter a column: ").strip().upper()
            
            # Check if input is a single character
            if len(user_input) != 1:
                print("Invalid input. Please enter a single letter.")
                continue
            
            # Check if input is a letter
            if not user_input.isalpha():
                print("Invalid input. Please enter a letter.")
                continue
            
            # Convert letter to column index
            col_index = ord(user_input) - ord('A')
            
            # Check if column index is within bounds
            if col_index < 0 or col_index >= cols:
                print(f"Invalid input. Column must be between A and {chr(ord('A') + cols - 1)}.")
                continue
            
            # Check if column is full
            if board[0][col_index] != " ":
                print("Invalid input. This column is full.")
                continue
            
            return col_index
        
        except Exception as e:
            print("Invalid input. Please try again.")


def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column.
    
    Args:
        board: The current game board
        col_index: The column index (0-indexed) where the checker is placed
        checker: The checker symbol (X, O, V, H, or M)
    
    Returns:
        True if the checker was successfully placed, False otherwise
    """
    rows = len(board)
    
    # Find the lowest empty row in the column
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    
    return False


def check_win(board, checker):
    """
    Check if the specified checker has won the game.
    
    Args:
        board: The current game board
        checker: The checker symbol to check for a win
    
    Returns:
        True if the checker has won, False otherwise
    """
    rows = len(board)
    cols = len(board[0])
    win_length = WIN_LENGTH
    
    # Check horizontal
    for row in range(rows):
        for col in range(cols - win_length + 1):
            if all(board[row][col + i] == checker for i in range(win_length)):
                return True
    
    # Check vertical
    for col in range(cols):
        for row in range(rows - win_length + 1):
            if all(board[row + i][col] == checker for i in range(win_length)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(rows - win_length + 1):
        for col in range(cols - win_length + 1):
            if all(board[row + i][col + i] == checker for i in range(win_length)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(rows - win_length + 1):
        for col in range(win_length - 1, cols):
            if all(board[row + i][col - i] == checker for i in range(win_length)):
                return True
    
    return False


def check_draw(board):
    """
    Check if the game is a draw (board is full).
    
    Args:
        board: The current game board
    
    Returns:
        True if the board is full, False otherwise
    """
    return all(board[0][col] != " " for col in range(len(board[0])))


def play_game():
    """
    Main game loop for Connect 4.
    Handles initialization, player turns, win/draw checking, and game flow.
    """
    # Initialize the board
    board = initialize_board(BOARD_ROWS, BOARD_COLS)
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Main game loop
    while True:
        # Get valid column input from current player
        col_index = get_valid_input(board, NUM_PLAYERS, current_player_index)
        
        # Place the checker
        checker = PLAYER_CHECKERS[current_player_index]
        place_checker(board, col_index, checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
        
        # Check for draw
        if check_draw(board):
            print("Draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


# Run the game
if __name__ == "__main__":
    play_game()
