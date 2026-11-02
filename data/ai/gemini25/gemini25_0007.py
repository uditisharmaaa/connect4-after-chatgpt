import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission, but supports 2-5
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers, ordered for selection
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# Column labels (A, B, C, ...)
COLUMN_LABELS = [chr(ord('A') + i) for i in range(NUM_COLS)]

# --- Board Initialization and Printing ---

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board.
    """
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board):
    """
    Clears the screen and prints the current state of the Connect 4 board.

    Args:
        board (list): The 2D list representing the game board.
    """
    os.system('clear')  # Clear the terminal screen

    # Print column labels
    print("  ", end="")
    for col_label in COLUMN_LABELS:
        print(f"{col_label}   ", end="")
    print()

    # Print top border
    print("+", end="")
    for _ in range(NUM_COLS):
        print("---+", end="")
    print()

    # Print rows with checkers and separators
    for r in range(NUM_ROWS):
        print("|", end="")
        for c in range(NUM_COLS):
            print(f" {board[r][c]} |", end="")
        print()
        print("+", end="")
        for _ in range(NUM_COLS):
            print("---+", end="")
        print()

# --- Game Logic ---

def is_valid_column_input(col_input):
    """
    Checks if the user's column input is a valid single uppercase letter.

    Args:
        col_input (str): The raw input from the user.

    Returns:
        bool: True if the input is a single uppercase letter within valid range, False otherwise.
    """
    return len(col_input) == 1 and 'A' <= col_input <= COLUMN_LABELS[NUM_COLS - 1]

def get_column_index(col_char):
    """
    Converts a column character (e.g., 'A') to its corresponding 0-based index.

    Args:
        col_char (str): The uppercase character representing the column.

    Returns:
        int: The 0-based index of the column.
    """
    return ord(col_char) - ord('A')

def drop_checker(board, col_index, checker):
    """
    Places a checker in the lowest available space in the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-based index of the column to drop the checker into.
        checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was successfully placed, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Iterate from bottom row upwards
        if board[r][col_index] == ' ':
            board[r][col_index] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """
    Checks if the given player's checker has achieved a win condition (4 in a row).

    Args:
        board (list): The 2D list representing the game board.
        checker (str): The checker symbol of the player to check for a win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Helper function to check a line segment
    def check_line(r, c, dr, dc):
        count = 0
        for i in range(WIN_CONDITION):
            nr, nc = r + i * dr, c + i * dc
            if 0 <= nr < NUM_ROWS and 0 <= nc < NUM_COLS and board[nr][nc] == checker:
                count += 1
            else:
                break
        return count == WIN_CONDITION

    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if check_line(r, c, 0, 1):
                return True

    # Check vertical
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS):
            if check_line(r, c, 1, 0):
                return True

    # Check diagonal (positive slope)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if check_line(r, c, 1, 1):
                return True

    # Check diagonal (negative slope)
    for r in range(WIN_CONDITION - 1, NUM_ROWS): # Start from row WIN_CONDITION-1
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if check_line(r, c, -1, 1):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == ' ':
                return False  # Found an empty space, not a draw
    return True  # Board is full

# --- Main Game Loop ---

def main():
    """
    Main function to run the Connect 4 game.
    """
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if not (1 <= NUM_COLS <= 26):
        print("Error: NUM_COLS must be between 1 and 26.")
        sys.exit(1)
    if not (WIN_CONDITION <= NUM_ROWS and WIN_CONDITION <= NUM_COLS):
        print(f"Error: WIN_CONDITION ({WIN_CONDITION}) must be less than or equal to both NUM_ROWS ({NUM_ROWS}) and NUM_COLS ({NUM_COLS}).")
        sys.exit(1)

    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    game_over = False

    while not game_over:
        current_checker = players[current_player_idx]
        print_board(board)
        print(f"Player {current_checker}, please enter a column: ", end="")

        valid_turn = False
        while not valid_turn:
            user_input = input().strip().upper()

            if not is_valid_column_input(user_input):
                print(f"Invalid input '{user_input}'. Please enter a single letter from A to {COLUMN_LABELS[NUM_COLS-1]}: ", end="")
                continue

            col_idx = get_column_index(user_input)

            if not drop_checker(board, col_idx, current_checker):
                print(f"Column {user_input} is full. Please choose another column: ", end="")
            else:
                valid_turn = True

        # After a valid turn, check game status
        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The board is full. It's a draw!")
            game_over = True
        else:
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
