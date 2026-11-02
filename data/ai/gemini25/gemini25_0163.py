import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers needed to win

# Player checkers (max 5 players)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]


# --- Utility Functions ---
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
        list[list[str]]: A 2D list representing the game board,
                         initialized with whitespaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list[list[str]]): The current state of the game board.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col_idx in range(num_cols):
        print(f" {chr(ord('A') + col_idx)} ", end="")
    print()

    # Print board content
    for r in range(num_rows):
        print("+", end="")
        for _ in range(num_cols):
            print("---+", end="")
        print()
        print("|", end="")
        for c in range(num_cols):
            print(f" {board[r][c]} |", end="")
        print()
    print("+", end="")
    for _ in range(num_cols):
        print("---+", end="")
    print()


def get_column_from_input(prompt, num_cols):
    """
    Prompts the player for a column input and validates it.

    Args:
        prompt (str): The message to display to the player.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-indexed column number if the input is valid.
             Returns -1 if input is 'q' to quit (not explicitly part of spec,
             but good for testing).
    """
    while True:
        col_input = input(prompt).strip().upper()
        if col_input == 'Q':  # Added for graceful exit during testing
            return -1

        if len(col_input) == 1 and 'A' <= col_input <= chr(ord('A') + num_cols - 1):
            return ord(col_input) - ord('A')
        else:
            print("Invalid input. Please enter a single uppercase letter "
                  f"from A to {chr(ord('A') + num_cols - 1)}.")


def place_checker(board, col, checker):
    """
    Places a checker in the specified column.

    Args:
        board (list[list[str]]): The game board.
        col (int): The 0-indexed column to place the checker.
        checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was placed successfully, False if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Start from bottom row
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False  # Column is full


def check_win(board, checker, win_condition):
    """
    Checks if the current player has won the game.

    Args:
        board (list[list[str]]): The game board.
        checker (str): The checker symbol of the current player.
        win_condition (int): The number of checkers needed in a row to win.

    Returns:
        bool: True if the current player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r][c + i] == checker for i in range(win_condition)):
                return True

    # Check vertical
    for c in range(num_cols):
        for r in range(num_rows - win_condition + 1):
            if all(board[r + i][c] == checker for i in range(win_condition)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols - win_condition + 1):
            if all(board[r + i][c + i] == checker for i in range(win_condition)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(win_condition - 1, num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r - i][c + i] == checker for i in range(win_condition)):
                return True

    return False


def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

    Args:
        board (list[list[str]]): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True  # Board is full


# --- Main Game Logic ---
def play_connect_4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]

    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    clear_screen()
    print_board(board)
    print(f"Player {players[current_player_idx]} goes first!\n")

    game_over = False
    winner = None

    while not game_over:
        current_checker = players[current_player_idx]

        while True:
            column_prompt = f"Player {current_checker}, please enter a column: "
            chosen_col_idx = get_column_from_input(column_prompt, NUM_COLS)

            if chosen_col_idx == -1: # Allows quitting during testing
                game_over = True
                break

            if 0 <= chosen_col_idx < NUM_COLS:
                if place_checker(board, chosen_col_idx, current_checker):
                    break  # Checker placed successfully, exit inner loop
                else:
                    clear_screen()
                    print_board(board)
                    print(f"Column {chr(ord('A') + chosen_col_idx)} is full. Please choose another column.")
            # If input was invalid format, get_column_from_input already printed message
        
        if game_over: # If player chose to quit
            break

        clear_screen()
        print_board(board)

        if check_win(board, current_checker, WIN_CONDITION):
            winner = current_checker
            game_over = True
        elif check_draw(board):
            game_over = True
        else:
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

    # --- Game End ---
    if winner:
        print(f"Player {winner} won!")
    elif game_over:  # Only if game_over was set by draw, not by player quitting
        print("It's a draw!")
    else:
        print("Game quit.") # If player chose to quit


if __name__ == "__main__":
    play_connect_4()
