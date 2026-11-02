import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers, ordered for up to 5 players
CHECKERS = ["X", "O", "V", "H", "M"]

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
    rows = len(board)
    cols = len(board[0])

    # Print column labels (A, B, C, ...)
    sys.stdout.write("  ")
    for i in range(cols):
        sys.stdout.write(f"{chr(ord('A') + i)}   ")
    sys.stdout.write("\n")

    # Print board rows
    for r in range(rows):
        sys.stdout.write("+")
        sys.stdout.write("---+") * cols
        sys.stdout.write("\n")
        sys.stdout.write("|")
        for c in range(cols):
            sys.stdout.write(f" {board[r][c]} |")
        sys.stdout.write("\n")

    sys.stdout.write("+")
    sys.stdout.write("---+") * cols
    sys.stdout.write("\n")

def get_column_index(col_char, num_cols):
    """
    Converts a column character (e.g., 'A') to its integer index.

    Args:
        col_char (str): The uppercase letter representing the column.
        num_cols (int): The total number of columns on the board.

    Returns:
        int or None: The integer index of the column, or None if invalid.
    """
    if not isinstance(col_char, str) or len(col_char) != 1:
        return None
    
    col_char = col_char.upper()
    col_index = ord(col_char) - ord('A')
    
    if 0 <= col_index < num_cols:
        return col_index
    return None

def get_player_input(current_player_checker, board, num_cols):
    """
    Prompts the current player for a column choice and validates the input.

    Args:
        current_player_checker (str): The checker symbol of the current player.
        board (list): The game board.
        num_cols (int): The number of columns on the board.

    Returns:
        int: The valid integer index of the chosen column.
    """
    while True:
        try:
            col_input = input(f"Player {current_player_checker}, please enter a column: ").strip()
            
            # Check for empty input
            if not col_input:
                print("Invalid input: Please enter a column letter (e.g., A).")
                continue

            # Check for multiple characters
            if len(col_input) > 1:
                print("Invalid input: Please enter only one column letter.")
                continue

            col_index = get_column_index(col_input, num_cols)

            if col_index is None:
                print("Invalid input: Column does not exist. Please enter a letter from A to "
                      f"{chr(ord('A') + num_cols - 1)}.")
            elif board[0][col_index] != " ":  # Check if the top of the column is full
                print("Column is full. Please choose another column.")
            else:
                return col_index
        except Exception:
            # Catch unexpected errors, though the checks above should cover most
            print("An unexpected error occurred. Please try again.")


def drop_checker(board, col_index, player_checker):
    """
    Places the player's checker in the lowest available space of the specified column.

    Args:
        board (list): The game board.
        col_index (int): The integer index of the chosen column.
        player_checker (str): The checker symbol of the current player.

    Returns:
        tuple or None: A tuple (row, col) of the placed checker's position if successful,
                       None if the column is full (should be caught by input validation).
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = player_checker
            return (r, col_index)
    return None  # Column is full

def check_win(board, last_move_row, last_move_col, player_checker, win_condition):
    """
    Checks if the player who just made a move has won the game.

    Args:
        board (list): The game board.
        last_move_row (int): The row index of the last placed checker.
        last_move_col (int): The column index of the last placed checker.
        player_checker (str): The checker symbol of the current player.
        win_condition (int): The number of checkers in a row required to win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    def count_consecutive(delta_row, delta_col):
        """Helper to count consecutive checkers in a given direction."""
        count = 0
        r, c = last_move_row, last_move_col
        # Count forwards
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == player_checker:
            count += 1
            r += delta_row
            c += delta_col
        
        # Count backwards (excluding the starting checker to avoid double counting)
        r, c = last_move_row - delta_row, last_move_col - delta_col
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == player_checker:
            count += 1
            r -= delta_row
            c -= delta_col
        
        return count

    # Check horizontal
    if count_consecutive(0, 1) >= win_condition:
        return True

    # Check vertical
    if count_consecutive(1, 0) >= win_condition: # Only need to check downwards as new checker is always highest
        return True

    # Check diagonal (top-left to bottom-right)
    if count_consecutive(1, 1) >= win_condition:
        return True

    # Check diagonal (top-right to bottom-left)
    if count_consecutive(1, -1) >= win_condition:
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
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True  # Board is full

# --- Main Game Logic ---

def play_connect_4():
    """
    Main function to run the Connect 4 game.
    """
    
    # Initialize game variables
    board = create_board(NUM_ROWS, NUM_COLS)
    players = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner_checker = None

    print_board(board)
    print(f"Player {players[current_player_index]} goes first!")
    
    while not game_over:
        current_player_checker = players[current_player_index]
        
        # Get valid player input
        col_index = get_player_input(current_player_checker, board, NUM_COLS)
        
        # Place the checker
        placed_position = drop_checker(board, col_index, current_player_checker)
        
        # Print updated board
        print_board(board)

        # Check for win condition
        if check_win(board, placed_position[0], placed_position[1], current_player_checker, WIN_CONDITION):
            winner_checker = current_player_checker
            game_over = True
            print(f"Player {winner_checker} won!")
        elif check_draw(board):
            game_over = True
            print("The game is a draw!")
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# --- Entry Point ---
if __name__ == "__main__":
    play_connect_4()
