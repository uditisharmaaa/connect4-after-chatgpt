import os
import random
import sys

# --- Global Constants ---
# Board dimensions (can be changed, max 26 columns)
NUM_ROWS = 6
NUM_COLS = 7

# Number of players (between 2 and 5)
NUM_PLAYERS = 2

# Checkers for players
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# Number of checkers in a row to win
WIN_CONDITION = 4

# --- Function Definitions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console, including column labels.

    Args:
        board (list): The 2D list representing the game board.
    """
    # Clear the terminal screen before printing the new board
    os.system('clear')

    # Print column labels (A, B, C, ...)
    sys.stdout.write("  ")
    for i in range(len(board[0])):
        sys.stdout.write(f" {chr(ord('A') + i)} ")
    sys.stdout.write("\n")

    # Print the board rows
    for r_idx, row in enumerate(board):
        sys.stdout.write("+")
        sys.stdout.write("---+")
        sys.stdout.write("---+" * (len(row) - 1))
        sys.stdout.write("\n")
        sys.stdout.write("|")
        for cell in row:
            sys.stdout.write(f" {cell} |")
        sys.stdout.write("\n")
    
    # Print the bottom border of the board
    sys.stdout.write("+")
    sys.stdout.write("---+")
    sys.stdout.write("---+" * (len(board[0]) - 1))
    sys.stdout.write("\n")

def get_column_input(player_checker, num_cols):
    """
    Prompts the current player for a column choice and validates the input.

    Args:
        player_checker (str): The checker symbol of the current player.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            col_char = input(f"Player {player_checker}, please enter a column: ").strip().upper()

            # Check if input is a single uppercase letter
            if not (len(col_char) == 1 and 'A' <= col_char <= chr(ord('A') + num_cols - 1)):
                print(f"Invalid input. Please enter a single letter from A to {chr(ord('A') + num_cols - 1)}.")
                continue

            # Convert column letter to 0-indexed integer
            col_idx = ord(col_char) - ord('A')
            return col_idx
        except Exception:
            # Catch any unexpected errors, though the checks above should handle most
            print("An unexpected error occurred. Please try again.")

def drop_checker(board, col_idx, player_checker):
    """
    Places the player's checker in the lowest available space of the chosen column.

    Args:
        board (list): The 2D list representing the game board.
        col_idx (int): The 0-indexed column where the checker is to be dropped.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the checker was successfully dropped, False if the column is full.
    """
    # Iterate from the bottom row upwards to find the first empty space
    for r_idx in range(len(board) - 1, -1, -1):
        if board[r_idx][col_idx] == " ":
            board[r_idx][col_idx] = player_checker
            return True
    return False  # Column is full

def check_win(board, player_checker, win_condition):
    """
    Checks if the current player has won the game.
    Checks for horizontal, vertical, and diagonal (both directions) wins.

    Args:
        board (list): The 2D list representing the game board.
        player_checker (str): The checker symbol of the current player.
        win_condition (int): The number of consecutive checkers needed to win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal wins
    for r in range(num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check vertical wins
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols):
            if all(board[r + i][c] == player_checker for i in range(win_condition)):
                return True

    # Check diagonal wins (top-left to bottom-right)
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols - win_condition + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check diagonal wins (top-right to bottom-left)
    for r in range(win_condition - 1, num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r - i][c + i] == player_checker for i in range(win_condition)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for row in board:
        if " " in row:  # If any empty space is found, the game is not a draw yet
            return False
    return True  # No empty spaces found, it's a draw

def main():
    """
    Main function to run the Connect 4 game.
    Initializes the game, manages player turns, and checks for win/draw conditions.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly select the first player
    current_player_idx = random.randrange(NUM_PLAYERS)
    
    game_over = False
    
    print_board(board)

    while not game_over:
        current_checker = CHECKERS[current_player_idx]

        # Get and validate player input for column
        valid_move = False
        while not valid_move:
            col_to_drop = get_column_input(current_checker, NUM_COLS)
            
            # Attempt to drop the checker
            if drop_checker(board, col_to_drop, current_checker):
                valid_move = True
            else:
                print(f"Column {chr(ord('A') + col_to_drop)} is full. Please choose another column.")
                # The turn is NOT lost, player is asked for another input

        print_board(board)

        # Check for a win
        if check_win(board, current_checker, WIN_CONDITION):
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for a draw if no win
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        
        # If the game is not over, switch to the next player
        if not game_over:
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

# --- Entry Point ---
if __name__ == "__main__":
    main()
