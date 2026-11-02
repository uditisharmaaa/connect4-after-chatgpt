import os
import random
import sys

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (up to 5 players)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
CURRENT_PLAYERS = PLAYER_CHECKERS[:NUM_PLAYERS]

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

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
    clear_screen()
    num_cols = len(board[0])

    # Print column headers (A, B, C, ...)
    print("  " + "   ".join([chr(ord('A') + i) for i in range(num_cols)]))

    # Print board rows
    for r in range(len(board)):
        print("+---" * num_cols + "+")
        row_str = "|"
        for c in range(num_cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * num_cols + "+")

def get_column_input(current_player_checker, num_cols):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker symbol of the current player.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The validated column index (0-based).
    """
    while True:
        try:
            prompt = f"Player {current_player_checker}, please enter a column: "
            user_input = input(prompt).strip().upper()

            if not user_input:
                print("Input cannot be empty. Please enter a column letter.")
                continue

            if len(user_input) != 1 or not ('A' <= user_input <= chr(ord('A') + num_cols - 1)):
                print(f"Invalid input. Please enter a single letter from A to {chr(ord('A') + num_cols - 1)}.")
                continue

            col_index = ord(user_input) - ord('A')
            return col_index
        except Exception:
            print(f"Invalid input. Please enter a single letter from A to {chr(ord('A') + num_cols - 1)}.")

def place_checker(board, col_index, checker):
    """
    Places the checker in the lowest available space of the given column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-based index of the column to place the checker.
        checker (str): The checker symbol to place.

    Returns:
        bool: True if the checker was successfully placed, False if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Iterate from bottom to top
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """
    Checks if the given player (checker) has won the game.

    Args:
        board (list): The 2D list representing the game board.
        checker (str): The checker symbol of the player to check for a win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for r in range(num_rows - WIN_CONDITION + 1):
        for c in range(num_cols):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(num_rows - WIN_CONDITION + 1):
        for c in range(num_cols - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, num_rows):
        for c in range(num_cols - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # An empty space is found, not a draw
    return True  # Board is full

# --- Main Game Logic ---

def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner_checker = None

    print_board(board)
    print(f"Player {CURRENT_PLAYERS[current_player_index]} starts!")

    while not game_over:
        current_player_checker = CURRENT_PLAYERS[current_player_index]

        col_index = get_column_input(current_player_checker, NUM_COLS)

        if place_checker(board, col_index, current_player_checker):
            print_board(board)

            if check_win(board, current_player_checker):
                winner_checker = current_player_checker
                game_over = True
            elif check_draw(board):
                game_over = True
            else:
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            print(f"Column {chr(ord('A') + col_index)} is full. Player {current_player_checker} loses their turn!")
            # Note: The assignment says "the turn is invalid and the player loses the turn."
            # This implementation makes the player lose the turn if the column is full.
            # If the intent was for them to try again, the `else` block above would `continue`
            # and not advance `current_player_index`. Sticking to the text.
            current_player_index = (current_player_index + 1) % NUM_PLAYERS # Advance turn even on full column

    print_board(board) # Print final state of the board

    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    play_game()
