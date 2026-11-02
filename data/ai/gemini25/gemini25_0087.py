import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
COLUMN_LABELS = [chr(ord('A') + i) for i in range(NUM_COLS)]

# --- Board Initialization ---
def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    Args:
        rows (int): The number of rows on the board.
        cols (int): The number of columns on the board.
    Returns:
        list: A 2D list representing the game board, initialized with spaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

# --- Board Printing ---
def print_board(board):
    """
    Prints the current state of the Connect 4 board to the console.
    Args:
        board (list): The 2D list representing the game board.
    """
    os.system('clear' if os.name == 'posix' else 'cls') # Clear screen for Linux/Unix

    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS[:NUM_COLS]))

    # Print top border
    print("+" + "---+" * NUM_COLS)

    # Print rows
    for row in board:
        print("|" + "|".join([f" {cell} " for cell in row]) + "|")
        print("+" + "---+" * NUM_COLS)

# --- Game Logic Functions ---
def get_column_index(col_char):
    """
    Converts a column character (e.g., 'A', 'B') to its corresponding integer index.
    Args:
        col_char (str): The column character.
    Returns:
        int: The 0-based index of the column, or -1 if invalid.
    """
    try:
        index = COLUMN_LABELS.index(col_char.upper())
        return index if 0 <= index < NUM_COLS else -1
    except ValueError:
        return -1

def is_valid_input(col_input):
    """
    Checks if the player's column input is valid.
    Args:
        col_input (str): The raw input from the player.
    Returns:
        bool: True if the input is a valid column character, False otherwise.
    """
    return len(col_input) == 1 and col_input.upper() in COLUMN_LABELS[:NUM_COLS]

def get_player_move(current_player_char):
    """
    Prompts the current player for their move and validates the input.
    Args:
        current_player_char (str): The checker character of the current player.
    Returns:
        int: The 0-based column index chosen by the player.
    """
    while True:
        col_input = input(f"Player {current_player_char}, please enter a column: ").strip()
        if not is_valid_input(col_input):
            print("Invalid column input. Please enter a single letter corresponding to a column (e.g., A, B).")
            continue
        
        col_index = get_column_index(col_input)
        return col_index

def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.
    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column to drop the checker into.
        checker (str): The checker character to place.
    Returns:
        tuple: (bool, int) - True if the checker was placed successfully, along with the row it landed in.
                         False and -1 if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True, r
    return False, -1 # Column is full

def check_win(board, checker):
    """
    Checks if the given player has won the game.
    Args:
        board (list): The game board.
        checker (str): The checker character of the player to check for a win.
    Returns:
        bool: True if the player has won, False otherwise.
    """

    # Helper function to check a line of cells
    def check_line(cells):
        count = 0
        for cell in cells:
            if cell == checker:
                count += 1
                if count == WIN_CONDITION:
                    return True
            else:
                count = 0
        return False

    # Check horizontal wins
    for r in range(NUM_ROWS):
        if check_line(board[r]):
            return True

    # Check vertical wins
    for c in range(NUM_COLS):
        column_cells = [board[r][c] for r in range(NUM_ROWS)]
        if check_line(column_cells):
            return True

    # Check diagonal wins (top-left to bottom-right)
    for r_start in range(NUM_ROWS - WIN_CONDITION + 1):
        for c_start in range(NUM_COLS - WIN_CONDITION + 1):
            diagonal_cells = [board[r_start + i][c_start + i] for i in range(WIN_CONDITION)]
            if check_line(diagonal_cells):
                return True

    # Check diagonal wins (bottom-left to top-right)
    for r_start in range(WIN_CONDITION - 1, NUM_ROWS):
        for c_start in range(NUM_COLS - WIN_CONDITION + 1):
            diagonal_cells = [board[r_start - i][c_start + i] for i in range(WIN_CONDITION)]
            if check_line(diagonal_cells):
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
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False
    return True

# --- Main Game Loop ---
def play_connect_4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_player_char = PLAYER_CHECKERS[current_player_index]
        print_board(board)

        col_index = get_player_move(current_player_char)

        placed, _ = drop_checker(board, col_index, current_player_char)
        
        if not placed:
            print(f"Column {COLUMN_LABELS[col_index]} is full! Player {current_player_char} loses turn.")
            # Player does not lose turn, they are re-prompted.
            # This implementation re-prompts inside get_player_move if input is invalid.
            # If the column is full, the turn IS lost according to assignment.
            # So, if a column is full, we print a message and proceed to the next player.
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue # Skip win/draw check for this invalid move

        if check_win(board, current_player_char):
            print_board(board)
            print(f"Player {current_player_char} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The board is full! It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_connect_4()
