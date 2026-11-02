import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (X, O, V, H, M)
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
        board (list): The 2D list representing the current game board.
    """
    clear_screen()
    num_cols = len(board[0])
    num_rows = len(board)

    # Print column labels (A, B, C, ...)
    sys.stdout.write("  ")
    for i in range(num_cols):
        sys.stdout.write(f" {chr(ord('A') + i)}  ")
    sys.stdout.write("\n")

    # Print board content
    for r in range(num_rows):
        sys.stdout.write("+")
        for _ in range(num_cols):
            sys.stdout.write("---+")
        sys.stdout.write("\n")

        sys.stdout.write("|")
        for c in range(num_cols):
            sys.stdout.write(f" {board[r][c]} |")
        sys.stdout.write("\n")

    sys.stdout.write("+")
    for _ in range(num_cols):
        sys.stdout.write("---+")
    sys.stdout.write("\n")


def get_player_input(current_player_checker, num_cols):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker of the current player.
        num_cols (int): The number of columns on the board.

    Returns:
        int: The validated column index (0-based).
    """
    while True:
        try:
            col_input = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if not col_input:
                raise ValueError("Input cannot be empty.")
            
            col_index = ord(col_input[0]) - ord('A')

            if not (0 <= col_index < num_cols):
                print(f"Invalid column: '{col_input}'. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")
            else:
                return col_index
        except (ValueError, IndexError):
            print("Invalid input. Please enter a single uppercase letter for the column (e.g., A, B, C).")


def drop_checker(board, col_index, player_checker):
    """
    Places the player's checker into the specified column.

    Args:
        board (list): The 2D list representing the current game board.
        col_index (int): The 0-based index of the column to drop the checker.
        player_checker (str): The checker of the current player.

    Returns:
        tuple: (True, row_index) if the checker was placed successfully,
               (False, -1) if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Start from bottom row
        if board[r][col_index] == " ":
            board[r][col_index] = player_checker
            return True, r  # Return success and the row where it was placed
    return False, -1  # Column is full


def check_win(board, last_row, last_col, player_checker):
    """
    Checks if the last placed checker results in a win.

    Args:
        board (list): The 2D list representing the current game board.
        last_row (int): The row index where the last checker was placed.
        last_col (int): The column index where the last checker was placed.
        player_checker (str): The checker of the player who just moved.

    Returns:
        bool: True if the player won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])
    k = WIN_CONDITION  # Number of checkers needed to win

    # Check horizontal
    count = 0
    for c in range(num_cols):
        if board[last_row][c] == player_checker:
            count += 1
            if count >= k:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(num_rows):
        if board[r][last_col] == player_checker:
            count += 1
            if count >= k:
                return True
        else:
            count = 0

    # Check positive diagonal (bottom-left to top-right)
    # Start from the point (last_row, last_col) and go to the bottom-left edge of the diagonal
    row_start = last_row
    col_start = last_col
    while row_start < num_rows - 1 and col_start > 0:
        row_start += 1
        col_start -= 1

    count = 0
    while row_start >= 0 and col_start < num_cols:
        if board[row_start][col_start] == player_checker:
            count += 1
            if count >= k:
                return True
        else:
            count = 0
        row_start -= 1
        col_start += 1

    # Check negative diagonal (top-left to bottom-right)
    # Start from the point (last_row, last_col) and go to the top-left edge of the diagonal
    row_start = last_row
    col_start = last_col
    while row_start > 0 and col_start > 0:
        row_start -= 1
        col_start -= 1

    count = 0
    while row_start < num_rows and col_start < num_cols:
        if board[row_start][col_start] == player_checker:
            count += 1
            if count >= k:
                return True
        else:
            count = 0
        row_start += 1
        col_start += 1

    return False


def check_draw(board):
    """
    Checks if the board is completely filled (draw condition).

    Args:
        board (list): The 2D list representing the current game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True  # No empty spaces found, it's a draw


def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner = None

    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)
        
        col_index = get_player_input(current_player_checker, NUM_COLS)
        
        success, last_row = drop_checker(board, col_index, current_player_checker)

        if not success:
            print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
            # Player does not lose turn if column is full
            continue 

        if check_win(board, last_row, col_index, current_player_checker):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            winner = current_player_checker
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
