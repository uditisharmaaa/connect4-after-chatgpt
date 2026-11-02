import os
import random
import sys

# --- Global Constants ---
# Board dimensions
NUM_ROWS = 6
NUM_COLS = 7  # Maximum 26 columns (A-Z)

# Number of players (between 2 and 5)
NUM_PLAYERS = 2

# Player checkers
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# Number of checkers in a row to win
WIN_CONDITION = 4

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows on the board.
        cols (int): The number of columns on the board.

    Returns:
        list: A 2D list representing the game board, initialized with spaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()

    # Print column labels (A, B, C, ...)
    sys.stdout.write("  ")
    for i in range(len(board[0])):
        sys.stdout.write(f" {chr(ord('A') + i)}  ")
    sys.stdout.write("\n")

    # Print board rows and cells
    for r_idx, row in enumerate(board):
        sys.stdout.write("+")
        sys.stdout.write("---+" * len(row))
        sys.stdout.write("\n")
        sys.stdout.write("|")
        for cell in row:
            sys.stdout.write(f" {cell} |")
        sys.stdout.write("\n")

    sys.stdout.write("+")
    sys.stdout.write("---+" * len(board[0]))
    sys.stdout.write("\n")

def get_column_input(current_player_checker, board_cols):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker of the current player.
        board_cols (int): The number of columns on the board.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            prompt_message = f"Player {current_player_checker}, please enter a column: "
            column_input = input(prompt_message).upper()

            # Check if input is a single letter
            if len(column_input) != 1 or not 'A' <= column_input <= chr(ord('A') + board_cols - 1):
                print(f"Invalid input. Please enter a single letter between A and {chr(ord('A') + board_cols - 1)}.")
                continue

            # Convert letter to 0-indexed column number
            col_index = ord(column_input) - ord('A')
            return col_index
        except Exception:
            # Catch any unexpected errors, though the specific checks above handle most cases
            print("Invalid input. Please try again.")

def drop_checker(board, col_index, player_checker):
    """
    Places the player's checker in the lowest available space of the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-indexed column number to drop the checker into.
        player_checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was successfully placed, False if the column is full.
    """
    # Iterate from the bottom row upwards
    for row_index in range(len(board) - 1, -1, -1):
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = player_checker
            return True  # Checker placed successfully
    return False  # Column is full

def check_win(board, player_checker, win_condition):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The 2D list representing the game board.
        player_checker (str): The checker symbol for the current player.
        win_condition (int): The number of checkers in a row required to win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal wins
    for r in range(num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check vertical wins
    for c in range(num_cols):
        for r in range(num_rows - win_condition + 1):
            if all(board[r + i][c] == player_checker for i in range(win_condition)):
                return True

    # Check positively sloped diagonal wins (bottom-left to top-right)
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols - win_condition + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check negatively sloped diagonal wins (top-left to bottom-right)
    for r in range(win_condition - 1, num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r - i][c + i] == player_checker for i in range(win_condition)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely filled, indicating a draw.

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full (draw), False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # An empty space still exists
    return True  # Board is full

# --- Main Game Logic ---

def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    players = CHECKERS # List of player checkers

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player_checker = players[current_player_index]

    game_over = False

    while not game_over:
        print_board(board)
        # Indicate whose turn it is
        sys.stdout.write(f"Player {current_player_checker}, please enter a column:\n")

        valid_turn = False
        while not valid_turn:
            col_input_index = get_column_input(current_player_checker, NUM_COLS)

            # Check if the chosen column is full
            if board[0][col_input_index] != " ":
                print("That column is full. Please choose another column.")
                continue # Player does not lose turn, asked to input again

            # Drop the checker and validate the turn
            if drop_checker(board, col_input_index, current_player_checker):
                valid_turn = True
            else:
                # This case should ideally be caught by the board[0][col_input_index] check,
                # but it's a fallback if drop_checker logic changes.
                print("Failed to place checker. Column might be full (unexpected). Please try again.")

        # After a valid turn, print the board again
        print_board(board)

        # Check for win
        if check_win(board, current_player_checker, WIN_CONDITION):
            print(f"Player {current_player_checker} won!")
            game_over = True
        # Check for draw if no win
        elif check_draw(board):
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            current_player_checker = players[current_player_index]

    print("\nGame Over!")

# Entry point of the script
if __name__ == "__main__":
    play_game()
