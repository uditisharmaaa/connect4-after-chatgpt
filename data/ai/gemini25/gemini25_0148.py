import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_SEQUENCE_LENGTH = 4

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows on the board.
        cols (int): The number of columns on the board.

    Returns:
        list: A 2D list representing the board, initialized with whitespaces.
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
    col_labels = [chr(ord('A') + i) for i in range(NUM_COLS)]
    print("  " + "   ".join(col_labels))

    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * NUM_COLS + "+")

def get_column_index(col_char):
    """
    Converts a column character (e.g., 'A') to its integer index.

    Args:
        col_char (str): The uppercase character representing the column.

    Returns:
        int: The 0-based index of the column, or -1 if invalid.
    """
    if len(col_char) == 1 and 'A' <= col_char <= chr(ord('A') + NUM_COLS - 1):
        return ord(col_char) - ord('A')
    return -1

def is_valid_column_input(col_char):
    """
    Checks if the user's column input is valid.

    Args:
        col_char (str): The user's input for the column.

    Returns:
        bool: True if the input is a single uppercase letter within the board's range, False otherwise.
    """
    return len(col_char) == 1 and 'A' <= col_char <= chr(ord('A') + NUM_COLS - 1)

def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column.
        checker (str): The checker symbol (e.g., "X", "O").

    Returns:
        tuple: (bool, int, int) - (True if successful, row_index, col_index)
                                 - (False if column is full, -1, -1)
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Start from bottom row
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True, r, col_index
    return False, -1, -1  # Column is full

def check_win(board, checker, last_move_row, last_move_col):
    """
    Checks if the current player has won after their last move.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the current player.
        last_move_row (int): The row of the last placed checker.
        last_move_col (int): The column of the last placed checker.

    Returns:
        bool: True if the player has won, False otherwise.
    """

    # Helper to check a specific direction
    def check_direction(dr, dc):
        count = 0
        # Check forward
        r, c = last_move_row, last_move_col
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check backward (don't double count the last_move_checker)
        r, c = last_move_row - dr, last_move_col - dc
        while 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        return count >= WIN_SEQUENCE_LENGTH

    # Check horizontal
    if check_direction(0, 1):
        return True
    
    # Check vertical
    if check_direction(1, 0): # Only need to check downwards from the last move
        return True

    # Check diagonal (top-left to bottom-right)
    if check_direction(1, 1):
        return True

    # Check anti-diagonal (top-right to bottom-left)
    if check_direction(1, -1):
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
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False
    return True

# --- Main Game Logic ---

def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner_checker = None

    while not game_over:
        current_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)
        
        print(f"Player {current_checker}, please enter a column:")

        # Input validation loop
        valid_input = False
        while not valid_input:
            user_input = input().strip().upper()
            if not is_valid_column_input(user_input):
                print("Invalid input. Please enter a single uppercase letter (e.g., A, B) within the board range.")
                continue

            col_index = get_column_index(user_input)
            
            # Check if column is full
            if board[0][col_index] != " ": # Check the top-most row
                print(f"Column {user_input} is full. Please choose another column.")
                continue
            
            valid_input = True
        
        # Drop the checker
        success, last_move_row, last_move_col = drop_checker(board, col_index, current_checker)
        
        if success:
            # Check for a win
            if check_win(board, current_checker, last_move_row, last_move_col):
                game_over = True
                winner_checker = current_checker
            # Check for a draw if no one won
            elif check_draw(board):
                game_over = True
                winner_checker = None # Indicates a draw
            else:
                # Next player's turn
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        # Else (column was full), the player does not lose their turn due to re-prompting above.
        # This branch won't be reached if the `if board[0][col_index] != " "` check is robust.

    # Game ended, print final board and result
    print_board(board)
    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("It's a draw!")

# --- Entry Point ---
if __name__ == "__main__":
    play_game()
