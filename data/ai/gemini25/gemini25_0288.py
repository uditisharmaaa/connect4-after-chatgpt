import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4

# Checkers for up to 5 players
CHECKERS = ["X", "O", "V", "H", "M"]
CURRENT_CHECKERS = CHECKERS[:NUM_PLAYERS]


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
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for i in range(NUM_COLS):
        print(f"{chr(ord('A') + i)}   ", end="")
    print()

    # Print board rows
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        print("|", end="")
        for c in range(NUM_COLS):
            print(f" {board[r][c]} |", end="")
        print()
    print("+---" * NUM_COLS + "+")


def is_valid_column(col_input):
    """
    Validates if the user's column input is a valid letter within the board dimensions.

    Args:
        col_input (str): The user's input for the column.

    Returns:
        int or None: The 0-indexed column number if valid, otherwise None.
    """
    if not isinstance(col_input, str) or len(col_input) != 1 or not col_input.isalpha():
        return None

    col_index = ord(col_input.upper()) - ord('A')
    if 0 <= col_index < NUM_COLS:
        return col_index
    return None


def get_player_move(current_player_checker):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker symbol for the current player.

    Returns:
        int: The 0-indexed valid column number chosen by the player.
    """
    while True:
        col_char = input(f"Player {current_player_checker}, please enter a column: ").strip()
        col_index = is_valid_column(col_char)

        if col_index is None:
            print("Invalid column input. Please enter a single letter (e.g., A, B).")
        else:
            return col_index


def place_checker(board, col_index, checker):
    """
    Places the checker in the lowest available row of the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-indexed column number.
        checker (str): The checker symbol to place.

    Returns:
        bool: True if the checker was placed successfully, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Iterate from bottom to top
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True
    return False  # Column is full


def check_win(board, checker):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the player to check for a win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check horizontal wins
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical wins
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - WIN_CONDITION + 1):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal wins (positive slope)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal wins (negative slope)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
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
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True  # No empty spaces found, it's a draw


def play_connect_4():
    """Main function to play the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player_checker = CURRENT_CHECKERS[current_player_index]

    game_over = False
    print_board(board)
    print(f"Player {current_player_checker} goes first!")

    while not game_over:
        col_index = get_player_move(current_player_checker)

        if place_checker(board, col_index, current_player_checker):
            print_board(board)

            if check_win(board, current_player_checker):
                print(f"Player {current_player_checker} won!")
                game_over = True
            elif check_draw(board):
                print("The board is full! It's a draw!")
                game_over = True
            else:
                # Switch to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
                current_player_checker = CURRENT_CHECKERS[current_player_index]
        else:
            print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
            # Player does not lose turn if column is full, they try again

    print("\nGame Over!")


# --- Run the game ---
if __name__ == "__main__":
    play_connect_4()
