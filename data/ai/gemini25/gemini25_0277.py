import os
import random
import sys

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
PLAYER_TOKENS = ["X", "O", "V", "H", "M"]

# --- Global Variables ---
board = []
current_player_index = 0

# --- Helper Functions ---


def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')


def create_board():
    """Creates an empty game board initialized with spaces."""
    global board
    board = [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]


def print_board():
    """Prints the current state of the game board."""
    clear_screen()

    # Print column headers (A, B, C, ...)
    sys.stdout.write("  ")
    for col in range(NUM_COLS):
        sys.stdout.write(f" {chr(ord('A') + col)} ")
    sys.stdout.write("\n")

    # Print board rows
    for r in range(NUM_ROWS):
        sys.stdout.write("+")
        for _ in range(NUM_COLS):
            sys.stdout.write("---+")
        sys.stdout.write("\n")
        sys.stdout.write("|")
        for c in range(NUM_COLS):
            sys.stdout.write(f" {board[r][c]} |")
        sys.stdout.write("\n")

    sys.stdout.write("+")
    for _ in range(NUM_COLS):
        sys.stdout.write("---+")
    sys.stdout.write("\n")


def get_column_input(player_token):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            col_char = input(f"Player {player_token}, please enter a column: ").upper()
            if len(col_char) != 1 or not ('A' <= col_char <= chr(ord('A') + NUM_COLS - 1)):
                print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + NUM_COLS - 1)}.")
                continue

            col = ord(col_char) - ord('A')
            return col
        except Exception:
            print("Invalid input. Please enter a single letter.")


def drop_checker(col, player_token):
    """
    Drops the player's checker into the specified column.
    Returns True if successful, False if the column is full.
    """
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_token
            return True
    return False


def check_win(player_token):
    """
    Checks if the given player has won the game.
    Checks horizontally, vertically, and diagonally.
    """

    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c + i] == player_token for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - WIN_CONDITION + 1):
            if all(board[r + i][c] == player_token for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == player_token for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == player_token for i in range(WIN_CONDITION)):
                return True

    return False


def check_draw():
    """Checks if the board is completely full, indicating a draw."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False
    return True


def main():
    """Main function to run the Connect 4 game."""
    global current_player_index

    create_board()
    
    # Select a random first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    while True:
        player_token = PLAYER_TOKENS[current_player_index]
        print_board()
        print(f"Player {player_token}, it is your turn.")

        col_input = get_column_input(player_token)

        if not drop_checker(col_input, player_token):
            print(f"Column {chr(ord('A') + col_input)} is full! You lose your turn.")
            # Player does not lose turn, they are asked again for valid input as per requirements
            continue

        if check_win(player_token):
            print_board()
            print(f"Player {player_token} won!")
            break

        if check_draw():
            print_board()
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
