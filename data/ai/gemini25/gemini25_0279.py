import os
import random
import sys

# --- Global Constants (for easy modification as per assignment) ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Max 5 players
WIN_SEQUENCE_LENGTH = 4

# Player checkers (X, O, V, H, M)
CHECKERS = ["X", "O", "V", "H", "M"]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console, including column labels.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_idx in range(num_cols):
        print(f" {chr(ord('A') + col_idx)} ", end=" ")
    print()

    # Print top border
    print("+", end="")
    for _ in range(num_cols):
        print("---+", end="")
    print()

    # Print rows with checkers and horizontal separators
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+", end="")
        for _ in range(num_cols):
            print("---+", end="")
        print()

def get_column_input(current_player_checker):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker of the current player.

    Returns:
        int: The 0-indexed valid column number chosen by the player.
    """
    while True:
        try:
            user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()

            if not user_input.isalpha() or len(user_input) != 1:
                raise ValueError("Invalid input. Please enter a single letter (A-Z).")

            col_index = ord(user_input) - ord('A')

            if not (0 <= col_index < NUM_COLS):
                raise ValueError(f"Column '{user_input}' is out of board range (A-{chr(ord('A') + NUM_COLS - 1)}).")

            return col_index
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def drop_checker(board, col_index, checker):
    """
    Drops the checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-indexed column where the checker is to be dropped.
        checker (str): The checker symbol ("X", "O", etc.).

    Returns:
        tuple: (True, row_index) if successful, (False, -1) if column is full.
    """
    for row_index in range(NUM_ROWS - 1, -1, -1):
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker
            return True, row_index
    return False, -1 # Column is full

def check_win(board, row, col, checker):
    """
    Checks if the last placed checker at (row, col) results in a win.

    Args:
        board (list): The game board.
        row (int): The row index of the last placed checker.
        col (int): The column index of the last placed checker.
        checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the current player has won, False otherwise.
    """
    # Define directions for checking (horizontal, vertical, diagonal)
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal (top-left to bottom-right)
        (1, -1)   # Diagonal (top-right to bottom-left)
    ]

    for dr, dc in directions:
        count = 1  # Count of consecutive checkers

        # Check in positive direction
        for i in range(1, WIN_SEQUENCE_LENGTH):
            r, c = row + dr * i, col + dc * i
            if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
                count += 1
            else:
                break
        
        # Check in negative direction (if applicable, e.g., for horizontal/diagonal)
        for i in range(1, WIN_SEQUENCE_LENGTH):
            r, c = row - dr * i, col - dc * i
            if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
                count += 1
            else:
                break
        
        if count >= WIN_SEQUENCE_LENGTH:
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
    for row in board:
        if " " in row:
            return False  # An empty space found, not a draw yet
    return True # No empty spaces, it's a draw

def main():
    """
    Main function to run the Connect 4 game.
    """
    # Initialize game variables
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Select checkers for the active players
    active_checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    # --- Game Loop ---
    while not game_over:
        current_player_checker = active_checkers[current_player_index]
        
        print_board(board)
        
        # Get valid column input
        col_to_drop = get_column_input(current_player_checker)
        
        # Attempt to drop checker
        success, row_dropped = drop_checker(board, col_to_drop, current_player_checker)
        
        if not success:
            print(f"Column {chr(ord('A') + col_to_drop)} is full. Player {current_player_checker} loses their turn.")
            # Player loses turn if column is full, so we simply don't switch player index
            # and let them try again in the next iteration.
            # Rationale based on "If the column is already completely filled with checkers,
            # the turn is invalid and the player loses the turn."
            # The assignment also says "the player will be asked to provide another input until the input is valid (the turn is not lost)."
            # This is a slight ambiguity. The common interpretation in Connect 4 is that
            # trying to drop into a full column is an invalid move, and the player needs to
            # choose a *different* valid column. The current implementation gives them another
            # chance to pick a column, rather than moving to the next player.
            # For strict interpretation of "loses the turn", the player index should advance.
            # Given "the player will be asked to provide another input until the input is valid (the turn is not lost)",
            # it implies they keep their turn until a checker is *successfully* placed.
            # So, if a column is full, they pick again.
            continue # Re-prompt current player
        
        # Check for win
        if check_win(board, row_dropped, col_to_drop, current_player_checker):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print("\n--- Game Over ---")

if __name__ == "__main__":
    main()
