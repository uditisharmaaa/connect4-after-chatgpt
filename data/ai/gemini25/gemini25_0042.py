import os
import random
import sys

# Global constants for board dimensions and player count
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5 players

# Checkers for players. The first NUM_PLAYERS checkers will be used.
CHECKERS = ["X", "O", "V", "H", "M"]

# --- Board Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list[list[str]]: A 2D list representing the game board.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Clears the screen and prints the current state of the Connect 4 board
    with column labels.

    Args:
        board (list[list[str]]): The current game board.
    """
    os.system('clear')  # Clear the terminal screen

    # Print column labels (A, B, C, ...)
    col_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))

    # Print top border
    print("+---" * len(board[0]) + "+")

    # Print rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

# --- Game Logic Functions ---

def get_column_index(column_char, num_cols):
    """
    Converts a column character (e.g., 'A', 'B') to its corresponding
    0-based integer index.

    Args:
        column_char (str): The uppercase character representing the column.
        num_cols (int): The total number of columns on the board.

    Returns:
        int or None: The 0-based column index if valid, otherwise None.
    """
    if not isinstance(column_char, str) or len(column_char) != 1:
        return None
    
    col_index = ord(column_char.upper()) - ord('A')
    if 0 <= col_index < num_cols:
        return col_index
    return None

def is_valid_move(board, col_index):
    """
    Checks if a move to the specified column is valid.
    A move is valid if the column exists and is not completely full.

    Args:
        board (list[list[str]]): The current game board.
        col_index (int): The 0-based index of the chosen column.

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    if col_index is None or not (0 <= col_index < len(board[0])):
        return False
    # Check if the top row of the chosen column is empty
    return board[0][col_index] == " "

def drop_checker(board, col_index, checker):
    """
    Places a checker in the lowest available space of the specified column.

    Args:
        board (list[list[str]]): The current game board.
        col_index (int): The 0-based index of the column to drop the checker into.
        checker (str): The checker symbol for the current player.

    Returns:
        int: The row index where the checker was placed, or -1 if the column was full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Start from bottom row
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return r  # Return the row where the checker was placed
    return -1  # Column is full

def check_win(board, checker, last_row, last_col):
    """
    Checks if the last placed checker resulted in a win (4 in a row
    horizontally, vertically, or diagonally).

    Args:
        board (list[list[str]]): The current game board.
        checker (str): The checker symbol of the player who just moved.
        last_row (int): The row index where the last checker was placed.
        last_col (int): The column index where the last checker was placed.

    Returns:
        bool: True if the player won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Helper function to count consecutive checkers in a direction
    def count_consecutive(r_start, c_start, r_delta, c_delta):
        count = 0
        r, c = r_start, c_start
        while 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
            count += 1
            r += r_delta
            c += c_delta
        return count

    # Check horizontal win
    # Count left from last_col
    left = count_consecutive(last_row, last_col, 0, -1)
    # Count right from last_col (excluding the last_col itself, already counted in left)
    right = count_consecutive(last_row, last_col + 1, 0, 1)
    if left + right >= 4:
        return True

    # Check vertical win
    # Count up from last_row
    up = count_consecutive(last_row, last_col, -1, 0)
    # Count down from last_row (excluding the last_row itself)
    down = count_consecutive(last_row + 1, last_col, 1, 0)
    if up + down >= 4:
        return True

    # Check diagonal (positive slope: /)
    # Count up-left
    up_left = count_consecutive(last_row, last_col, -1, -1)
    # Count down-right (excluding the last_row, last_col itself)
    down_right = count_consecutive(last_row + 1, last_col + 1, 1, 1)
    if up_left + down_right >= 4:
        return True

    # Check diagonal (negative slope: \)
    # Count up-right
    up_right = count_consecutive(last_row, last_col, -1, 1)
    # Count down-left (excluding the last_row, last_col itself)
    down_left = count_consecutive(last_row + 1, last_col - 1, 1, -1)
    if up_right + down_left >= 4:
        return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list[list[str]]): The current game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False  # Found an empty cell, not a draw
    return True  # No empty cells found, it's a draw

def main():
    """
    Main function to run the Connect 4 game.
    """
    # Initialize the game board
    board = create_board(NUM_ROWS, NUM_COLS)

    # Get available checkers for the specified number of players
    player_checkers = CHECKERS[:NUM_PLAYERS]

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Game loop
    game_over = False
    winner_checker = None

    while not game_over:
        current_checker = player_checkers[current_player_index]
        
        print_board(board)
        
        # Prompt for player input
        print(f"Player {current_checker}, please enter a column:")
        
        user_input = input().strip().upper()
        
        # Validate input
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Please enter a single letter (e.g., A, B).")
            # Turn is not lost, ask again
            continue
        
        col_index = get_column_index(user_input, NUM_COLS)

        if not is_valid_move(board, col_index):
            print("Invalid move. Column is full or out of bounds. Please choose another column.")
            # Turn is not lost, ask again
            continue
        
        # Drop the checker
        last_row_placed = drop_checker(board, col_index, current_checker)
        last_col_placed = col_index # This is the same as col_index

        # Check for a win
        if check_win(board, current_checker, last_row_placed, last_col_placed):
            print_board(board) # Print final board with win
            winner_checker = current_checker
            game_over = True
        # Check for a draw
        elif check_draw(board):
            print_board(board) # Print final board for draw
            game_over = True
            print("It's a draw!")
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            
    # After game loop, print winner if any
    if winner_checker:
        print(f"Player {winner_checker} won!")
    
    print("Game Over!")

# Ensure the main function runs when the script is executed
if __name__ == "__main__":
    main()
