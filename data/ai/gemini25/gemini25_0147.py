import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers needed to win

# Valid checkers for players
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]


# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')


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
    Prints the current state of the Connect 4 board.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()

    # Print column headers (A, B, C, ...)
    sys.stdout.write("  ")
    for i in range(NUM_COLS):
        sys.stdout.write(f" {chr(ord('A') + i)} ")
        if i < NUM_COLS - 1:
            sys.stdout.write(" ")
    sys.stdout.write("\n")

    # Print top border
    sys.stdout.write("+")
    for _ in range(NUM_COLS):
        sys.stdout.write("---+")
    sys.stdout.write("\n")

    # Print rows with checkers
    for r in range(NUM_ROWS):
        sys.stdout.write("|")
        for c in range(NUM_COLS):
            sys.stdout.write(f" {board[r][c]} |")
        sys.stdout.write("\n")

        # Print row separator
        sys.stdout.write("+")
        for _ in range(NUM_COLS):
            sys.stdout.write("---+")
        sys.stdout.write("\n")


def get_column_input(current_player_checker):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker symbol of the current player.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            col_input = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if not col_input.isalpha() or len(col_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(col_input) - ord('A')
            if not (0 <= col_index < NUM_COLS):
                print(f"Invalid column. Please choose a column between A and {chr(ord('A') + NUM_COLS - 1)}.")
                continue
            return col_index
        except ValueError:
            print("Invalid input. Please enter a letter.")


def drop_checker(board, col, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col (int): The 0-indexed column where the checker is to be dropped.
        checker (str): The checker symbol to place.

    Returns:
        int or None: The row where the checker was placed, or None if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return None  # Column is full


def check_win(board, checker, last_row, last_col):
    """
    Checks if the last placed checker resulted in a win.

    Args:
        board (list): The 2D list representing the game board.
        checker (str): The checker symbol to check for.
        last_row (int): The row of the last placed checker.
        last_col (int): The column of the last placed checker.

    Returns:
        bool: True if the checker has won, False otherwise.
    """

    # Check horizontal
    count = 0
    for c in range(NUM_COLS):
        if board[last_row][c] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(NUM_ROWS):
        if board[r][last_col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check positive slope diagonal (bottom-left to top-right)
    # Start from the bottom-left of the diagonal that contains (last_row, last_col)
    start_row = last_row + min(NUM_ROWS - 1 - last_row, last_col)
    start_col = last_col - min(NUM_ROWS - 1 - last_row, last_col)

    count = 0
    while start_row >= 0 and start_col < NUM_COLS:
        if board[start_row][start_col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
        start_row -= 1
        start_col += 1

    # Check negative slope diagonal (top-left to bottom-right)
    # Start from the top-left of the diagonal that contains (last_row, last_col)
    start_row = last_row - min(last_row, last_col)
    start_col = last_col - min(last_row, last_col)

    count = 0
    while start_row < NUM_ROWS and start_col < NUM_COLS:
        if board[start_row][start_col] == checker:
            count += 1
            if count >= WIN_CONDITION:
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
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True  # Board is full


def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player_checker = CHECKERS[current_player_index]

    game_over = False
    winning_player = None

    while not game_over:
        print_board(board)
        print(f"It's Player {current_player_checker}'s turn.")

        col_index = get_column_input(current_player_checker)

        # Attempt to drop checker
        row_placed = drop_checker(board, col_index, current_player_checker)

        if row_placed is None:
            print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
            # Player does not lose turn, continue to next iteration for the same player
            continue

        # Check for win condition
        if check_win(board, current_player_checker, row_placed, col_index):
            winning_player = current_player_checker
            game_over = True
        elif check_draw(board):
            game_over = True  # It's a draw
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            current_player_checker = CHECKERS[current_player_index]

    # Game End
    print_board(board)  # Print final board state

    if winning_player:
        print(f"Player {winning_player} won!")
    else:
        print("The game is a draw!")


if __name__ == "__main__":
    main()
