import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    # os.system('clear') works on Linux/Unix.
    # For Windows, it would be os.system('cls').
    # Since the assignment specifies Linux/Unix, 'clear' is sufficient.
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
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    num_cols = len(board[0])
    num_rows = len(board)

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for i in range(num_cols):
        print(f" {chr(ord('A') + i)} ", end="")
    print()

    # Print the board with separators
    for r in range(num_rows):
        print("+", end="")
        for _ in range(num_cols):
            print("---+", end="")
        print()

        print("|", end="")
        for c in range(num_cols):
            print(f" {board[r][c]} |", end="")
        print()

    # Print the bottom separator
    print("+", end="")
    for _ in range(num_cols):
        print("---+", end="")
    print()

def get_valid_column_input(board, current_player_char):
    """
    Prompts the current player to enter a column and validates the input.

    Args:
        board (list): The 2D list representing the game board.
        current_player_char (str): The checker character of the current player.

    Returns:
        int: The 0-based index of the chosen column.
    """
    num_cols = len(board[0])
    while True:
        try:
            prompt = f"Player {current_player_char}, please enter a column: "
            user_input = input(prompt).strip().upper()

            if not user_input:
                print("Input cannot be empty. Please enter a column letter.")
                continue

            if len(user_input) != 1:
                print("Invalid input. Please enter a single column letter (e.g., A, B, C).")
                continue

            col_index = ord(user_input) - ord('A')

            if not (0 <= col_index < num_cols):
                print(f"Column '{user_input}' is out of bounds. Please choose a column from A to {chr(ord('A') + num_cols - 1)}.")
                continue

            # Check if the column is full
            if board[0][col_index] != " ":
                print(f"Column '{user_input}' is full. Please choose another column.")
                continue

            return col_index
        except TypeError: # This might catch cases where ord() receives non-string
            print("Invalid input. Please enter a valid column letter.")
        except Exception: # Catch any other unexpected errors
            print("An unexpected error occurred. Please try again.")


def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-based index of the column to drop the checker into.
        checker (str): The checker character to place.

    Returns:
        bool: True if the checker was successfully placed, False otherwise (column was full).
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Start from bottom row
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True
    return False # Should not happen if get_valid_column_input is used correctly

def check_win(board, checker):
    """
    Checks if the given player (checker) has won the game.

    Args:
        board (list): The 2D list representing the game board.
        checker (str): The checker character to check for a win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal win
    for r in range(num_rows):
        for c in range(num_cols - 3): # -3 because we need 4 consecutive
            if all(board[r][c+i] == checker for i in range(4)):
                return True

    # Check vertical win
    for r in range(num_rows - 3):
        for c in range(num_cols):
            if all(board[r+i][c] == checker for i in range(4)):
                return True

    # Check positive diagonal win (bottom-left to top-right)
    for r in range(3, num_rows): # Start from row 3 upwards
        for c in range(num_cols - 3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True

    # Check negative diagonal win (top-left to bottom-right)
    for r in range(num_rows - 3):
        for c in range(num_cols - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    num_cols = len(board[0])
    for c in range(num_cols):
        if board[0][c] == " ": # If top row of any column is empty, not a draw
            return False
    return True

def main():
    """
    Main function to run the Connect 4 game.
    """
    # Initialize game
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Get player checkers based on NUM_PLAYERS
    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly choose the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    clear_screen()
    print_board(board)
    
    while not game_over:
        current_player_char = player_checkers[current_player_index]
        
        col_index = get_valid_column_input(board, current_player_char)
        
        drop_checker(board, col_index, current_player_char)
        
        clear_screen()
        print_board(board)
        
        if check_win(board, current_player_char):
            print(f"Player {current_player_char} won!")
            game_over = True
        elif check_draw(board):
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
