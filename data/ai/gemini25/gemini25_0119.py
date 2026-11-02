import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (up to 5 players)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
CURRENT_PLAYERS = PLAYER_CHECKERS[:NUM_PLAYERS]

# Column labels (up to 26 columns)
COLUMN_LABELS = [chr(ord('A') + i) for i in range(NUM_COLS)]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

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
        board (list): The 2D list representing the current game board.
    """
    clear_screen()

    # Print column labels
    print(" ", end="")
    for label in COLUMN_LABELS:
        print(f" {label} ", end="")
    print()

    # Print board rows
    for r_idx, row in enumerate(board):
        print("+", end="")
        for _ in range(NUM_COLS):
            print("---+", end="")
        print()

        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()

    # Print the last horizontal separator
    print("+", end="")
    for _ in range(NUM_COLS):
        print("---+", end="")
    print()

def get_player_input(current_player_checker):
    """
    Prompts the current player for a column choice and validates the input.

    Args:
        current_player_checker (str): The checker symbol of the current player.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()

            if not user_input:
                print("Error: Input cannot be empty. Please enter a column letter.")
                continue

            if len(user_input) != 1:
                print("Error: Please enter a single column letter (e.g., A, B, C).")
                continue

            if user_input not in COLUMN_LABELS:
                print(f"Error: Invalid column '{user_input}'. Please choose from {', '.join(COLUMN_LABELS)}.")
                continue

            return COLUMN_LABELS.index(user_input)
        except Exception as e:
            print(f"An unexpected error occurred during input: {e}")
            sys.exit(1) # Exit cleanly if a critical error happens

def drop_checker(board, col_idx, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The 2D list representing the current game board.
        col_idx (int): The 0-indexed column number to drop the checker into.
        checker (str): The checker symbol to place.

    Returns:
        int or None: The 0-indexed row where the checker was placed, or None if the column is full.
    """
    for r_idx in range(NUM_ROWS - 1, -1, -1):
        if board[r_idx][col_idx] == " ":
            board[r_idx][col_idx] = checker
            return r_idx
    return None  # Column is full

def check_win(board, checker):
    """
    Checks if the given checker has formed a winning line (horizontal, vertical, or diagonal).

    Args:
        board (list): The 2D list representing the current game board.
        checker (str): The checker symbol to check for a win.

    Returns:
        bool: True if the checker has won, False otherwise.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check positive diagonal (bottom-left to top-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check negative diagonal (top-left to bottom-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The 2D list representing the current game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True  # No empty spaces found, it's a draw

def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    
    # Game Loop
    while not game_over:
        current_player_checker = CURRENT_PLAYERS[current_player_index]
        print_board(board)

        col_chosen = get_player_input(current_player_checker)
        
        row_placed = drop_checker(board, col_chosen, current_player_checker)

        if row_placed is None:
            print(f"Error: Column {COLUMN_LABELS[col_chosen]} is full. Please choose another column.")
            # Player does not lose turn if column is full
            continue 

        # Check for win
        if check_win(board, current_player_checker):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print_board(board)
            print("The game is a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
