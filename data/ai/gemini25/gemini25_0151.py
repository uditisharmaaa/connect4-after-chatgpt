import os
import random
import sys
import math

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_SEQUENCE_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# --- Helper Functions ---

def clear_screen():
    """Clears the console screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board, initialized with spaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col_idx in range(num_cols):
        print(f" {chr(ord('A') + col_idx)} ", end="")
    print()

    # Print board content
    for r in range(num_rows):
        print("+", end="")
        for _ in range(num_cols):
            print("---+", end="")
        print()
        print("|", end="")
        for c in range(num_cols):
            print(f" {board[r][c]} |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for _ in range(num_cols):
        print("---+", end="")
    print()

def get_player_input(current_player_checker, board):
    """
    Prompts the current player for a column choice and validates the input.

    Args:
        current_player_checker (str): The checker symbol of the current player.
        board (list): The game board.

    Returns:
        int: The 0-indexed column chosen by the player.
    """
    num_cols = len(board[0])
    while True:
        try:
            player_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
            if not player_input.isalpha() or len(player_input) != 1:
                print("Invalid input. Please enter a single uppercase letter (e.g., A, B, C).")
                continue

            col_char_code = ord(player_input)
            col_idx = col_char_code - ord('A')

            if not (0 <= col_idx < num_cols):
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")
                continue
            
            # Check if column is full
            if board[0][col_idx] != " ":
                print("Column is full. Please choose another column.")
                continue

            return col_idx
        except Exception:
            print("An unexpected error occurred with your input. Please try again.")

def place_checker(board, col_idx, checker):
    """
    Places a checker in the lowest available space of the specified column.

    Args:
        board (list): The game board.
        col_idx (int): The 0-indexed column to place the checker.
        checker (str): The checker symbol to place.

    Returns:
        bool: True if the checker was placed successfully, False if the column was full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return True
    return False # Should not be reached if column full check is done before calling this

def check_win(board, checker):
    """
    Checks if the given player has won the game.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the player to check for a win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check vertical
    for c in range(num_cols):
        for r in range(num_rows - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r + i][c] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(num_rows - WIN_SEQUENCE_LENGTH + 1):
        for c in range(num_cols - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_SEQUENCE_LENGTH - 1, num_rows):
        for c in range(num_cols - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    num_cols = len(board[0])
    for c in range(num_cols):
        if board[0][c] == " ":  # If any space in the top row is empty, game is not a draw yet
            return False
    return True

# --- Main Game Logic ---

def main():
    """
    Main function to run the Connect 4 game.
    """
    clear_screen()
    
    # Initialize game elements
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Select checkers based on NUM_PLAYERS
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: Number of players must be between 2 and 5.")
        sys.exit(1)
    
    player_checkers = PLAYER_CHECKERS[:NUM_PLAYERS]
    
    # Randomly choose the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player_checker = player_checkers[current_player_index]

    game_over = False

    while not game_over:
        clear_screen()
        print_board(board)

        col_idx = get_player_input(current_player_checker, board)
        
        # Place the checker
        place_checker(board, col_idx, current_player_checker)

        # Check for win
        if check_win(board, current_player_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_player_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! The board is full.")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            current_player_checker = player_checkers[current_player_index]

    print("\nGame Over!")

if __name__ == "__main__":
    main()
