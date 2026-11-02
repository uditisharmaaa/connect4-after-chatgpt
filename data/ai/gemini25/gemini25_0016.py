import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_LENGTH = 4

# Player checkers (X, O, V, H, M)
CHECKERS = ['X', 'O', 'V', 'H', 'M']
PLAYER_CHECKERS = CHECKERS[:NUM_PLAYERS]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows on the board.
        cols (int): The number of columns on the board.

    Returns:
        list: A 2D list representing the board, initialized with spaces.
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    # Print column headers (A, B, C, ...)
    print("  " + "   ".join([chr(ord('A') + i) for i in range(NUM_COLS)]))
    
    # Print board rows
    for r in range(NUM_ROWS):
        print("+" + "---+" * NUM_COLS)
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+" + "---+" * NUM_COLS)

def get_column_input(player_checker):
    """
    Prompts the current player for a column input and validates it.

    Args:
        player_checker (str): The checker symbol of the current player.

    Returns:
        int: The 0-indexed column number if input is valid.
    """
    while True:
        try:
            col_char = input(f"Player {player_checker}, please enter a column: ").upper()
            if not col_char:
                print("Input cannot be empty. Please enter a column letter.")
                continue

            col_index = ord(col_char) - ord('A')

            if not (0 <= col_index < NUM_COLS):
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + NUM_COLS - 1)}.")
            else:
                return col_index
        except TypeError: # Should not happen with .upper() but good practice
            print("Invalid input. Please enter a single letter.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")

def place_checker(board, col, checker):
    """
    Places a checker in the specified column.

    Args:
        board (list): The game board.
        col (int): The 0-indexed column to place the checker.
        checker (str): The checker symbol to place.

    Returns:
        bool: True if the checker was placed successfully, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Iterate from bottom row up
        if board[r][col] == ' ':
            board[r][col] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check vertical
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - WIN_LENGTH + 1):
            if all(board[r + i][c] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_LENGTH + 1):
        for c in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_LENGTH - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is full, resulting in a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == ' ':
                return False  # Found an empty space, not a draw yet
    return True  # Board is full

# --- Main Game Logic ---

def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)
        
        valid_move = False
        while not valid_move:
            col_index = get_column_input(current_checker)
            if place_checker(board, col_index, current_checker):
                valid_move = True
            else:
                print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
                # Player does not lose turn for a full column

        print_board(board) # Print board after successful placement

        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        elif check_draw(board):
            print("It's a draw! The board is full.")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
