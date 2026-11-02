import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# Check for valid NUM_COLS for labeling
if NUM_COLS > 26:
    print("Error: Maximum 26 columns supported for labeling (A-Z).")
    sys.exit(1)
if NUM_PLAYERS > len(PLAYER_CHECKERS):
    print(f"Error: Maximum {len(PLAYER_CHECKERS)} players supported.")
    sys.exit(1)


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
    Prints the current state of the Connect 4 board.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    num_rows = len(board)
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_idx in range(num_cols):
        print(f" {chr(ord('A') + col_idx)} ", end="")
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
    print("+", end="")
    for _ in range(num_cols):
        print("---+", end="")
    print()


def get_column_input(current_player_checker, num_cols):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker symbol of the current player.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-based index of the chosen column.
    """
    while True:
        try:
            col_char = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if not col_char.isalpha() or len(col_char) != 1:
                print("Invalid input. Please enter a single letter (A-Z).")
                continue

            col_index = ord(col_char) - ord('A')
            if 0 <= col_index < num_cols:
                return col_index
            else:
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")
        except Exception:
            print("Invalid input. Please enter a single letter (A-Z).")


def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-based index of the column to drop the checker into.
        checker (str): The checker symbol to place.

    Returns:
        bool: True if the checker was successfully placed, False if the column was full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Start from the bottom row
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True
    return False  # Column is full


def check_win(board, checker):
    """
    Checks if the given player (with `checker`) has won the game.

    Args:
        board (list): The 2D list representing the game board.
        checker (str): The checker symbol of the player to check.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for r in range(num_rows - WIN_CONDITION + 1):
        for c in range(num_cols):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check positively sloped diagonals (bottom-left to top-right)
    for r in range(num_rows - WIN_CONDITION + 1):
        for c in range(num_cols - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check negatively sloped diagonals (top-left to bottom-right)
    for r in range(WIN_CONDITION - 1, num_rows):
        for c in range(num_cols - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    return False


def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full (draw), False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])
    for r in range(num_rows):
        for c in range(num_cols):
            if board[r][c] == " ":
                return False  # An empty space is found, not a draw
    return True  # No empty spaces, it's a draw


def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player_checker = players[current_player_index]

    game_over = False

    while not game_over:
        print_board(board)
        print(f"Player {current_player_checker}, please enter a column:")

        col_index = get_column_input(current_player_checker, NUM_COLS)

        if drop_checker(board, col_index, current_player_checker):
            if check_win(board, current_player_checker):
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
                current_player_checker = players[current_player_index]
        else:
            print("Column is full. Please choose another column.")
            # Player does not lose turn if column is full, they are re-prompted
            # The current implementation will re-prompt through the `while True` loop in get_column_input
            # If the requirement was "lose the turn", we would skip the `else` and directly move to the next player.
            # "If the column is already completely filled with checkers, the turn is invalid and the player loses the turn."
            # Based on this, the player *should* lose their turn. Reverting this logic.
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            current_player_checker = players[current_player_index]


if __name__ == "__main__":
    main()
