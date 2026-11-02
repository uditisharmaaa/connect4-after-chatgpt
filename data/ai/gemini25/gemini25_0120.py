import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5 players

# Checkers for players
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board, initialized with whitespaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the current game board.
    """
    clear_screen()

    # Print column labels (A, B, C, ...)
    sys.stdout.write(" ")
    for col_idx in range(NUM_COLS):
        sys.stdout.write(f" {chr(ord('A') + col_idx)} ")
    sys.stdout.write("\n")

    # Print top border
    sys.stdout.write("+")
    for _ in range(NUM_COLS):
        sys.stdout.write("---+")
    sys.stdout.write("\n")

    # Print rows with checkers
    for row_idx in range(NUM_ROWS):
        sys.stdout.write("|")
        for col_idx in range(NUM_COLS):
            sys.stdout.write(f" {board[row_idx][col_idx]} |")
        sys.stdout.write("\n")

        # Print row separator
        sys.stdout.write("+")
        for _ in range(NUM_COLS):
            sys.stdout.write("---+")
        sys.stdout.write("\n")

def get_player_input(current_player_checker):
    """
    Prompts the current player for a column choice and validates the input.

    Args:
        current_player_checker (str): The checker of the current player.

    Returns:
        int: The validated column index (0-based).
    """
    while True:
        try:
            column_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()

            if not column_input.isalpha() or len(column_input) != 1:
                print("Invalid input. Please enter a single uppercase letter (e.g., A, B, C).")
                continue

            col_index = ord(column_input) - ord('A')

            if not (0 <= col_index < NUM_COLS):
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + NUM_COLS - 1)}.")
                continue

            return col_index
        except Exception:
            print("An unexpected error occurred. Please try again.")

def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column to drop the checker into.
        checker (str): The checker symbol ('X', 'O', etc.).

    Returns:
        tuple: A tuple containing (True, row_index) if the checker was placed successfully,
               or (False, None) if the column is full.
    """
    for row_index in range(NUM_ROWS - 1, -1, -1):
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker
            return True, row_index
    return False, None  # Column is full

def check_win(board, row, col, checker):
    """
    Checks if the last placed checker results in a win.

    Args:
        board (list): The game board.
        row (int): The row index of the last placed checker.
        col (int): The column index of the last placed checker.
        checker (str): The checker symbol ('X', 'O', etc.) of the current player.

    Returns:
        bool: True if the current player has won, False otherwise.
    """
    # Check horizontally
    count = 0
    for c in range(NUM_COLS):
        if board[row][c] == checker:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0

    # Check vertically
    count = 0
    for r in range(NUM_ROWS):
        if board[r][col] == checker:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0

    # Check positively sloped diagonals (bottom-left to top-right)
    # Find the starting point of the diagonal containing (row, col)
    # This starting point will be either on the last row or first column.
    start_row = row
    start_col = col
    while start_row < NUM_ROWS - 1 and start_col > 0:
        start_row += 1
        start_col -= 1

    count = 0
    while start_row >= 0 and start_col < NUM_COLS:
        if board[start_row][start_col] == checker:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0
        start_row -= 1
        start_col += 1

    # Check negatively sloped diagonals (top-left to bottom-right)
    # Find the starting point of the diagonal containing (row, col)
    # This starting point will be either on the first row or first column.
    start_row = row
    start_col = col
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1

    count = 0
    while start_row < NUM_ROWS and start_col < NUM_COLS:
        if board[start_row][start_col] == checker:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0
        start_row += 1
        start_col += 1

    return False

def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for col in range(NUM_COLS):
        if board[0][col] == " ":  # If the top row of any column is empty, not a draw
            return False
    return True

# --- Main Game Logic ---

def play_game():
    """
    Orchestrates the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    winning_player = None

    while not game_over:
        current_player_checker = CHECKERS[current_player_index]
        print_board(board)

        valid_move_made = False
        while not valid_move_made:
            col_index = get_player_input(current_player_checker)
            placement_success, row_placed = drop_checker(board, col_index, current_player_checker)

            if placement_success:
                valid_move_made = True
                # Check for win after a valid move
                if check_win(board, row_placed, col_index, current_player_checker):
                    winning_player = current_player_checker
                    game_over = True
                elif check_draw(board):
                    game_over = True
            else:
                print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
                # The turn is not lost, player is asked for another input

        if not game_over:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Game End
    print_board(board)
    if winning_player:
        print(f"Player {winning_player} won!")
    else:
        print("The game is a draw!")

if __name__ == "__main__":
    play_game()
