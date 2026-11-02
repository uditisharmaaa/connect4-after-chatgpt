import os
import random
import sys

# --- Global Constants ---
# Board dimensions (can be changed for different game sizes)
NUM_ROWS = 6
NUM_COLS = 7

# Number of players (between 2 and 5)
NUM_PLAYERS = 2

# Checkers for players
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# Number of checkers in a row to win
WIN_CONDITION = 4

# ANSI escape codes for clearing the screen (works on Linux/Unix terminals)
CLEAR_SCREEN = '\033[H\033[J'

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    # Use os.system('clear') for Linux/Unix or os.system('cls') for Windows
    # For this assignment, 'clear' is specified.
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.

    Args:
        rows (int): The number of rows in the board.
        cols (int): The number of columns in the board.

    Returns:
        list[list[str]]: A 2D list representing the game board.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console, including column labels.

    Args:
        board (list[list[str]]): The game board.
    """
    clear_screen()  # Clear the screen before printing the updated board

    # Print column labels (A, B, C, ...)
    column_labels = [chr(ord('A') + i) for i in range(NUM_COLS)]
    print("  " + "   ".join(column_labels))

    # Print the board with separators
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * NUM_COLS + "+")

def get_column_index(column_char):
    """
    Converts a column character (e.g., 'A', 'B') to its corresponding 0-based index.

    Args:
        column_char (str): The uppercase character representing the column.

    Returns:
        int: The 0-based index of the column, or -1 if invalid.
    """
    if len(column_char) == 1 and 'A' <= column_char <= chr(ord('A') + NUM_COLS - 1):
        return ord(column_char) - ord('A')
    return -1

def is_valid_input(column_char):
    """
    Checks if the user's column input is valid.

    Args:
        column_char (str): The user's input for the column.

    Returns:
        bool: True if the input is valid, False otherwise.
    """
    return get_column_index(column_char) != -1

def get_next_available_row(board, col_index):
    """
    Finds the lowest available row in a given column.

    Args:
        board (list[list[str]]): The game board.
        col_index (int): The 0-based index of the column.

    Returns:
        int: The row index where the checker should be placed, or -1 if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Start from the bottom row
        if board[r][col_index] == " ":
            return r
    return -1  # Column is full

def place_checker(board, col_index, player_checker):
    """
    Places a player's checker in the specified column.

    Args:
        board (list[list[str]]): The game board.
        col_index (int): The 0-based index of the column.
        player_checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was placed successfully, False if the column was full.
    """
    row_index = get_next_available_row(board, col_index)
    if row_index != -1:
        board[row_index][col_index] = player_checker
        return True
    return False

def check_win(board, player_checker):
    """
    Checks if the current player has won the game.

    Args:
        board (list[list[str]]): The game board.
        player_checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check horizontal wins
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical wins
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - WIN_CONDITION + 1):
            if all(board[r + i][c] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal wins (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal wins (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list[list[str]]): The game board.

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
    game_board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1) # Randomly select the first player
    game_over = False
    turn_count = 0

    print_board(game_board)
    print(f"Player {CHECKERS[current_player_index]} starts!")

    while not game_over:
        player_checker = CHECKERS[current_player_index]

        valid_turn = False
        while not valid_turn:
            # Prompt the current player for input
            column_input = input(f"Player {player_checker}, please enter a column: ").upper()

            # Validate input format (single uppercase letter)
            if not is_valid_input(column_input):
                print("Invalid input. Please enter a single uppercase letter (e.g., A, B) within the board range.")
                continue

            col_index = get_column_index(column_input)

            # Validate if the chosen column is full
            if get_next_available_row(game_board, col_index) == -1:
                print(f"Column {column_input} is full. Please choose another column.")
                # Player does not lose turn, will be prompted again
                continue

            # If input is valid and column is not full, place the checker
            if place_checker(game_board, col_index, player_checker):
                valid_turn = True
            else:
                # This case should ideally not be reached if get_next_available_row check is correct,
                # but good for robustness.
                print("Could not place checker. Please try again.")

        turn_count += 1
        print_board(game_board)

        # Check for win after every turn
        if check_win(game_board, player_checker):
            print(f"Player {player_checker} won!")
            game_over = True
        # Check for draw if no one has won and the board is full
        elif check_draw(game_board):
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print("\nGame Over!")

if __name__ == "__main__":
    main()
