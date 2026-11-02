import os
import random
import string

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

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
    num_cols = len(board[0])

    # Print column headers (A, B, C...)
    col_labels = [string.ascii_uppercase[i] for i in range(num_cols)]
    print("  " + "   ".join(col_labels))

    # Print top border
    print("+" + "---+" * num_cols)

    # Print rows
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print("\n" + "+" + "---+" * num_cols)

def get_column_input(num_cols):
    """
    Prompts the current player for a column input and validates it.

    Args:
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-indexed column number if the input is valid.
    """
    while True:
        try:
            col_input = input("Please enter a column: ").upper()
            if len(col_input) != 1 or not col_input.isalpha():
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(col_input) - ord('A')
            if 0 <= col_index < num_cols:
                return col_index
            else:
                print(f"Invalid column. Please enter a letter between A and {string.ascii_uppercase[num_cols - 1]}.")
        except ValueError:
            print("Invalid input. Please enter a letter.")

def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-indexed column number.
        checker (str): The checker symbol for the current player.

    Returns:
        tuple: (True, row_index) if the checker was dropped successfully,
               (False, -1) if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True, r
    return False, -1  # Column is full

def check_win(board, checker, last_row, last_col):
    """
    Checks if the last placed checker resulted in a win.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the player who just moved.
        last_row (int): The row index where the last checker was placed.
        last_col (int): The column index where the last checker was placed.

    Returns:
        bool: True if the current player won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Helper to count consecutive checkers in a direction
    def count_consecutive(delta_row, delta_col):
        count = 0
        for i in range(-WIN_CONDITION + 1, WIN_CONDITION):
            r, c = last_row + i * delta_row, last_col + i * delta_col
            if 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
                count += 1
                if count >= WIN_CONDITION:
                    return True
            else:
                count = 0
        return False

    # Check horizontal
    if count_consecutive(0, 1):
        return True

    # Check vertical
    if count_consecutive(1, 0):
        return True

    # Check diagonal (top-left to bottom-right)
    if count_consecutive(1, 1):
        return True

    # Check diagonal (top-right to bottom-left)
    if count_consecutive(1, -1):
        return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False  # Found an empty cell, not a draw
    return True

# --- Main Game Logic ---

def play_game():
    """Manages the Connect 4 game flow."""
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner_checker = None

    while not game_over:
        current_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)
        print(f"Player {current_checker},", end=" ")

        column_placed = False
        last_row = -1
        last_col = -1

        while not column_placed:
            col_index = get_column_input(NUM_COLS)
            
            success, r = drop_checker(board, col_index, current_checker)
            if success:
                column_placed = True
                last_row = r
                last_col = col_index
            else:
                print("Column is full. Please choose another column.")
                # Player does not lose turn, keeps trying until valid input

        # After a valid move, check for win or draw
        if check_win(board, current_checker, last_row, last_col):
            print_board(board)
            winner_checker = current_checker
            game_over = True
        elif check_draw(board):
            print_board(board)
            game_over = True
        else:
            # Switch to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Game over, announce result
    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    play_game()
