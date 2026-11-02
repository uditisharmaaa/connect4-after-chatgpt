import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_LENGTH = 4

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

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(len(board[0])):
        print(f" {chr(ord('A') + col_index)} ", end="")
    print()

    # Print the board with separators
    for row_index in range(len(board)):
        print("+", end="")
        for _ in range(len(board[0])):
            print("---+", end="")
        print()

        print("|", end="")
        for col_index in range(len(board[0])):
            print(f" {board[row_index][col_index]} |", end="")
        print()

    # Print the bottom separator
    print("+", end="")
    for _ in range(len(board[0])):
        print("---+", end="")
    print()

def get_column_input(current_player_checker, num_cols):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker of the current player.
        num_cols (int): The number of columns on the board.

    Returns:
        int: The validated column index (0-indexed).
    """
    while True:
        try:
            col_char = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if len(col_char) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B).")
                continue

            col_index = ord(col_char) - ord('A')

            if 0 <= col_index < num_cols:
                return col_index
            else:
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")
        except TypeError:
            print("Invalid input. Please enter a letter.")
        except Exception: # Catch any other unexpected input errors
            print("An unexpected input error occurred. Please try again.")


def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-indexed column where the checker is dropped.
        checker (str): The checker symbol ("X", "O", etc.).

    Returns:
        int or None: The row index where the checker landed, or None if the column is full.
    """
    num_rows = len(board)
    for row_index in range(num_rows - 1, -1, -1):
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker
            return row_index
    return None # Column is full

def check_win(board, checker, last_row, last_col):
    """
    Checks if the current player has won after their last move.

    Args:
        board (list): The game board.
        checker (str): The checker of the current player.
        last_row (int): The row index where the last checker was placed.
        last_col (int): The column index where the last checker was placed.

    Returns:
        bool: True if the current player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    count = 0
    for c in range(num_cols):
        if board[last_row][c] == checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(num_rows):
        if board[r][last_col] == checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0

    # Check diagonal (top-left to bottom-right)
    count = 0
    # Find the starting point of the diagonal (top-leftmost)
    start_row = last_row - min(last_row, last_col)
    start_col = last_col - min(last_row, last_col)
    r, c = start_row, start_col
    while r < num_rows and c < num_cols:
        if board[r][c] == checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
        r += 1
        c += 1

    # Check diagonal (top-right to bottom-left)
    count = 0
    # Find the starting point of the diagonal (top-rightmost)
    start_row = last_row - min(last_row, num_cols - 1 - last_col)
    start_col = last_col + min(last_row, num_cols - 1 - last_col)
    r, c = start_row, start_col
    while r < num_rows and c >= 0:
        if board[r][c] == checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
        r += 1
        c -= 1

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
        for cell in row:
            if cell == " ":
                return False  # Found an empty cell, not a draw
    return True  # No empty cells, it's a draw

# --- Main Game Logic ---

def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_player_checker = CHECKERS[current_player_index]
        print_board(board)

        col_index = get_column_input(current_player_checker, NUM_COLS)
        
        # Drop the checker
        last_row = drop_checker(board, col_index, current_player_checker)

        if last_row is None:
            print("Column is full! Please choose another column.")
            # Player does not lose turn if column is full
            continue

        # Check for win
        if check_win(board, current_player_checker, last_row, col_index):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
