import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
EMPTY_CELL = " "


# --- Helper Functions ---

def clear_screen():
    """Clears the console screen."""
    os.system('clear')


def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board, initialized with empty cells.
    """
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the current game board.
    """
    clear_screen()
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for i in range(num_cols):
        print(f" {chr(ord('A') + i)} ", end="")
    print()

    # Print board rows
    for r in range(len(board)):
        print("+", end="")
        for _ in range(num_cols):
            print("---+", end="")
        print()
        print("|", end="")
        for c in range(num_cols):
            print(f" {board[r][c]} |", end="")
        print()

    # Print bottom border
    print("+", end="")
    for _ in range(num_cols):
        print("---+", end="")
    print()


def get_column_input(player_checker, board):
    """
    Gets valid column input from the current player.

    Args:
        player_checker (str): The checker symbol for the current player.
        board (list): The current game board.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    num_cols = len(board[0])
    while True:
        try:
            col_char = input(f"Player {player_checker}, please enter a column: ").strip().upper()

            if not col_char.isalpha() or len(col_char) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(col_char) - ord('A')

            if not (0 <= col_index < num_cols):
                print(f"Invalid column. Please choose a column between A and {chr(ord('A') + num_cols - 1)}.")
                continue

            if board[0][col_index] != EMPTY_CELL:
                print("Column is full. Please choose another column.")
                continue

            return col_index
        except ValueError:
            print("Invalid input. Please enter a letter.")


def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column on the board.

    Args:
        board (list): The current game board.
        col_index (int): The 0-indexed column where the checker is to be dropped.
        checker (str): The checker symbol to place.

    Returns:
        bool: True if the checker was successfully placed, False if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):
        if board[r][col_index] == EMPTY_CELL:
            board[r][col_index] = checker
            return True
    return False


def check_win(board, checker):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The current game board.
        checker (str): The checker symbol of the player to check for a win.

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
    for c in range(num_cols):
        for r in range(num_rows - WIN_CONDITION + 1):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(num_rows - WIN_CONDITION + 1):
        for c in range(num_cols - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, num_rows):
        for c in range(num_cols - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    return False


def check_draw(board):
    """
    Checks if the game is a draw (board is full).

    Args:
        board (list): The current game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])
    for r in range(num_rows):
        for c in range(num_cols):
            if board[r][c] == EMPTY_CELL:
                return False  # Found an empty cell, not a draw
    return True  # No empty cells found, it's a draw


def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    players = list(CHECKERS)  # Use a mutable list for players
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)
    print(f"Player {players[current_player_index]} starts the game!")
    input("Press Enter to continue...") # Pause to let user see starting player

    game_over = False

    while not game_over:
        print_board(board)
        current_player_checker = players[current_player_index]

        col_index = get_column_input(current_player_checker, board)

        # Drop checker. The validation in get_column_input already ensures the column isn't full.
        drop_checker(board, col_index, current_player_checker)

        if check_win(board, current_player_checker):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
