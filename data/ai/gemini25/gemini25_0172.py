import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4

# Checkers available
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYER_CHECKERS = CHECKERS[:NUM_PLAYERS]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
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
    clear_screen()
    
    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col in range(len(board[0])):
        print(f"{chr(ord('A') + col):3s}", end="")
    print()

    # Print board content
    for row in board:
        print("+---" * len(row) + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * len(board[0]) + "+")

def get_column_input(prompt):
    """
    Gets validated column input from the player.

    Args:
        prompt (str): The prompt message to display to the player.

    Returns:
        str: The uppercase letter representing the chosen column.
    """
    while True:
        user_input = input(prompt).strip().upper()
        if len(user_input) == 1 and 'A' <= user_input <= chr(ord('A') + NUM_COLS - 1):
            return user_input
        print(f"Invalid input. Please enter a column letter between A and {chr(ord('A') + NUM_COLS - 1)}.")

def get_column_index(column_char):
    """
    Converts a column character (e.g., 'A') to its integer index (e.g., 0).

    Args:
        column_char (str): The column character.

    Returns:
        int: The integer index of the column.
    """
    return ord(column_char) - ord('A')

def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The integer index of the column.
        checker (str): The checker symbol ('X', 'O', etc.).

    Returns:
        bool: True if the checker was placed successfully, False if the column is full.
    """
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False # Column is full

def check_win(board, checker):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check horizontal win
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[row][col + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical win
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - WIN_CONDITION + 1):
            if all(board[row + i][col] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right) win
    for row in range(NUM_ROWS - WIN_CONDITION + 1):
        for col in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (bottom-left to top-right) win
    for row in range(WIN_CONDITION - 1, NUM_ROWS):
        for col in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[row - i][col + i] == checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely filled, resulting in a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if board[row][col] == " ":
                return False
    return True

# --- Main Game Logic ---

def play_connect4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Initialize players and randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_checker = PLAYER_CHECKERS[current_player_index]
        
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        # Get and validate column input
        while True:
            col_char = get_column_input(f"Player {current_checker}, please enter a column: ")
            col_index = get_column_index(col_char)
            
            if drop_checker(board, col_index, current_checker):
                break # Valid move, break out of input loop
            else:
                print("Column is full. Please choose another column.")
        
        # Check for win
        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # End of game
    print("Game over!")
    sys.exit() # Terminate the program

# --- Run the game ---
if __name__ == "__main__":
    play_connect4()
