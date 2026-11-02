import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_LENGTH = 4

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
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    num_cols = len(board[0])

    # Print column headers (A, B, C, ...)
    print("  " + "   ".join([chr(ord('A') + i) for i in range(num_cols)]))

    # Print board content
    for r in range(len(board)):
        print("+" + "---+" * num_cols)
        row_str = "|"
        for c in range(num_cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+" + "---+" * num_cols)


def get_column_from_input(prompt):
    """
    Prompts the user for a column input and validates it.

    Args:
        prompt (str): The message to display to the user.

    Returns:
        str: The validated uppercase column letter.
    """
    while True:
        try:
            col_input = input(prompt).strip().upper()
            if len(col_input) != 1 or not ('A' <= col_input <= chr(ord('A') + NUM_COLS - 1)):
                raise ValueError("Invalid column. Please enter a single letter from A to {}.".format(
                    chr(ord('A') + NUM_COLS - 1)))
            return col_input
        except ValueError as e:
            print(f"Error: {e}")


def drop_checker(board, col_char, checker):
    """
    Drops a checker into the specified column of the board.

    Args:
        board (list): The game board.
        col_char (str): The column letter (e.g., 'A', 'B').
        checker (str): The checker symbol (e.g., 'X', 'O').

    Returns:
        bool: True if the checker was successfully dropped, False if the column is full.
    """
    col_index = ord(col_char) - ord('A')

    for r in range(NUM_ROWS - 1, -1, -1):  # Start from bottom row
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True
    return False  # Column is full


def check_win(board, checker):
    """
    Checks if the given checker has formed a winning line of WIN_LENGTH.

    Args:
        board (list): The game board.
        checker (str): The checker symbol to check for a win.

    Returns:
        bool: True if a win is found, False otherwise.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check vertical
    for r in range(NUM_ROWS - WIN_LENGTH + 1):
        for c in range(NUM_COLS):
            if all(board[r + i][c] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_LENGTH + 1):
        for c in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_LENGTH - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    return False


def check_draw(board):
    """
    Checks if the board is completely filled (a draw).

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False
    return True


# --- Main Game Logic ---

def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_checker = PLAYER_CHECKERS[current_player_index]

    while True:
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        col_input = get_column_from_input("")

        # Attempt to drop checker
        if drop_checker(board, col_input, current_checker):
            # Check for win after successful drop
            if check_win(board, current_checker):
                print_board(board)
                print(f"Player {current_checker} won!")
                break

            # Check for draw after successful drop
            if check_draw(board):
                print_board(board)
                print("It's a draw!")
                break

            # Switch to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            current_checker = PLAYER_CHECKERS[current_player_index]
        else:
            print(f"Column {col_input} is full. Player {current_checker}, please choose another column.")
            # The turn is not lost, player is re-prompted in the next iteration

if __name__ == "__main__":
    play_game()
