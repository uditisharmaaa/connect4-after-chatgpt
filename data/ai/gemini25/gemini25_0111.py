import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_SEQUENCE_LENGTH = 4

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# Column labels (A, B, C, ...)
COLUMN_LABELS = [chr(ord('A') + i) for i in range(NUM_COLS)]


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
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Prints the current state of the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()

    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))

    # Print top border
    print("+" + "---+".join(['-' * 3 for _ in range(NUM_COLS)]) + "+")

    # Print rows with checkers
    for r in range(NUM_ROWS):
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
        # Print row separator
        print("+" + "---+".join(['-' * 3 for _ in range(NUM_COLS)]) + "+")


def is_valid_column_input(col_input):
    """
    Checks if the user's column input is valid (a single uppercase letter
    within the allowed range).

    Args:
        col_input (str): The user's raw input.

    Returns:
        bool: True if the input is valid, False otherwise.
    """
    if not isinstance(col_input, str):
        return False
    if len(col_input) != 1:
        return False
    if not col_input.isalpha():
        return False
    if not col_input.isupper():
        return False
    if col_input not in COLUMN_LABELS:
        return False
    return True


def get_column_index(col_char):
    """
    Converts a column character (e.g., 'A') to its corresponding 0-based index.

    Args:
        col_char (str): The uppercase character representing the column.

    Returns:
        int: The 0-based index of the column, or -1 if invalid.
    """
    try:
        return COLUMN_LABELS.index(col_char)
    except ValueError:
        return -1


def drop_checker(board, col_index, checker):
    """
    Places a checker in the lowest available space in the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column.
        checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was successfully dropped, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Start from bottom row
        if board[r][col_index] == ' ':
            board[r][col_index] = checker
            return True
    return False  # Column is full


def check_win(board, checker):
    """
    Checks if the current player has achieved a win condition (4 in a row)
    horizontally, vertically, or diagonally.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the player to check for a win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check vertical
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r + i][c] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check positive slope diagonal (bottom-left to top-right)
    for r in range(WIN_SEQUENCE_LENGTH - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check negative slope diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_SEQUENCE_LENGTH + 1):
        for c in range(NUM_COLS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    return False


def check_draw(board):
    """
    Checks if the board is completely filled, resulting in a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == ' ':
                return False  # Found an empty space, not a draw yet
    return True  # Board is full


def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player_checker = PLAYER_CHECKERS[current_player_index]

    game_over = False
    turn_count = 0

    while not game_over:
        print_board(board)
        current_player_checker = PLAYER_CHECKERS[current_player_index]

        print(f"Player {current_player_checker}, please enter a column:")
        
        while True:
            col_input = input().strip().upper()

            if not is_valid_column_input(col_input):
                print("Invalid input. Please enter a single uppercase letter (e.g., A, B, C) corresponding to an available column.")
                continue

            col_index = get_column_index(col_input)

            if col_index == -1: # Should already be caught by is_valid_column_input
                print(f"Column '{col_input}' is out of bounds. Please choose a column from {COLUMN_LABELS[0]} to {COLUMN_LABELS[-1]}.")
                continue
            
            if not drop_checker(board, col_index, current_player_checker):
                print(f"Column {col_input} is full. Please choose another column.")
                continue
            
            break # Valid move, break out of input loop

        turn_count += 1

        if check_win(board, current_player_checker):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The board is full. It's a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
