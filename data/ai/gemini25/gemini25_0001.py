import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns for 'A' through 'Z' labeling
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_SEQUENCE_LENGTH = 4

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']
ACTIVE_CHECKERS = PLAYER_CHECKERS[:NUM_PLAYERS]

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
        list: A 2D list representing the board, initialized with spaces.
    """
    board = []
    for _ in range(rows):
        board.append([' '] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the current state of the board.
    """
    clear_screen()
    
    # Print column headers (A, B, C, ...)
    sys.stdout.write('  ')
    for col_idx in range(len(board[0])):
        sys.stdout.write(f'{chr(ord("A") + col_idx)}   ')
    sys.stdout.write('\n')

    # Print board rows
    for row_idx in range(len(board)):
        sys.stdout.write('+')
        for _ in range(len(board[0])):
            sys.stdout.write('---+')
        sys.stdout.write('\n')

        sys.stdout.write('|')
        for col_idx in range(len(board[0])):
            sys.stdout.write(f' {board[row_idx][col_idx]} |')
        sys.stdout.write('\n')

    # Print bottom border
    sys.stdout.write('+')
    for _ in range(len(board[0])):
        sys.stdout.write('---+')
    sys.stdout.write('\n')

def get_column_input(prompt_message, num_cols):
    """
    Gets and validates column input from the player.

    Args:
        prompt_message (str): The message to display to the player.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-based index of the chosen column, or -1 if input is invalid.
    """
    while True:
        try:
            user_input = input(prompt_message).strip().upper()
            if not user_input:
                print("Input cannot be empty. Please enter a column letter.")
                continue

            col_char = user_input[0] # Take only the first character
            
            # Check if it's a valid letter
            if not 'A' <= col_char <= chr(ord('A') + num_cols - 1):
                print(f"Invalid column. Please enter a letter from A to {chr(ord('A') + num_cols - 1)}.")
                continue
            
            col_index = ord(col_char) - ord('A')
            return col_index
        except (ValueError, IndexError):
            print("Invalid input. Please enter a single letter corresponding to a column.")

def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The 2D list representing the board.
        col_index (int): The 0-based index of the column to drop the checker into.
        checker (str): The checker symbol (e.g., 'X', 'O').

    Returns:
        bool: True if the checker was successfully dropped, False if the column is full.
    """
    for row_idx in range(len(board) - 1, -1, -1):  # Start from bottom row
        if board[row_idx][col_index] == ' ':
            board[row_idx][col_index] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The 2D list representing the board.
        checker (str): The checker symbol of the player to check for a win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check vertical
    for r in range(num_rows - WIN_SEQUENCE_LENGTH + 1):
        for c in range(num_cols):
            if all(board[r + i][c] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check positive diagonal (bottom-left to top-right)
    for r in range(num_rows - WIN_SEQUENCE_LENGTH + 1):
        for c in range(num_cols - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check negative diagonal (top-left to bottom-right)
    for r in range(WIN_SEQUENCE_LENGTH - 1, num_rows):
        for c in range(num_cols - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    return False

def check_draw(board):
    """
    Checks if the game is a draw (board is full).

    Args:
        board (list): The 2D list representing the board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for row in board:
        if ' ' in row:
            return False  # There's still an empty space
    return True  # Board is full

# --- Main Game Logic ---

def main():
    """
    Main function to run the Connect 4 game.
    """
    game_board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly choose the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(game_board)
    print("Welcome to Connect 4!")
    print(f"Players: {', '.join([f'Player {c}' for c in ACTIVE_CHECKERS])}")
    print(f"First player is Player {ACTIVE_CHECKERS[current_player_index]}!\n")
    
    game_over = False

    while not game_over:
        current_checker = ACTIVE_CHECKERS[current_player_index]
        
        # Get valid column input
        column_valid = False
        while not column_valid:
            col_input_char = chr(ord('A') + NUM_COLS - 1) # Example: 'G' for 7 columns
            prompt = f"Player {current_checker}, please enter a column (A-{col_input_char}): "
            col_index = get_column_input(prompt, NUM_COLS)

            if 0 <= col_index < NUM_COLS: # Basic bounds check, further validation handled by drop_checker
                if drop_checker(game_board, col_index, current_checker):
                    column_valid = True
                else:
                    print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
            else:
                print(f"Column index {chr(ord('A') + col_index)} is out of bounds. This should not happen with current input validation.") # Should be caught by get_column_input
        
        print_board(game_board)

        # Check for win
        if check_win(game_board, current_checker):
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(game_board):
            print("It's a draw! The board is full.")
            game_over = True
        
        # Switch to the next player
        if not game_over:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
