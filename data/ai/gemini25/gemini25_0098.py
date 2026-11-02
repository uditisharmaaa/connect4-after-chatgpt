import os
import random
import sys

# --- GLOBAL CONSTANTS ---
# Board dimensions (can be customized)
NUM_ROWS = 6
NUM_COLS = 7

# Number of players (can be customized, between 2 and 5)
NUM_PLAYERS = 2

# Checkers for players
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# Number of checkers needed to win
WIN_CONDITION = 4

# --- HELPER FUNCTIONS ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows in the board.
        cols (int): The number of columns in the board.

    Returns:
        list: A 2D list representing the game board, initialized with whitespaces.
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
    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_idx in range(len(board[0])):
        print(f"   {chr(ord('A') + col_idx)}", end="")
    print("\n" + "+---" * len(board[0]) + "+")

    # Print rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print("\n" + "+---" * len(board[0]) + "+")

def get_valid_column_input(current_player_checker, board):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker symbol of the current player.
        board (list): The current state of the game board.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    num_cols = len(board[0])
    while True:
        try:
            prompt = f"Player {current_player_checker}, please enter a column (A-{chr(ord('A') + num_cols - 1)}): "
            column_input = input(prompt).upper()

            # Validate input length and type
            if not column_input or len(column_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A).")
                continue

            # Convert column letter to 0-indexed integer
            col_idx = ord(column_input) - ord('A')

            # Validate column range
            if not (0 <= col_idx < num_cols):
                print(f"Invalid column. Please choose a column between A and {chr(ord('A') + num_cols - 1)}.")
                continue

            # Validate if the column is full
            if board[0][col_idx] != " ": # Check the top row of the chosen column
                print("That column is full. Please choose another column.")
                continue

            return col_idx

        except ValueError:
            print("Invalid input. Please enter a letter.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")


def drop_checker(board, col_idx, player_checker):
    """
    Drops the player's checker into the specified column.

    Args:
        board (list): The game board.
        col_idx (int): The 0-indexed column to drop the checker into.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the checker was successfully placed, False if the column was full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1): # Iterate from bottom to top
        if board[r][col_idx] == " ":
            board[r][col_idx] = player_checker
            return True
    return False # Column was full (should be caught by validation earlier, but good for robustness)

def check_win(board, player_checker):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal wins
    for r in range(num_rows):
        for c in range(num_cols - WIN_CONDITION + 1):
            if all(board[r][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical wins
    for c in range(num_cols):
        for r in range(num_rows - WIN_CONDITION + 1):
            if all(board[r + i][c] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal wins (positive slope: top-left to bottom-right)
    for r in range(num_rows - WIN_CONDITION + 1):
        for c in range(num_cols - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal wins (negative slope: top-right to bottom-left)
    for r in range(num_rows - WIN_CONDITION + 1):
        for c in range(WIN_CONDITION - 1, num_cols):
            if all(board[r + i][c - i] == player_checker for i in range(WIN_CONDITION)):
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
    # A draw occurs if the top row of all columns is filled
    for col_idx in range(len(board[0])):
        if board[0][col_idx] == " ":
            return False # Found an empty spot in the top row, so not a draw
    return True # All top spots are filled, game is a draw

# --- MAIN GAME LOGIC ---

def connect_four_game():
    """
    Main function to run the Connect 4 game.
    """
    # Initialize game
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if not (NUM_COLS >= WIN_CONDITION and NUM_ROWS >= WIN_CONDITION):
        print(f"Error: Board dimensions ({NUM_ROWS}x{NUM_COLS}) are too small for WIN_CONDITION ({WIN_CONDITION}).")
        sys.exit(1)
    if not (1 <= NUM_COLS <= 26):
        print("Error: NUM_COLS must be between 1 and 26 (for letter labels).")
        sys.exit(1)

    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS] # Select checkers based on NUM_PLAYERS

    # Randomly choose the first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    game_over = False

    while not game_over:
        clear_screen()
        print_board(board)

        current_player_checker = players[current_player_idx]

        # Get valid column input from current player
        col_to_drop = get_valid_column_input(current_player_checker, board)

        # Drop the checker
        drop_checker(board, col_to_drop, current_player_checker)

        # Check for win
        if check_win(board, current_player_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_player_checker} won!")
            game_over = True
        # Check for draw if no win
        elif check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! The board is full.")
            game_over = True
        else:
            # Switch to the next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    connect_four_game()
