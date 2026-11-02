import os
import random
import sys

# --- Global Constants ---
NUM_COLUMNS = 7  # Maximum 26 columns (A-Z)
NUM_ROWS = 6
NUM_PLAYERS = 2  # Between 2 and 5 players

# Checkers for players
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# Column labels (A, B, C, ...)
COLUMN_LABELS = [chr(ord('A') + i) for i in range(NUM_COLUMNS)]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

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

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    
    # Print board content
    for r_idx, row in enumerate(board):
        print("+---" * NUM_COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * NUM_COLUMNS + "+")

def get_valid_column_input(current_player_checker):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker symbol of the current player.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            user_input = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if not user_input.isalpha() or len(user_input) != 1:
                raise ValueError("Invalid input. Please enter a single letter (e.g., A, B, C).")

            col_index = ord(user_input) - ord('A')

            if not (0 <= col_index < NUM_COLUMNS):
                raise ValueError(f"Column '{user_input}' is out of bounds. Please choose between A and {COLUMN_LABELS[-1]}.")
            
            return col_index
        except ValueError as e:
            print(f"Error: {e}")

def drop_checker(board, col, player_checker):
    """
    Drops a player's checker into the specified column.

    Args:
        board (list): The game board.
        col (int): The 0-indexed column to drop the checker into.
        player_checker (str): The checker symbol of the current player.

    Returns:
        tuple: A tuple (row, col) indicating where the checker was placed,
               or None if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = player_checker
            return (r, col)
    return None  # Column is full

def check_win(board, player_checker, last_placed_row, last_placed_col):
    """
    Checks if the last placed checker resulted in a win.

    Args:
        board (list): The game board.
        player_checker (str): The checker symbol of the current player.
        last_placed_row (int): The row index of the last placed checker.
        last_placed_col (int): The column index of the last placed checker.

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
        for i in range(1, 4):
            r, c = last_placed_row + dr * i, last_placed_col + dc * i
            if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLUMNS and board[r][c] == player_checker:
                count += 1
            else:
                break
        
        # Check in negative direction
        for i in range(1, 4):
            r, c = last_placed_row - dr * i, last_placed_col - dc * i
            if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLUMNS and board[r][c] == player_checker:
                count += 1
            else:
                break
        
        if count >= 4:
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
        for c in range(NUM_COLUMNS):
            if board[r][c] == " ":
                return False
    return True

# --- Main Game Logic ---

def play_connect4():
    """Main function to play the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLUMNS)

    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner = None

    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]
        
        print_board(board)
        
        last_placed_pos = None
        while last_placed_pos is None:
            col_index = get_valid_column_input(current_player_checker)
            last_placed_pos = drop_checker(board, col_index, current_player_checker)
            
            if last_placed_pos is None:
                print(f"Column {COLUMN_LABELS[col_index]} is full. Please choose another column.")
                # Player does NOT lose turn for full column, they are asked again
        
        r, c = last_placed_pos

        if check_win(board, current_player_checker, r, c):
            winner = current_player_checker
            game_over = True
        elif check_draw(board):
            game_over = True
        
        if not game_over:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print_board(board) # Print final board
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")

# --- Start the game ---
if __name__ == "__main__":
    play_connect4()
