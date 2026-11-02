import os
import random

# Global constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """
    Initialize the Connect 4 board with all empty spaces.
    Returns a 2D list (list of rows) with dimensions ROWS x COLUMNS.
    """
    board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
    return board


def print_board(board):
    """
    Print the Connect 4 board to the console with proper formatting.
    Includes column labels (A, B, C, etc.) and borders.
    """
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLUMNS):
        print(chr(ord('A') + col) + "   ", end="")
    print()
    
    # Print each row with borders
    for row in range(ROWS):
        print("+---" * COLUMNS + "+")
        print("|", end="")
        for col in range(COLUMNS):
            print(" " + board[row][col] + " |", end="")
        print()
    print("+---" * COLUMNS + "+")


def get_column_input(current_player):
    """
    Get and validate the column input from the current player.
    Keeps asking until a valid column letter is provided.
    Returns the column index (0-based).
    """
    while True:
        try:
            user_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
            
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
            
            # Check if column is within bounds
            if col_index < 0 or col_index >= COLUMNS:
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + COLUMNS - 1)}.")
                continue
            
            return col_index
            
        except Exception:
            print("Invalid input. Please try again.")


def place_checker(board, col_index, checker):
    """
    Place a checker in the specified column.
    The checker falls to the lowest available row.
    Returns True if placement was successful, False if the column is full.
    """
    # Find the lowest empty row in the column (start from bottom)
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    
    # Column is full
    print("Column is full. You lose your turn.")
    return False


def check_winner(board, checker):
    """
    Check if the specified checker has won the game.
    A player wins with 4 in a row horizontally, vertically, or diagonally.
    Returns True if the player has won, False otherwise.
    """
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLUMNS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board):
    """
    Check if the board is completely full (draw condition).
    Returns True if the board is full, False otherwise.
    """
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """
    Main game loop for Connect 4.
    Handles initialization, player turns, win checking, and game flow.
    """
    # Initialize the board
    board = initialize_board()
    
    # Select a random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Main game loop
    while True:
        # Get current player's checker
        current_checker = CHECKERS[current_player_index]
        current_player_name = current_checker
        
        # Get valid column input from player
        col_index = get_column_input(current_player_name)
        
        # Attempt to place the checker
        if place_checker(board, col_index, current_checker):
            # Print updated board
            print_board(board)
            
            # Check if current player won
            if check_winner(board, current_checker):
                print(f"Player {current_player_name} won!")
                break
            
            # Check if the board is full (draw)
            if is_board_full(board):
                print("The board is full. It's a draw!")
                break
        else:
            # Column was full, player loses turn but doesn't re-input
            print_board(board)
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


def main():
    """
    Entry point for the Connect 4 game.
    """
    play_game()


if __name__ == "__main__":
    main()
