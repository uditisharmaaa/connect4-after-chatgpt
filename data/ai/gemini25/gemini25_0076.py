import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels
NUM_PLAYERS = 2  # Between 2 and 5 players

# Checkers available
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYERS_CHECKERS = CHECKERS[:NUM_PLAYERS]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    # For Windows, use 'cls'
    os.system('cls' if os.name == 'nt' else 'clear')

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
    clear_screen()

    # Print column labels (A, B, C, ...)
    sys.stdout.write(" ")
    for col_idx in range(len(board[0])):
        sys.stdout.write(f" {chr(ord('A') + col_idx)}  ")
    sys.stdout.write("\n")

    # Print board rows and cells
    for row in board:
        sys.stdout.write("+")
        for _ in row:
            sys.stdout.write("---+")
        sys.stdout.write("\n")

        sys.stdout.write("|")
        for cell in row:
            sys.stdout.write(f" {cell} |")
        sys.stdout.write("\n")

    # Print the last horizontal line
    sys.stdout.write("+")
    for _ in board[0]:
        sys.stdout.write("---+")
    sys.stdout.write("\n")

def get_column_input(current_player_checker, num_cols):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker of the current player.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            col_char = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()

            if not col_char.isalpha() or len(col_char) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(col_char) - ord('A')

            if 0 <= col_index < num_cols:
                return col_index
            else:
                print(f"Column '{col_char}' is out of board range. Please choose between A and {chr(ord('A') + num_cols - 1)}.")
        except Exception:
            print("An unexpected error occurred. Please try again.")

def place_checker(board, col, player_checker):
    """
    Places the player's checker in the lowest available space in the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col (int): The 0-indexed column number where the checker is to be placed.
        player_checker (str): The checker of the current player.

    Returns:
        bool: True if the checker was successfully placed, False if the column is full.
    """
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_checker
            return True
    print(f"Column {chr(ord('A') + col)} is full. Please choose another column.")
    return False

def check_win(board, player_checker):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The 2D list representing the game board.
        player_checker (str): The checker of the current player.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == player_checker for i in range(4)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r + i][c] == player_checker for i in range(4)):
                return True

    # Check diagonal (positive slope)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == player_checker for i in range(4)):
                return True

    # Check diagonal (negative slope)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == player_checker for i in range(4)):
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
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # An empty space is found, not a draw
    return True  # No empty spaces found, it's a draw

def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    num_cols_on_board = len(board[0])

    # Randomly choose the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_player_checker = PLAYERS_CHECKERS[current_player_index]
        print_board(board)
        
        # Get and validate player input
        valid_placement = False
        chosen_col = -1
        while not valid_placement:
            chosen_col = get_column_input(current_player_checker, num_cols_on_board)
            valid_placement = place_checker(board, chosen_col, current_player_checker)

        # Print the board after placement
        print_board(board)

        # Check for win
        if check_win(board, current_player_checker):
            print(f"Player {current_player_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("The board is full. It's a draw!")
            game_over = True
        
        # Switch to the next player
        if not game_over:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
