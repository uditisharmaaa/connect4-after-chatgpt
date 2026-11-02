import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]


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
    num_rows = len(board)
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for i in range(num_cols):
        print(f" {chr(ord('A') + i)} ", end="")
    print("\n" + "+---" * num_cols + "+")

    # Print board rows
    for r in range(num_rows):
        print("|", end="")
        for c in range(num_cols):
            print(f" {board[r][c]} |", end="")
        print("\n" + "+---" * num_cols + "+")


def is_valid_column_input(col_input, num_cols):
    """
    Checks if the user's column input is valid.

    Args:
        col_input (str): The raw input string from the user.
        num_cols (int): The total number of columns on the board.

    Returns:
        int or None: The 0-indexed column number if valid, otherwise None.
    """
    if not isinstance(col_input, str) or len(col_input) != 1:
        return None

    col_input = col_input.upper()
    if 'A' <= col_input <= chr(ord('A') + num_cols - 1):
        return ord(col_input) - ord('A')
    return None


def get_next_available_row(board, col):
    """
    Finds the lowest available row in a given column.

    Args:
        board (list): The game board.
        col (int): The column index.

    Returns:
        int or None: The row index if a spot is available, otherwise None.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None  # Column is full


def place_checker(board, col, checker):
    """
    Places a checker in the specified column.

    Args:
        board (list): The game board.
        col (int): The column index to place the checker.
        checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was placed successfully, False if the column was full.
    """
    row = get_next_available_row(board, col)
    if row is not None:
        board[row][col] = checker
        return True
    return False


def check_win(board, checker, win_condition):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the current player.
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
    for c in range(num_cols):
        for r in range(num_rows - win_condition + 1):
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
    Checks if the board is full, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def play_connect_4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    while not game_over:
        current_checker = CHECKERS[current_player_index]
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        valid_turn = False
        while not valid_turn:
            player_input = input().strip()
            col_index = is_valid_column_input(player_input, NUM_COLS)

            if col_index is None:
                print("Invalid input. Please enter a single letter (e.g., A, B, C) corresponding to a column.")
            elif get_next_available_row(board, col_index) is None:
                print(f"Column {player_input.upper()} is full. Please choose another column.")
            else:
                if place_checker(board, col_index, current_checker):
                    valid_turn = True
                else:
                    # This case should ideally not be reached if get_next_available_row() is checked first
                    print("Error placing checker. Please try again.")

        # Check for win
        if check_win(board, current_checker, WIN_CONDITION):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print_board(board)
            print("The game is a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_connect_4()
