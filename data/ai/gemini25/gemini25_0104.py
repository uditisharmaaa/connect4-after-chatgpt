import os
import random
import string

# --- Constants (Global Variables) ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_SEQUENCE_LENGTH = 4

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
        list: A 2D list representing the empty board, initialized with spaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the current state of the board.
    """
    clear_screen()

    # Print column labels (A, B, C, ...)
    print("  " + "   ".join(string.ascii_uppercase[:NUM_COLS]))

    # Print board rows and columns
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        row_content = []
        for c in range(NUM_COLS):
            row_content.append(f"| {board[r][c]} ")
        print("".join(row_content) + "|")
    print("+---" * NUM_COLS + "+")


def get_column_input(current_player_checker):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker of the current player.

    Returns:
        int: The 0-indexed column number if input is valid.
    """
    while True:
        try:
            col_char = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if len(col_char) != 1 or not col_char.isalpha():
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(col_char) - ord('A')
            if 0 <= col_index < NUM_COLS:
                return col_index
            else:
                print(f"Invalid column. Please enter a column between A and {string.ascii_uppercase[NUM_COLS - 1]}.")
        except Exception:
            print("Invalid input. Please enter a single letter.")


def drop_checker(board, col_index, player_checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The 2D list representing the board.
        col_index (int): The 0-indexed column where the checker is to be dropped.
        player_checker (str): The checker of the current player.

    Returns:
        bool: True if the checker was successfully dropped, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Iterate from bottom row up
        if board[r][col_index] == " ":
            board[r][col_index] = player_checker
            return True
    return False  # Column is full


def check_win(board, player_checker):
    """
    Checks if the given player has won the game.

    Args:
        board (list): The 2D list representing the board.
        player_checker (str): The checker of the player to check for a win.

    Returns:
        bool: True if the player has won, False otherwise.
    """

    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r][c + i] == player_checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check vertical
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r + i][c] == player_checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_SEQUENCE_LENGTH + 1):
        for c in range(NUM_COLS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r + i][c + i] == player_checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_SEQUENCE_LENGTH - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r - i][c + i] == player_checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    return False


def check_draw(board):
    """
    Checks if the board is full (a draw condition).

    Args:
        board (list): The 2D list representing the board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True  # No empty spaces found, it's a draw


def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)
    print(f"Player {PLAYER_CHECKERS[current_player_index]} starts!")

    game_over = False
    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]

        col_index = get_column_input(current_player_checker)

        if not drop_checker(board, col_index, current_player_checker):
            print("That column is full. Please choose another column.")
            # Player does not lose turn, continue to next iteration of loop to ask again
            continue

        print_board(board)

        if check_win(board, current_player_checker):
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
