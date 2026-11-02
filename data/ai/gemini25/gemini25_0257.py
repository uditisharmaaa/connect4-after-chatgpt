import os
import random
import string

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
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
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board


def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()  # Clear screen before printing
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(num_cols):
        print(f" {string.ascii_uppercase[col_index]} ", end="")
    print()

    # Print board content
    for row in board:
        print("+", end="")
        for _ in range(num_cols):
            print("---+", end="")
        print()
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    # Print the bottom border
    print("+", end="")
    for _ in range(num_cols):
        print("---+", end="")
    print()


def get_column_input(current_player_checker, num_cols):
    """
    Gets and validates column input from the player.

    Args:
        current_player_checker (str): The checker of the current player.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-indexed column number if the input is valid.
    """
    while True:
        try:
            prompt = f"Player {current_player_checker}, please enter a column: "
            user_input = input(prompt).upper()

            if len(user_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            column_char = user_input
            column_index = string.ascii_uppercase.find(column_char)

            if 0 <= column_index < num_cols:
                return column_index
            else:
                print(f"Invalid column '{column_char}'. Please enter a letter between A and {string.ascii_uppercase[num_cols - 1]}.")
        except Exception:
            print("Invalid input. Please enter a valid column letter.")


def drop_checker(board, col_index, current_player_checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-indexed column where the checker is to be dropped.
        current_player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the checker was successfully dropped, False if the column is full.
    """
    num_rows = len(board)
    for row in range(num_rows - 1, -1, -1):  # Start from bottom row
        if board[row][col_index] == " ":
            board[row][col_index] = current_player_checker
            return True
    return False  # Column is full


def check_win(board, checker, win_condition):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the current player.
        win_condition (int): Number of checkers in a row needed to win.

    Returns:
        bool: True if the current player has won, False otherwise.
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
    Checks if the board is full, resulting in a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])
    for r in range(num_rows):
        for c in range(num_cols):
            if board[r][c] == " ":
                return False  # Board is not full
    return True  # Board is full


# --- Main Game Logic ---

def play_connect_4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)

        valid_turn = False
        while not valid_turn:
            col_index = get_column_input(current_player_checker, NUM_COLS)
            if drop_checker(board, col_index, current_player_checker):
                valid_turn = True
            else:
                print("Column is full! Please choose another column.")

        print_board(board)  # Print board after successful drop

        if check_win(board, current_player_checker, WIN_CONDITION):
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print("It's a draw! The board is full.")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_connect_4()
