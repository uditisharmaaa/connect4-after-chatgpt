import os
import random

# --- Global Constants ---
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
    Creates a new game board initialized with whitespaces.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board.
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Prints the current state of the game board.

    Args:
        board (list): The 2D list representing the game board.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(num_cols):
        print(f" {chr(ord('A') + col_index)} ", end="")
    print()

    # Print top border
    print("+", end="")
    for _ in range(num_cols):
        print("---+", end="")
    print()

    # Print rows with checkers and separators
    for row_index in range(num_rows):
        print("|", end="")
        for col_index in range(num_cols):
            print(f" {board[row_index][col_index]} |", end="")
        print()

        # Print row separator
        print("+", end="")
        for _ in range(num_cols):
            print("---+", end="")
        print()


def get_column_input(prompt, num_cols):
    """
    Prompts the player for a column input and validates it.

    Args:
        prompt (str): The message to display to the user.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-indexed column number if input is valid.
    """
    while True:
        user_input = input(prompt).strip().upper()
        if not user_input:
            print("Input cannot be empty. Please enter a column letter.")
            continue

        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter (e.g., A, B, C).")
            continue

        col_char = user_input[0]
        col_index = ord(col_char) - ord('A')

        if 0 <= col_index < num_cols:
            return col_index
        else:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")


def place_checker(board, col_index, checker):
    """
    Places a checker in the lowest available spot of a given column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-indexed column to place the checker in.
        checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was successfully placed, False if the column is full.
    """
    num_rows = len(board)
    for row_index in range(num_rows - 1, -1, -1):  # Iterate from bottom to top
        if board[row_index][col_index] == ' ':
            board[row_index][col_index] = checker
            return True
    return False  # Column is full


def check_win(board, checker, win_condition):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The 2D list representing the game board.
        checker (str): The checker symbol of the player to check for a win.
        win_condition (int): The number of checkers needed in a row to win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r][c + i] == checker for i in range(win_condition)):
                return True

    # Check vertical
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols):
            if all(board[r + i][c] == checker for i in range(win_condition)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols - win_condition + 1):
            if all(board[r + i][c + i] == checker for i in range(win_condition)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(win_condition - 1, num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r - i][c + i] == checker for i in range(win_condition)):
                return True

    return False


def check_draw(board):
    """
    Checks if the board is completely filled, indicating a draw.

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for row in board:
        if ' ' in row:
            return False  # Found an empty space, not a draw yet
    return True  # No empty spaces, it's a draw


# --- Main Game Logic ---

def play_connect_4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    while not game_over:
        clear_screen()
        print_board(board)

        current_checker = PLAYER_CHECKERS[current_player_index]
        print(f"Player {current_checker}, please enter a column:")

        col_index = get_column_input(f"Player {current_checker}, your turn: ", NUM_COLS)

        if place_checker(board, col_index, current_checker):
            # Checker was successfully placed
            if check_win(board, current_checker, WIN_CONDITION):
                clear_screen()
                print_board(board)
                print(f"Player {current_checker} won!")
                game_over = True
            elif check_draw(board):
                clear_screen()
                print_board(board)
                print("It's a draw! The board is full.")
                game_over = True
            else:
                # Switch to next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            print("Column is full! You lose your turn.")
            input("Press Enter to continue...") # Pause to let player read message


if __name__ == "__main__":
    play_connect_4()
