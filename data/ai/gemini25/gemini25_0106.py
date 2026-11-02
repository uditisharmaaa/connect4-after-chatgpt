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
    # Clear the console screen for a clean display
    os.system('clear')

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for i in range(len(board[0])):
        print(f"{chr(ord('A') + i)}   ", end="")
    print()

    # Print the board rows
    for r_idx, row in enumerate(board):
        # Print horizontal separator
        print("+---" * len(row) + "+")
        # Print row content
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    # Print the last horizontal separator
    print("+---" * len(board[0]) + "+")

def get_column_from_input(prompt):
    """
    Prompts the user for a column input and validates it.

    Args:
        prompt (str): The message to display to the user.

    Returns:
        str: The validated uppercase column letter.
    """
    while True:
        col_input = input(prompt).strip().upper()
        # Check if the input is a single uppercase letter
        if len(col_input) == 1 and 'A' <= col_input <= chr(ord('A') + NUM_COLS - 1):
            return col_input
        else:
            print(f"Invalid input. Please enter a column letter between A and {chr(ord('A') + NUM_COLS - 1)}.")

def place_checker(board, col_char, checker):
    """
    Places a checker in the specified column.

    Args:
        board (list): The game board.
        col_char (str): The uppercase character representing the column (e.g., 'A').
        checker (str): The checker symbol for the current player.

    Returns:
        tuple: (bool, int) - True if placement was successful, False otherwise,
               and the row index where the checker was placed, or -1 if invalid.
    """
    # Convert column character to a 0-indexed integer
    col_idx = ord(col_char) - ord('A')

    # Check if the column is within valid bounds
    if not (0 <= col_idx < NUM_COLS):
        return False, -1 # Should ideally be caught by get_column_from_input, but good for robustness

    # Find the lowest available row in the column
    for r_idx in range(NUM_ROWS - 1, -1, -1): # Iterate from bottom to top
        if board[r_idx][col_idx] == " ":
            board[r_idx][col_idx] = checker
            return True, r_idx # Return success and the row where it was placed
    
    # If loop finishes, the column is full
    print(f"Column {col_char} is full. Please choose another column.")
    return False, -1

def check_win(board, checker, last_row, last_col):
    """
    Checks if the current player has won after placing a checker.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the current player.
        last_row (int): The row index where the last checker was placed.
        last_col (int): The column index where the last checker was placed.

    Returns:
        bool: True if the current player has won, False otherwise.
    """
    # Helper function to count consecutive checkers in a given direction
    def count_consecutive(row, col, d_row, d_col):
        count = 0
        r, c = row, col
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r += d_row
            c += d_col
        return count

    # Check horizontally
    # Count left and right from the last placed checker
    horizontal_count = count_consecutive(last_row, last_col, 0, 1) + \
                       count_consecutive(last_row, last_col, 0, -1) - 1 # Subtract 1 because (last_row, last_col) is counted twice
    if horizontal_count >= WIN_CONDITION:
        return True

    # Check vertically
    # Count up and down from the last placed checker
    vertical_count = count_consecutive(last_row, last_col, 1, 0) + \
                     count_consecutive(last_row, last_col, -1, 0) - 1
    if vertical_count >= WIN_CONDITION:
        return True

    # Check diagonally (top-left to bottom-right)
    # Count towards top-left and bottom-right
    diag1_count = count_consecutive(last_row, last_col, 1, 1) + \
                  count_consecutive(last_row, last_col, -1, -1) - 1
    if diag1_count >= WIN_CONDITION:
        return True

    # Check diagonally (top-right to bottom-left)
    # Count towards top-right and bottom-left
    diag2_count = count_consecutive(last_row, last_col, 1, -1) + \
                  count_consecutive(last_row, last_col, -1, 1) - 1
    if diag2_count >= WIN_CONDITION:
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
        if " " in row: # If any empty space is found, the board is not full
            return False
    return True # No empty spaces found, board is full

def play_game():
    """
    Main function to run the Connect 4 game.
    Initializes the board, handles player turns, checks for wins/draws.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly choose the first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_checker = CHECKERS[current_player_idx]
        
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        placement_successful = False
        last_placed_row = -1
        last_placed_col = -1

        while not placement_successful:
            col_input_char = get_column_from_input(f"Player {current_checker}, your turn: ")
            
            # Convert column char to index for check_win
            last_placed_col = ord(col_input_char) - ord('A')
            
            placement_successful, last_placed_row = place_checker(board, col_input_char, current_checker)
            # If placement was not successful, the loop continues and the player re-enters input.
            # The player does *not* lose their turn if the column is full or input is invalid.

        # After a successful placement, check for win or draw
        if check_win(board, current_checker, last_placed_row, last_placed_col):
            print_board(board) # Print final board with winning move
            print(f"Player {current_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board) # Print final board for draw
            print("It's a draw!")
            game_over = True
        else:
            # If no win or draw, switch to the next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

# --- Main execution ---
if __name__ == "__main__":
    play_game()
