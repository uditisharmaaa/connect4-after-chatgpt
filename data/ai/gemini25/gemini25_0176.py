import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4

# Checkers available
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYERS_CHECKERS = CHECKERS[:NUM_PLAYERS]


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
    clear_screen()  # Clear screen before printing
    num_cols = len(board[0])

    # Print column labels (A, B, C...)
    col_labels = [chr(ord('A') + i) for i in range(num_cols)]
    print("  " + "   ".join(col_labels))

    # Print board rows
    for row in board:
        print("+---" * num_cols + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * num_cols + "+")


def is_valid_column_input(col_input, num_cols):
    """
    Checks if the user's column input is valid.

    Args:
        col_input (str): The user's input for the column.
        num_cols (int): The total number of columns on the board.

    Returns:
        bool: True if the input is valid, False otherwise.
    """
    if not isinstance(col_input, str) or len(col_input) != 1:
        return False
    col_input = col_input.upper()
    if not 'A' <= col_input <= chr(ord('A') + num_cols - 1):
        return False
    return True


def get_column_index(col_char):
    """
    Converts a column character (e.g., 'A', 'B') to its corresponding integer index.

    Args:
        col_char (str): The column character.

    Returns:
        int: The 0-based index of the column.
    """
    return ord(col_char.upper()) - ord('A')


def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column.
        checker (str): The checker symbol (e.g., "X", "O").

    Returns:
        int or None: The row index where the checker was placed, or None if the column is full.
    """
    for row_index in range(len(board) - 1, -1, -1):
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker
            return row_index
    return None  # Column is full


def check_win(board, checker, last_row, last_col):
    """
    Checks if the last placed checker results in a win.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the current player.
        last_row (int): The row index where the last checker was placed.
        last_col (int): The column index where the last checker was placed.

    Returns:
        bool: True if the current player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    def check_direction(dr, dc):
        count = 0
        # Check in one direction
        r, c = last_row, last_col
        while 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Check in the opposite direction
        r, c = last_row - dr, last_col - dc  # Start one step back from original placement
        while 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        return count >= WIN_CONDITION

    # Check horizontal
    if check_direction(0, 1):
        return True
    # Check vertical
    if check_direction(1, 0):
        return True
    # Check diagonal (top-left to bottom-right)
    if check_direction(1, 1):
        return True
    # Check anti-diagonal (top-right to bottom-left)
    if check_direction(1, -1):
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
    for row in board:
        for cell in row:
            if cell == " ":
                return False  # Found an empty cell, not a draw
    return True


# --- Main Game Logic ---

def play_connect_4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    while not game_over:
        current_checker = PLAYERS_CHECKERS[current_player_index]
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        valid_turn = False
        while not valid_turn:
            col_input = input().strip()
            if not is_valid_column_input(col_input, NUM_COLS):
                print("Invalid column. Please enter a letter from A to", chr(ord('A') + NUM_COLS - 1) + ":")
                continue

            col_index = get_column_index(col_input)
            last_placed_row = drop_checker(board, col_index, current_checker)

            if last_placed_row is None:
                print("Column is full. Please choose another column:")
            else:
                valid_turn = True

        # After a valid turn, check for win or draw
        if check_win(board, current_checker, last_placed_row, col_index):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_connect_4()
