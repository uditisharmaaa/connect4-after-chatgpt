import os
import random
import sys

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
CHECKERS = ["X", "O", "V", "H", "M"]

# --- Helper Functions ---

def clear_screen():
    """Clears the console screen."""
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
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    num_cols = len(board[0])
    num_rows = len(board)

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(num_cols):
        print(f" {chr(ord('A') + col_index)} ", end="")
    print()

    # Print the board content
    for r_idx in range(num_rows):
        print("+", end="")
        for _ in range(num_cols):
            print("---+", end="")
        print()
        print("|", end="")
        for c_idx in range(num_cols):
            print(f" {board[r_idx][c_idx]} |", end="")
        print()
    print("+", end="")
    for _ in range(num_cols):
        print("---+", end="")
    print()

def get_column_input(player_checker, num_cols):
    """
    Prompts the current player for a column input and validates it.

    Args:
        player_checker (str): The checker symbol of the current player.
        num_cols (int): The number of columns on the board.

    Returns:
        int: The 0-indexed column number if the input is valid.
    """
    while True:
        try:
            prompt = f"Player {player_checker}, please enter a column: "
            col_char = input(prompt).strip().upper()

            if not col_char.isalpha() or len(col_char) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B).")
                continue

            col_index = ord(col_char) - ord('A')

            if 0 <= col_index < num_cols:
                return col_index
            else:
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")
        except Exception:
            print("An unexpected error occurred. Please try again.")

def drop_checker(board, col_index, player_checker):
    """
    Drops the player's checker into the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-indexed column number.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the checker was successfully dropped, False if the column is full.
    """
    num_rows = len(board)
    for r_idx in range(num_rows - 1, -1, -1):  # Iterate from bottom to top
        if board[r_idx][col_index] == " ":
            board[r_idx][col_index] = player_checker
            return True
    return False  # Column is full

def check_win(board, player_checker, win_condition):
    """
    Checks if the given player has won the game.

    Args:
        board (list): The 2D list representing the game board.
        player_checker (str): The checker symbol to check for.
        win_condition (int): The number of checkers in a row needed to win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal wins
    for r_idx in range(num_rows):
        for c_idx in range(num_cols - win_condition + 1):
            if all(board[r_idx][c_idx + i] == player_checker for i in range(win_condition)):
                return True

    # Check vertical wins
    for c_idx in range(num_cols):
        for r_idx in range(num_rows - win_condition + 1):
            if all(board[r_idx + i][c_idx] == player_checker for i in range(win_condition)):
                return True

    # Check diagonal wins (top-left to bottom-right)
    for r_idx in range(num_rows - win_condition + 1):
        for c_idx in range(num_cols - win_condition + 1):
            if all(board[r_idx + i][c_idx + i] == player_checker for i in range(win_condition)):
                return True

    # Check diagonal wins (bottom-left to top-right)
    for r_idx in range(win_condition - 1, num_rows):
        for c_idx in range(num_cols - win_condition + 1):
            if all(board[r_idx - i][c_idx + i] == player_checker for i in range(win_condition)):
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
    for r_idx in range(len(board)):
        for c_idx in range(len(board[0])):
            if board[r_idx][c_idx] == " ":
                return False
    return True

# --- Main Game Logic ---

def play_connect_4():
    """
    Main function to play a game of Connect 4.
    """
    # Initialize game
    game_board = create_board(NUM_ROWS, NUM_COLS)
    players_checkers = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    print("Welcome to Connect 4!")
    input("Press Enter to start...")

    while not game_over:
        current_player_checker = players_checkers[current_player_index]
        print_board(game_board)

        valid_turn = False
        while not valid_turn:
            col_chosen = get_column_input(current_player_checker, NUM_COLS)
            if drop_checker(game_board, col_chosen, current_player_checker):
                valid_turn = True
            else:
                print(f"Column {chr(ord('A') + col_chosen)} is full. Please choose another column.")

        print_board(game_board)  # Print board after checker drop

        if check_win(game_board, current_player_checker, WIN_CONDITION):
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(game_board):
            print("The board is full. It's a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print("Game Over!")

if __name__ == "__main__":
    play_connect_4()
