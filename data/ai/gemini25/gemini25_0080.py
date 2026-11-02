import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
CHECKERS = ["X", "O", "V", "H", "M"]

# --- Board Initialization ---
def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    Args:
        rows (int): Number of rows.
        cols (int): Number of columns.
    Returns:
        list: A 2D list representing the game board, initialized with spaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def get_column_labels(cols):
    """
    Generates uppercase letter labels for columns.
    Args:
        cols (int): Number of columns.
    Returns:
        list: A list of string labels (e.g., ['A', 'B', 'C']).
    """
    labels = []
    for i in range(cols):
        labels.append(chr(ord('A') + i))
    return labels

def print_board(board, column_labels):
    """
    Prints the Connect 4 board to the console.
    Args:
        board (list): The 2D list representing the game board.
        column_labels (list): List of column labels.
    """
    os.system('clear')  # Clear the screen

    # Print column labels
    print(" ", end="")
    for label in column_labels:
        print(f" {label} ", end="")
    print()

    # Print top border
    print("+", end="")
    for _ in range(len(column_labels)):
        print("---+", end="")
    print()

    # Print rows
    for r in range(len(board)):
        print("|", end="")
        for c in range(len(board[r])):
            print(f" {board[r][c]} |", end="")
        print()
        # Print row separator
        print("+", end="")
        for _ in range(len(column_labels)):
            print("---+", end="")
        print()

# --- Game Logic ---
def get_player_input(player_checker, column_labels):
    """
    Prompts the current player for a column choice and validates the input.
    Args:
        player_checker (str): The checker symbol of the current player.
        column_labels (list): List of valid column labels.
    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            player_input = input(f"Player {player_checker}, please enter a column: ").upper()
            if len(player_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(player_input) - ord('A')
            if 0 <= col_index < len(column_labels):
                return col_index
            else:
                print(f"Invalid column '{player_input}'. Please choose a column from {column_labels[0]} to {column_labels[-1]}.")
        except ValueError:
            print("Invalid input. Please enter a valid column letter.")

def drop_checker(board, col, player_checker):
    """
    Drops the player's checker into the specified column.
    Args:
        board (list): The game board.
        col (int): The 0-indexed column to drop the checker into.
        player_checker (str): The checker symbol of the current player.
    Returns:
        tuple: (True, row_index) if successful, (False, -1) if column is full.
    """
    for r in range(len(board) - 1, -1, -1):  # Iterate from bottom to top
        if board[r][col] == " ":
            board[r][col] = player_checker
            return True, r  # Return success and the row where checker landed
    return False, -1  # Column is full

def check_win(board, row, col, player_checker, win_condition):
    """
    Checks if the last placed checker resulted in a win.
    Args:
        board (list): The game board.
        row (int): The row of the last placed checker.
        col (int): The column of the last placed checker.
        player_checker (str): The checker symbol of the current player.
        win_condition (int): Number of checkers needed in a row to win.
    Returns:
        bool: True if a win is detected, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    count = 0
    for c in range(max(0, col - win_condition + 1), min(num_cols, col + win_condition)):
        if board[row][c] == player_checker:
            count += 1
            if count >= win_condition:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r_check in range(max(0, row - win_condition + 1), min(num_rows, row + win_condition)):
        if board[r_check][col] == player_checker:
            count += 1
            if count >= win_condition:
                return True
        else:
            count = 0

    # Check diagonal (top-left to bottom-right)
    count = 0
    # Start at the top-leftmost possible checker for the diagonal
    start_row = max(0, row - win_condition + 1)
    start_col = max(0, col - win_condition + 1)
    for i in range(win_condition * 2 - 1): # Max length of diagonal to check
        r_check = start_row + i
        c_check = start_col + i
        if 0 <= r_check < num_rows and 0 <= c_check < num_cols:
            if board[r_check][c_check] == player_checker:
                count += 1
                if count >= win_condition:
                    return True
            else:
                count = 0
    
    # Check diagonal (top-right to bottom-left)
    count = 0
    # Start at the top-rightmost possible checker for the diagonal
    start_row = max(0, row - win_condition + 1)
    start_col = min(num_cols - 1, col + win_condition - 1)
    for i in range(win_condition * 2 - 1): # Max length of diagonal to check
        r_check = start_row + i
        c_check = start_col - i
        if 0 <= r_check < num_rows and 0 <= c_check < num_cols:
            if board[r_check][c_check] == player_checker:
                count += 1
                if count >= win_condition:
                    return True
            else:
                count = 0

    return False

def check_draw(board):
    """
    Checks if the board is full, indicating a draw.
    Args:
        board (list): The game board.
    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True  # Board is full

# --- Main Game Function ---
def play_connect4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    column_labels = get_column_labels(NUM_COLS)
    
    if NUM_PLAYERS > len(CHECKERS):
        print(f"Error: Not enough checker symbols for {NUM_PLAYERS} players. Max players supported is {len(CHECKERS)}.")
        sys.exit(1)

    player_checkers = CHECKERS[:NUM_PLAYERS]
    
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_player_checker = player_checkers[current_player_index]
        print_board(board, column_labels)
        
        col_choice = get_player_input(current_player_checker, column_labels)
        
        success, row_landed = drop_checker(board, col_choice, current_player_checker)
        
        if not success:
            print(f"Column {column_labels[col_choice]} is full. Please choose another column.")
            # Player does not lose turn, will be prompted again for valid input
            continue 
        
        # After dropping the checker, print the updated board before checking win/draw
        print_board(board, column_labels)

        if check_win(board, row_landed, col_choice, current_player_checker, WIN_CONDITION):
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print("The board is full! It's a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print("\n--- Game Over ---")

if __name__ == "__main__":
    play_connect4()
