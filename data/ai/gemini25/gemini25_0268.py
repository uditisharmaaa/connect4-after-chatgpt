import os
import random
import string

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels
NUM_PLAYERS = 2
PLAYER_TOKENS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_CONDITION = 4  # Number of checkers in a row to win

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
        list: A 2D list representing the game board,
              initialized with whitespaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    num_cols = len(board[0])
    num_rows = len(board)

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for i in range(num_cols):
        print(f" {string.ascii_uppercase[i]} ", end="")
    print()

    # Print board content
    for r in range(num_rows):
        print("+", end="")
        for _ in range(num_cols):
            print("---+", end="")
        print()
        print("|", end="")
        for c in range(num_cols):
            print(f" {board[r][c]} |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for _ in range(num_cols):
        print("---+", end="")
    print()

def get_column_index(col_char, num_cols):
    """
    Converts a column letter (e.g., 'A') to a 0-based index.

    Args:
        col_char (str): The uppercase letter representing the column.
        num_cols (int): The total number of columns on the board.

    Returns:
        int or None: The 0-based index of the column, or None if invalid.
    """
    if not isinstance(col_char, str) or len(col_char) != 1:
        return None
    
    col_char = col_char.upper()
    
    if 'A' <= col_char <= string.ascii_uppercase[num_cols - 1]:
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
    num_cols = len(board[0])
    if not (0 <= col_index < num_cols):
        return False  # Column index out of bounds

    # Check if the top row of the column is empty
    return board[0][col_index] == " "

def place_checker(board, col_index, player_token):
    """
    Places a checker in the lowest available spot of the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column.
        player_token (str): The token of the current player.

    Returns:
        tuple: (row, col) of where the checker was placed, or None if failed.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = player_token
            return (r, col_index)
    return None  # Column is full

def check_win(board, last_placed_row, last_placed_col, player_token):
    """
    Checks if the current player has won after placing a checker.

    Args:
        board (list): The game board.
        last_placed_row (int): The row of the last placed checker.
        last_placed_col (int): The column of the last placed checker.
        player_token (str): The token of the current player.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Directions to check: (row_delta, col_delta)
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal (bottom-right)
        (1, -1)   # Diagonal (bottom-left)
    ]

    for dr, dc in directions:
        count = 0
        # Check in one direction
        for i in range(-(WIN_CONDITION - 1), WIN_CONDITION):
            r = last_placed_row + i * dr
            c = last_placed_col + i * dc

            if 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == player_token:
                count += 1
                if count >= WIN_CONDITION:
                    return True
            else:
                count = 0  # Reset count if consecutive chain is broken
    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])
    for r in range(num_rows):
        for c in range(num_cols):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True

# --- Main Game Logic ---

def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        player_token = PLAYER_TOKENS[current_player_index]
        
        print_board(board)
        print(f"Player {player_token}, please enter a column:")

        last_placed_pos = None  # To store (row, col) of the last placed checker

        while last_placed_pos is None:
            user_input = input().strip().upper()
            
            if not user_input or len(user_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., 'A'):")
                continue

            col_index = get_column_index(user_input, NUM_COLS)

            if col_index is None:
                print(f"Invalid column '{user_input}'. Please enter a letter between A and {string.ascii_uppercase[NUM_COLS-1]}:")
                continue

            if not is_valid_move(board, col_index):
                print(f"Column {user_input} is full. Please choose another column:")
                continue
            
            last_placed_pos = place_checker(board, col_index, player_token)
            
            if last_placed_pos is None: # Should ideally not happen if is_valid_move passed
                print("Error placing checker. Please try again.")

        # After a successful move, check for win or draw
        row, col = last_placed_pos
        if check_win(board, row, col, player_token):
            print_board(board)
            print(f"Player {player_token} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

# --- Entry Point ---
if __name__ == "__main__":
    play_game()
