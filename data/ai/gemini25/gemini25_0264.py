import os
import random
import string

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns due to letter labeling
NUM_PLAYERS = 2  # Between 2 and 5 players
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
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
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board_to_print):
    """
    Prints the Connect 4 board with column labels.

    Args:
        board_to_print (list): The 2D list representing the game board.
    """
    num_cols = len(board_to_print[0])
    # Print column labels (A, B, C, ...)
    print("  " + "   ".join(string.ascii_uppercase[:num_cols]))
    for r in range(len(board_to_print)):
        print("+---" * num_cols + "+")
        row_str = "|"
        for c in range(num_cols):
            row_str += f" {board_to_print[r][c]} |"
        print(row_str)
    print("+---" * num_cols + "+")

def get_column_index(col_char):
    """
    Converts a column letter (e.g., 'A') to its corresponding integer index.

    Args:
        col_char (str): The uppercase letter representing the column.

    Returns:
        int: The 0-based index of the column, or -1 if invalid.
    """
    if len(col_char) == 1 and 'A' <= col_char <= string.ascii_uppercase[NUM_COLS - 1]:
        return ord(col_char) - ord('A')
    return -1

def is_valid_input(input_str):
    """
    Checks if the player's input is a valid column letter.

    Args:
        input_str (str): The player's raw input.

    Returns:
        bool: True if the input is valid, False otherwise.
    """
    if len(input_str) != 1:
        return False
    col_char = input_str.upper()
    return 'A' <= col_char <= string.ascii_uppercase[NUM_COLS - 1]

def find_lowest_empty_row(col_index):
    """
    Finds the lowest empty row in a given column.

    Args:
        col_index (int): The 0-based index of the column.

    Returns:
        int: The 0-based index of the lowest empty row, or -1 if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col_index] == " ":
            return r
    return -1

def place_checker(col_index, player_checker):
    """
    Places a checker in the specified column.

    Args:
        col_index (int): The 0-based index of the column.
        player_checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was successfully placed, False if the column was full.
    """
    row_index = find_lowest_empty_row(col_index)
    if row_index != -1:
        board[row_index][col_index] = player_checker
        return True
    return False

def check_win(player_checker):
    """
    Checks if the current player has won the game.

    Args:
        player_checker (str): The checker symbol of the player to check.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - WIN_CONDITION + 1):
            if all(board[r + i][c] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True
    return False

def check_draw():
    """
    Checks if the board is full, indicating a draw.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False
    return True

# --- Main Game Logic ---

def game_loop():
    """Manages the main Connect 4 game loop."""
    global current_player_index
    global board

    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randrange(NUM_PLAYERS)

    game_over = False
    while not game_over:
        clear_screen()
        print_board(board)

        current_player_checker = CHECKERS[current_player_index]
        print(f"Player {current_player_checker}, please enter a column:")

        valid_turn = False
        while not valid_turn:
            user_input = input().strip().upper()

            if not is_valid_input(user_input):
                print(f"Invalid input. Please enter a letter between A and {string.ascii_uppercase[NUM_COLS-1]}.")
                continue

            col_index = get_column_index(user_input)
            if board[0][col_index] != " ":  # Check if the top row of the column is full
                print(f"Column {user_input} is full. Please choose another column.")
                continue

            if place_checker(col_index, current_player_checker):
                valid_turn = True
            else:
                # This case should ideally not be hit if board[0][col_index] check is robust
                print(f"Column {user_input} is full. Please choose another column.")

        # After a valid turn, check for win or draw
        if check_win(current_player_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw():
            clear_screen()
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    game_loop()
