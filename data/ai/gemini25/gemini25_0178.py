import os
import random

# --- Global Constants ---
NUM_ROWS = 6  # Number of rows on the board
NUM_COLS = 7  # Number of columns on the board (max 26 for 'A' to 'Z' labeling)
NUM_PLAYERS = 2  # Number of players (between 2 and 5)
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

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
    clear_screen()  # Clear screen before printing updated board

    # Print column headers (A, B, C, ...)
    print(" ", end="")
    for col_idx in range(NUM_COLS):
        print(f" {chr(ord('A') + col_idx)} ", end="")
    print("")

    # Print the board rows
    for row_idx in range(NUM_ROWS):
        print("+", end="")
        for _ in range(NUM_COLS):
            print("---+", end="")
        print("")

        print("|", end="")
        for col_idx in range(NUM_COLS):
            print(f" {board[row_idx][col_idx]} |", end="")
        print("")

    # Print the bottom border
    print("+", end="")
    for _ in range(NUM_COLS):
        print("---+", end="")
    print("")

def get_player_input(player_checker):
    """
    Prompts the current player for a column choice and validates the input.

    Args:
        player_checker (str): The checker symbol of the current player.

    Returns:
        int: The 0-indexed column chosen by the player.
    """
    while True:
        try:
            column_input = input(f"Player {player_checker}, please enter a column: ").upper()
            if len(column_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_char = column_input[0]
            if not ('A' <= col_char <= chr(ord('A') + NUM_COLS - 1)):
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + NUM_COLS - 1)}.")
                continue

            col_idx = ord(col_char) - ord('A')
            return col_idx
        except Exception:
            print("An unexpected error occurred. Please try again.")

def drop_checker(board, col_idx, player_checker):
    """
    Drops the player's checker into the specified column.

    Args:
        board (list): The game board.
        col_idx (int): The 0-indexed column to drop the checker into.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the checker was successfully placed, False if the column is full.
    """
    for row_idx in range(NUM_ROWS - 1, -1, -1):  # Start from the bottom row
        if board[row_idx][col_idx] == " ":
            board[row_idx][col_idx] = player_checker
            return True
    return False  # Column is full

def check_win(board, player_checker):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    # Check horizontal
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[row][col + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - WIN_CONDITION + 1):
            if all(board[row + i][col] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check positive diagonal (top-left to bottom-right)
    for row in range(NUM_ROWS - WIN_CONDITION + 1):
        for col in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[row + i][col + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check negative diagonal (top-right to bottom-left)
    for row in range(WIN_CONDITION - 1, NUM_ROWS):
        for col in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[row - i][col + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if board[row][col] == " ":
                return False  # Found an empty space, not a draw yet
    return True  # No empty spaces found, it's a draw

# --- Main Game Logic ---

def play_connect_4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)  # Randomly choose first player
    game_over = False
    winner_checker = None

    print_board(board)
    print(f"Player {PLAYER_CHECKERS[current_player_idx]} goes first!")

    while not game_over:
        player_checker = PLAYER_CHECKERS[current_player_idx]
        col_idx = -1
        input_valid = False

        while not input_valid:
            col_idx = get_player_input(player_checker)

            if not (0 <= col_idx < NUM_COLS):
                print(f"Invalid column index. Please choose a column between A and {chr(ord('A') + NUM_COLS - 1)}.")
                continue

            if not drop_checker(board, col_idx, player_checker):
                print(f"Column {chr(ord('A') + col_idx)} is full. Please choose another column.")
                # This player does not lose their turn for a full column
                continue
            else:
                input_valid = True

        print_board(board)

        if check_win(board, player_checker):
            winner_checker = player_checker
            game_over = True
            print(f"Player {winner_checker} won!")
        elif check_draw(board):
            game_over = True
            print("It's a draw!")
        else:
            # Switch to the next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

# --- Entry Point ---
if __name__ == "__main__":
    play_connect_4()
