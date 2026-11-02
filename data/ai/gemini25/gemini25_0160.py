import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4

# Checkers available
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYERS = CHECKERS[:NUM_PLAYERS]


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
    num_rows = len(board)

    # Print column headers (A, B, C, ...)
    print(" ", end="")
    for col_idx in range(num_cols):
        print(f"  {chr(ord('A') + col_idx)} ", end="")
    print()

    # Print top border
    print("+", end="")
    for _ in range(num_cols):
        print("---+", end="")
    print()

    # Print rows with checkers
    for r in range(num_rows):
        print("|", end="")
        for c in range(num_cols):
            print(f" {board[r][c]} |", end="")
        print()
        print("+", end="")
        for _ in range(num_cols):
            print("---+", end="")
        print()


def get_player_input(player_checker, board):
    """
    Prompts the current player for a column choice and validates the input.

    Args:
        player_checker (str): The checker symbol of the current player.
        board (list): The 2D list representing the game board.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    num_cols = len(board[0])
    while True:
        try:
            col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()

            # Validate input length and character type
            if not col_input or len(col_input) != 1 or not ('A' <= col_input[0] <= chr(ord('A') + num_cols - 1)):
                print(f"Invalid input. Please enter a single letter from A to {chr(ord('A') + num_cols - 1)}.")
                continue

            col_index = ord(col_input[0]) - ord('A')

            # Validate column not full
            if board[0][col_index] != " ":
                print(f"Column {col_input} is full. Please choose another column.")
                continue

            return col_index
        except (EOFError, KeyboardInterrupt):
            print("\nGame aborted by player.")
            sys.exit(0)
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")


def place_checker(board, col_index, checker):
    """
    Places the checker in the lowest available row of the given column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-indexed column number.
        checker (str): The checker symbol to place.

    Returns:
        tuple: (row_index, col_index) where the checker was placed, or None if column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Iterate from bottom row upwards
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return r, col_index
    return None  # Column is full (should be caught by get_player_input, but good for safety)


def check_win(board, checker, last_row, last_col):
    """
    Checks if the last placed checker resulted in a win.

    Args:
        board (list): The 2D list representing the game board.
        checker (str): The checker symbol of the current player.
        last_row (int): The row index where the last checker was placed.
        last_col (int): The column index where the last checker was placed.

    Returns:
        bool: True if the player won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Helper function to count consecutive checkers in a direction
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

    # Check diagonal (bottom-left to top-right)
    if count_consecutive(1, -1):
        return True

    return False


def check_draw(board):
    """
    Checks if the board is completely filled (game is a draw).

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True  # No empty spaces found, it's a draw


def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_checker = PLAYERS[current_player_index]

    game_over = False

    while not game_over:
        print_board(board)
        print(f"It's Player {current_checker}'s turn.")

        col_index = get_player_input(current_checker, board)
        placement = place_checker(board, col_index, current_checker)

        if placement:
            last_row, last_col = placement
            if check_win(board, current_checker, last_row, last_col):
                print_board(board)
                print(f"Player {current_checker} won!")
                game_over = True
            elif check_draw(board):
                print_board(board)
                print("The board is full! It's a draw!")
                game_over = True
            else:
                # Switch to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
                current_checker = PLAYERS[current_player_index]
        # If placement is None, the column was full, and get_player_input already handled it
        # and asked for new input, so the turn is effectively not lost.

    print("\n--- Game Over ---")


if __name__ == "__main__":
    main()
