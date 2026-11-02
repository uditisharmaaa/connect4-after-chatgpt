import os
import random

# --- Global Constants (Editable for different game configurations) ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_SEQUENCE_LENGTH = 4

# Player checkers, ordered by player number
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with spaces.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console, including column labels.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col_idx in range(NUM_COLS):
        print(f"{chr(ord('A') + col_idx)}   ", end="")
    print()

    # Print board content
    for row_idx in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        print("|", end="")
        for col_idx in range(NUM_COLS):
            print(f" {board[row_idx][col_idx]} |", end="")
        print()
    print("+---" * NUM_COLS + "+")

def get_player_input(current_player_checker):
    """
    Prompts the current player for a column choice and validates the input.

    Args:
        current_player_checker (str): The checker symbol of the current player.

    Returns:
        str: The validated uppercase column letter chosen by the player.
    """
    while True:
        try:
            column_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()

            if not column_input:
                print("Input cannot be empty. Please enter a column letter.")
                continue

            if len(column_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            if not 'A' <= column_input <= chr(ord('A') + NUM_COLS - 1):
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + NUM_COLS - 1)}.")
                continue

            return column_input
        except Exception: # Catch any unexpected errors during input
            print("An unexpected error occurred. Please try again.")

def place_checker(board, column_letter, checker):
    """
    Places a checker in the lowest available position of the specified column.

    Args:
        board (list): The 2D list representing the game board.
        column_letter (str): The uppercase letter of the chosen column.
        checker (str): The checker symbol to place.

    Returns:
        int: The row index where the checker was placed, or -1 if the column is full.
    """
    col_idx = ord(column_letter) - ord('A')

    for row_idx in range(NUM_ROWS - 1, -1, -1):  # Start from bottom row
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = checker
            return row_idx  # Return the row where it was placed
    return -1  # Column is full

def check_win(board, checker, last_row, last_col):
    """
    Checks if the last placed checker resulted in a win (4 in a row).

    Args:
        board (list): The 2D list representing the game board.
        checker (str): The checker symbol of the player to check for a win.
        last_row (int): The row index where the last checker was placed.
        last_col (int): The column index where the last checker was placed.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check horizontal
    count = 0
    for c in range(NUM_COLS):
        if board[last_row][c] == checker:
            count += 1
            if count >= WIN_SEQUENCE_LENGTH:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(NUM_ROWS):
        if board[r][last_col] == checker:
            count += 1
            if count >= WIN_SEQUENCE_LENGTH:
                return True
        else:
            count = 0

    # Check positive diagonal (top-left to bottom-right)
    # Start from the bottom-most, left-most possible point of the diagonal
    # that could contain (last_row, last_col)
    start_row = max(0, last_row - (WIN_SEQUENCE_LENGTH - 1))
    start_col = max(0, last_col - (WIN_SEQUENCE_LENGTH - 1))

    for r_start in range(start_row, NUM_ROWS - WIN_SEQUENCE_LENGTH + 1):
        for c_start in range(start_col, NUM_COLS - WIN_SEQUENCE_LENGTH + 1):
            if r_start <= last_row < r_start + WIN_SEQUENCE_LENGTH and \
               c_start <= last_col < c_start + WIN_SEQUENCE_LENGTH and \
               (last_row - r_start) == (last_col - c_start): # Check if (last_row, last_col) is on this diagonal
                count = 0
                for i in range(WIN_SEQUENCE_LENGTH):
                    if board[r_start + i][c_start + i] == checker:
                        count += 1
                if count >= WIN_SEQUENCE_LENGTH:
                    return True

    # Check negative diagonal (bottom-left to top-right)
    # Start from the bottom-most, right-most possible point of the diagonal
    # that could contain (last_row, last_col)
    start_row = max(0, last_row - (WIN_SEQUENCE_LENGTH - 1))
    end_col = min(NUM_COLS - 1, last_col + (WIN_SEQUENCE_LENGTH - 1))

    for r_start in range(start_row, NUM_ROWS - WIN_SEQUENCE_LENGTH + 1):
        for c_start in range(end_col, WIN_SEQUENCE_LENGTH - 2, -1): # Iterate backwards for columns
             if r_start <= last_row < r_start + WIN_SEQUENCE_LENGTH and \
                c_start >= last_col > c_start - WIN_SEQUENCE_LENGTH and \
                (last_row - r_start) == (c_start - last_col): # Check if (last_row, last_col) is on this diagonal
                count = 0
                for i in range(WIN_SEQUENCE_LENGTH):
                    if board[r_start + i][c_start - i] == checker:
                        count += 1
                if count >= WIN_SEQUENCE_LENGTH:
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
        for cell in row:
            if cell == " ":
                return False  # Found an empty cell, not a draw
    return True  # No empty cells, it's a draw

def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    last_placed_row = -1
    last_placed_col = -1

    clear_screen()
    print_board(board)
    print(f"Player {PLAYER_CHECKERS[current_player_index]} goes first!")

    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]

        column_letter = get_player_input(current_player_checker)
        col_idx = ord(column_letter) - ord('A')

        row_placed = place_checker(board, column_letter, current_player_checker)

        if row_placed == -1:
            print("Column is full! Please choose another column.")
            # Player does not lose turn, re-prompt for input for the same player
            continue
        else:
            last_placed_row = row_placed
            last_placed_col = col_idx

        print_board(board)

        if check_win(board, current_player_checker, last_placed_row, last_placed_col):
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print("\n--- Game Over ---")

if __name__ == "__main__":
    main()
