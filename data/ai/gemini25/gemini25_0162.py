import os
import random
import sys

# --- Global Constants ---
# Board dimensions
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z

# Player configuration
NUM_PLAYERS = 2  # Between 2 and 5 players
# Checkers for players. The first NUM_PLAYERS characters will be used.
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# Win condition
WIN_LENGTH = 4

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows in the board.
        cols (int): The number of columns in the board.

    Returns:
        list: A 2D list representing the board, initialized with spaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    cols = len(board[0])
    # Print column labels (A, B, C, ...)
    print("  " + "   ".join([chr(ord('A') + i) for i in range(cols)]))

    # Print top border
    print("+" + "---+".join(["" for _ in range(cols)]) + "---") # Fix: "---" for each column

    # Print rows with checkers and separators
    for row in board:
        print("|" + "|".join([f" {cell} " for cell in row]) + "|")
        print("+" + "---+".join(["" for _ in range(cols)]) + "+")

def get_column_index(col_char, num_cols):
    """
    Converts a column character (e.g., 'A') to its integer index.

    Args:
        col_char (str): The uppercase character representing the column.
        num_cols (int): The total number of columns on the board.

    Returns:
        int or None: The 0-based column index if valid, otherwise None.
    """
    if not isinstance(col_char, str) or len(col_char) != 1:
        return None
    
    col_char = col_char.upper()
    if 'A' <= col_char <= chr(ord('A') + num_cols - 1):
        return ord(col_char) - ord('A')
    return None

def is_valid_move(board, col_index):
    """
    Checks if a move to the given column is valid.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column.

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    # Check if column index is within bounds
    if not (0 <= col_index < len(board[0])):
        return False
    # Check if the top row of the column is empty
    return board[0][col_index] == " "

def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column.
        checker (str): The checker symbol ('X', 'O', etc.).

    Returns:
        int or None: The row index where the checker landed, or None if the column is full.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):  # Start from bottom row
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return r  # Return the row where the checker was placed
    return None  # Column is full

def check_win(board, checker, win_length):
    """
    Checks if the given checker has won the game.

    Args:
        board (list): The game board.
        checker (str): The checker symbol to check for a win.
        win_length (int): The number of consecutive checkers needed to win.

    Returns:
        bool: True if the checker has won, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - win_length + 1):
            if all(board[r][c + i] == checker for i in range(win_length)):
                return True

    # Check vertical
    for r in range(rows - win_length + 1):
        for c in range(cols):
            if all(board[r + i][c] == checker for i in range(win_length)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - win_length + 1):
        for c in range(cols - win_length + 1):
            if all(board[r + i][c + i] == checker for i in range(win_length)):
                return True

    # Check diagonal (top-right to bottom-left)
    for r in range(rows - win_length + 1):
        for c in range(win_length - 1, cols):
            if all(board[r + i][c - i] == checker for i in range(win_length)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True  # No empty spaces found, it's a draw

# --- Main Game Logic ---

def main():
    """
    Main function to run the Connect 4 game.
    """
    # --- Initialization ---
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Get checkers for the active players
    active_player_checkers = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    # --- Game Loop ---
    while not game_over:
        clear_screen()
        print_board(board)

        current_player_checker = active_player_checkers[current_player_index]
        print(f"Player {current_player_checker}, please enter a column:")

        # Get and validate player input
        while True:
            try:
                user_input = input().strip().upper()
                col_index = get_column_index(user_input, NUM_COLS)

                if col_index is None:
                    print("Invalid input. Please enter a single uppercase letter (e.g., A, B, C).")
                    continue
                
                if not is_valid_move(board, col_index):
                    print(f"Column {user_input} is full or invalid. Please choose another column.")
                    continue
                
                break # Valid input and valid move
            except EOFError:
                # Handle Ctrl+D gracefully for interactive input
                print("\nExiting game. Goodbye!")
                sys.exit()
            except Exception as e:
                print(f"An unexpected error occurred: {e}. Please try again.")

        # Place the checker
        row_placed = drop_checker(board, col_index, current_player_checker)
        
        # This should ideally not happen if is_valid_move is correct,
        # but as a safeguard.
        if row_placed is None:
            print("Error: Could not place checker. This shouldn't happen after validation.")
            # Player loses turn if this unexpected error occurs, or we can retry the turn
            # For simplicity, let's just proceed to next player, assuming validation should prevent this.
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        # Check for win
        if check_win(board, current_player_checker, WIN_LENGTH):
            clear_screen()
            print_board(board)
            print(f"Player {current_player_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            clear_screen()
            print_board(board)
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print("\nGame Over!")

if __name__ == "__main__":
    main()
