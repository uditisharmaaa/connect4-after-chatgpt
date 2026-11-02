import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5 players

# Checkers for players
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# Column labels (A, B, C, ...)
COLUMN_LABELS = [chr(ord('A') + i) for i in range(NUM_COLS)]

# --- Board Functions ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console with column labels.

    Args:
        board (list): The 2D list representing the game board.
    """
    os.system('clear')  # Clear the terminal screen

    # Print column labels
    print(" ", end="")
    for label in COLUMN_LABELS:
        print(f" {label} ", end="")
    print()

    # Print top border
    print("+", end="")
    for _ in range(len(board[0])):
        print("---+", end="")
    print()

    # Print board rows
    for r in range(len(board)):
        print("|", end="")
        for c in range(len(board[0])):
            print(f" {board[r][c]} |", end="")
        print()
        # Print row separator
        print("+", end="")
        for _ in range(len(board[0])):
            print("---+", end="")
        print()

def get_column_index(column_char):
    """
    Converts a column character (e.g., 'A') to its corresponding 0-based index.

    Args:
        column_char (str): The uppercase character representing the column.

    Returns:
        int or None: The 0-based column index, or None if the character is invalid.
    """
    if len(column_char) == 1 and 'A' <= column_char <= 'Z':
        index = ord(column_char) - ord('A')
        if 0 <= index < NUM_COLS:
            return index
    return None

def is_valid_column_input(column_char):
    """
    Checks if the user's column input is valid (a single uppercase letter
    within the board's column range).

    Args:
        column_char (str): The user's input string for the column.

    Returns:
        bool: True if the input is valid, False otherwise.
    """
    return get_column_index(column_char) is not None

def get_lowest_empty_row(board, col_index):
    """
    Finds the lowest available row in a given column where a checker can be placed.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column.

    Returns:
        int or None: The row index where the checker should be placed,
                     or None if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col_index] == " ":
            return r
    return None

def place_checker(board, col_index, player_checker):
    """
    Places a player's checker in the specified column at the lowest available spot.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column.
        player_checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was placed successfully, False if the column was full.
    """
    row_index = get_lowest_empty_row(board, col_index)
    if row_index is not None:
        board[row_index][col_index] = player_checker
        return True
    return False

# --- Win Condition Functions ---

def check_win(board, player_checker):
    """
    Checks if the given player has won the game by forming 4 in a row
    horizontally, vertically, or diagonally.

    Args:
        board (list): The game board.
        player_checker (str): The checker symbol of the player to check for a win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check horizontal wins
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - 3):
            if all(board[r][c + i] == player_checker for i in range(4)):
                return True

    # Check vertical wins
    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLS):
            if all(board[r + i][c] == player_checker for i in range(4)):
                return True

    # Check diagonal wins (top-left to bottom-right)
    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLS - 3):
            if all(board[r + i][c + i] == player_checker for i in range(4)):
                return True

    # Check diagonal wins (bottom-left to top-right)
    for r in range(3, NUM_ROWS):
        for c in range(NUM_COLS - 3):
            if all(board[r - i][c + i] == player_checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely filled, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True  # Board is full

# --- Main Game Logic ---

def main():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_checker = PLAYER_CHECKERS[current_player_index]

    game_over = False

    while not game_over:
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        # Get valid player input
        while True:
            try:
                col_input = input().upper()
                if not is_valid_column_input(col_input):
                    print("Invalid input. Please enter a letter from A to", COLUMN_LABELS[-1] + ":")
                    continue
                
                col_index = get_column_index(col_input)
                
                if get_lowest_empty_row(board, col_index) is None:
                    print(f"Column {col_input} is full. Please choose another column:")
                else:
                    break # Valid column and not full
            except EOFError: # Handles Ctrl+D on Linux/Unix
                print("\nGame terminated by user.")
                sys.exit(0)
            except Exception as e:
                print(f"An unexpected error occurred: {e}. Please try again.")

        # Place checker
        # The logic ensures the column is not full before calling place_checker
        place_checker(board, col_index, current_checker)

        # Check for win
        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print_board(board)
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            current_checker = PLAYER_CHECKERS[current_player_index]

if __name__ == "__main__":
    main()
