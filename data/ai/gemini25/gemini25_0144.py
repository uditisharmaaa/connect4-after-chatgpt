import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_LENGTH = 4

# Player checkers (X, O, V, H, M)
CHECKERS = ['X', 'O', 'V', 'H', 'M']
PLAYER_CHECKERS = CHECKERS[:NUM_PLAYERS]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows on the board.
        cols (int): The number of columns on the board.

    Returns:
        list: A 2D list representing the game board, initialized with spaces.
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    sys.stdout.write("  ")
    for col_idx in range(num_cols):
        sys.stdout.write(f"{chr(ord('A') + col_idx)}   ")
    sys.stdout.write("\n")

    # Print board rows
    for row in board:
        sys.stdout.write("+")
        for _ in range(num_cols):
            sys.stdout.write("---+")
        sys.stdout.write("\n")
        sys.stdout.write("|")
        for cell in row:
            sys.stdout.write(f" {cell} |")
        sys.stdout.write("\n")
    
    # Print bottom border
    sys.stdout.write("+")
    for _ in range(num_cols):
        sys.stdout.write("---+")
    sys.stdout.write("\n")

def is_valid_column_input(col_input, num_cols):
    """
    Checks if the user's column input is valid.

    Args:
        col_input (str): The user's input for the column.
        num_cols (int): The total number of columns on the board.

    Returns:
        int or None: The 0-indexed column number if valid, None otherwise.
    """
    if not isinstance(col_input, str) or len(col_input) != 1:
        return None
    
    col_input = col_input.upper()
    col_char_code = ord(col_input)
    
    if ord('A') <= col_char_code < ord('A') + num_cols:
        return col_char_code - ord('A')
    return None

def drop_checker(board, col, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col (int): The 0-indexed column to drop the checker into.
        checker (str): The checker symbol ('X', 'O', etc.).

    Returns:
        bool: True if the checker was placed successfully, False if the column is full.
    """
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the current player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal wins
    for r in range(num_rows):
        for c in range(num_cols - WIN_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check vertical wins
    for r in range(num_rows - WIN_LENGTH + 1):
        for c in range(num_cols):
            if all(board[r + i][c] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal wins (top-left to bottom-right)
    for r in range(num_rows - WIN_LENGTH + 1):
        for c in range(num_cols - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal wins (bottom-left to top-right)
    for r in range(WIN_LENGTH - 1, num_rows):
        for c in range(num_cols - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
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
    for row in board:
        for cell in row:
            if cell == ' ':
                return False  # Found an empty cell, not a draw yet
    return True

# --- Main Game Logic ---

def play_connect4():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    num_players = len(PLAYER_CHECKERS)

    # Randomly select the first player
    current_player_idx = random.randint(0, num_players - 1)
    
    game_over = False
    winner_checker = None

    while not game_over:
        current_checker = PLAYER_CHECKERS[current_player_idx]
        
        print_board(board)
        
        print(f"Player {current_checker}, please enter a column:")
        
        valid_turn = False
        while not valid_turn:
            try:
                col_input = input().strip()
                selected_col_idx = is_valid_column_input(col_input, NUM_COLS)

                if selected_col_idx is None:
                    print("Invalid input. Please enter a single letter (e.g., A, B) within the board range.")
                elif not drop_checker(board, selected_col_idx, current_checker):
                    print(f"Column {col_input.upper()} is full. Please choose another column.")
                else:
                    valid_turn = True
            except EOFError:
                print("\nExiting game due to EOF. Goodbye!")
                return
            except Exception as e:
                print(f"An unexpected error occurred: {e}. Please try again.")

        if check_win(board, current_checker):
            print_board(board)
            winner_checker = current_checker
            game_over = True
            print(f"Player {winner_checker} won!")
        elif check_draw(board):
            print_board(board)
            game_over = True
            print("The board is full! It's a draw!")
        else:
            # Switch to the next player
            current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    play_connect4()
