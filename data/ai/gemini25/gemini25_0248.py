import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']
COL_LABELS = [chr(ord('A') + i) for i in range(NUM_COLS)]


# --- Helper Functions ---
def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')


def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows on the board.
        cols (int): The number of columns on the board.

    Returns:
        list: A 2D list representing the game board,
              initialized with spaces.
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()

    # Print column labels
    print('  ' + '   '.join(COL_LABELS[:NUM_COLS]))
    print('+---+---' * NUM_COLS + '+')

    # Print rows
    for r in range(NUM_ROWS):
        row_str = '|'
        for c in range(NUM_COLS):
            row_str += f' {board[r][c]} |'
        print(row_str)
        print('+---+---' * NUM_COLS + '+')


def get_column_index(column_char):
    """
    Converts a column character (e.g., 'A') to its integer index.

    Args:
        column_char (str): The uppercase letter representing the column.

    Returns:
        int: The 0-based index of the column, or -1 if invalid.
    """
    if not isinstance(column_char, str) or len(column_char) != 1:
        return -1
    char_code = ord(column_char.upper())
    first_label_code = ord(COL_LABELS[0])
    last_label_code = ord(COL_LABELS[NUM_COLS - 1])

    if first_label_code <= char_code <= last_label_code:
        return char_code - first_label_code
    return -1


def is_valid_move(board, col_index):
    """
    Checks if a move to a given column is valid.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column.

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    if not (0 <= col_index < NUM_COLS):
        return False
    # Check if the top row of the column is empty
    return board[0][col_index] == ' '


def place_checker(board, col_index, checker):
    """
    Places a checker in the lowest available space in the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column.
        checker (str): The checker symbol ('X', 'O', etc.).

    Returns:
        bool: True if the checker was placed, False if the column was full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Iterate from bottom to top
        if board[r][col_index] == ' ':
            board[r][col_index] = checker
            return True, r  # Return True and the row where it was placed
    return False, -1 # Column is full


def check_win(board, checker):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the player has won, False otherwise.
    """

    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - WIN_CONDITION + 1):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-right to bottom-left)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(WIN_CONDITION - 1, NUM_COLS):
            if all(board[r + i][c - i] == checker for i in range(WIN_CONDITION)):
                return True

    return False


def check_draw(board):
    """
    Checks if the game is a draw (board is full).

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == ' ':
                return False  # An empty space found, not a draw yet
    return True  # Board is full


def get_player_input(current_player_checker):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker symbol of the current player.

    Returns:
        int: The 0-based index of the chosen column.
    """
    while True:
        try:
            user_input = input(f"Player {current_player_checker}, please enter a column: ").upper()
            col_index = get_column_index(user_input)

            if col_index == -1:
                print("Invalid input. Please enter a single uppercase letter (e.g., 'A').")
                continue
            return col_index
        except Exception:
            print("An unexpected error occurred. Please try again.")


# --- Main Game Logic ---
def play_game():
    """
    Manages the Connect 4 game flow.
    """
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)

    if NUM_COLS < WIN_CONDITION or NUM_ROWS < WIN_CONDITION:
        print(f"Error: Board dimensions ({NUM_ROWS}x{NUM_COLS}) are too small for a {WIN_CONDITION}-in-a-row win condition.")
        sys.exit(1)

    if NUM_COLS > 26:
        print("Error: Maximum 26 columns supported for letter labels (A-Z).")
        sys.exit(1)

    # Initialize game variables
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False

    while not game_over:
        current_player_checker = players[current_player_index]
        print_board(board)

        col_index = get_player_input(current_player_checker)

        # Validate column for placing checker
        if not is_valid_move(board, col_index):
            print("Column is full or out of bounds. Please choose another column.")
            # Player does not lose turn for invalid column choice (only for full column)
            continue

        # Place the checker
        placed, _ = place_checker(board, col_index, current_player_checker)
        if not placed: # This case should ideally be caught by is_valid_move, but for robustness
            print("Column is full. Please choose another column.")
            continue

        # Check for win
        if check_win(board, current_player_checker):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
