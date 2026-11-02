import os
import random
import string

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_CONDITION = 4  # Number of checkers in a row to win

# --- Global Variables ---
board = []
current_player_index = 0

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
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board_data):
    """
    Prints the Connect 4 board to the console.

    Args:
        board_data (list): The 2D list representing the game board.
    """
    num_rows = len(board_data)
    num_cols = len(board_data[0])

    # Print column labels (A, B, C, ...)
    print("  " + "   ".join(string.ascii_uppercase[:num_cols]))

    # Print board content
    for r in range(num_rows):
        print("+---" * num_cols + "+")
        row_str = "|"
        for c in range(num_cols):
            row_str += f" {board_data[r][c]} |"
        print(row_str)
    print("+---" * num_cols + "+")

def get_column_input(num_cols):
    """
    Prompts the current player for a column input and validates it.

    Args:
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-indexed column number if input is valid.
    """
    while True:
        player_char = PLAYER_CHECKERS[current_player_index]
        column_input = input(f"Player {player_char}, please enter a column: ").strip().upper()

        if len(column_input) != 1:
            print("Invalid input. Please enter a single letter (e.g., A, B, C).")
            continue

        if not 'A' <= column_input <= string.ascii_uppercase[num_cols - 1]:
            print(f"Invalid column. Please choose a column between A and {string.ascii_uppercase[num_cols - 1]}.")
            continue

        col_index = ord(column_input) - ord('A')
        return col_index

def place_checker(board_data, col_index, checker):
    """
    Places a checker in the lowest available space of a given column.

    Args:
        board_data (list): The 2D list representing the game board.
        col_index (int): The 0-indexed column where the checker is to be placed.
        checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was successfully placed, False if the column is full.
    """
    num_rows = len(board_data)
    for r in range(num_rows - 1, -1, -1):  # Iterate from bottom row up
        if board_data[r][col_index] == ' ':
            board_data[r][col_index] = checker
            return True
    return False  # Column is full

def check_win(board_data, checker):
    """
    Checks if the given checker has formed a winning line (4 in a row)
    horizontally, vertically, or diagonally.

    Args:
        board_data (list): The 2D list representing the game board.
        checker (str): The checker symbol to check for a win.

    Returns:
        bool: True if the checker has won, False otherwise.
    """
    num_rows = len(board_data)
    num_cols = len(board_data[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - WIN_CONDITION + 1):
            if all(board_data[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for c in range(num_cols):
        for r in range(num_rows - WIN_CONDITION + 1):
            if all(board_data[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(num_rows - WIN_CONDITION + 1):
        for c in range(num_cols - WIN_CONDITION + 1):
            if all(board_data[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, num_rows):
        for c in range(num_cols - WIN_CONDITION + 1):
            if all(board_data[r - i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board_data):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board_data (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board_data)):
        for c in range(len(board_data[0])):
            if board_data[r][c] == ' ':
                return False  # Found an empty space, not a draw
    return True  # Board is full

# --- Main Game Logic ---

def game_setup():
    """Initializes the game board and selects the first player."""
    global board, current_player_index
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

def play_game():
    """Manages the main game loop."""
    global current_player_index

    game_over = False
    winner = None

    while not game_over:
        clear_screen()
        print_board(board)

        current_checker = PLAYER_CHECKERS[current_player_index]
        
        placement_successful = False
        while not placement_successful:
            col_index = get_column_input(NUM_COLS)
            if place_checker(board, col_index, current_checker):
                placement_successful = True
            else:
                print("Column is full! Please choose another column.")
                # Player does not lose turn, re-prompt for input
                
        # After a successful placement, clear and print the board again
        clear_screen()
        print_board(board)

        if check_win(board, current_checker):
            winner = current_checker
            game_over = True
        elif check_draw(board):
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Game over, print results
    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")

# --- Entry Point ---

if __name__ == "__main__":
    game_setup()
    play_game()
