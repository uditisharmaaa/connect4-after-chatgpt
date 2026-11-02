import os
import random
import sys

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# --- Global Variables ---
board = []
current_player_index = 0

# --- Helper Functions ---


def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')


def create_board():
    """Initializes the game board with empty spaces."""
    global board
    board = [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]


def print_board():
    """Prints the current state of the game board."""
    clear_screen()
    # Print column labels (A, B, C...)
    print("  " + "   ".join([chr(ord('A') + i) for i in range(NUM_COLS)]))
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * NUM_COLS + "+")


def get_column_input(player_checker):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            col_char = input(f"Player {player_checker}, please enter a column: ").upper()
            if len(col_char) != 1 or not ('A' <= col_char <= chr(ord('A') + NUM_COLS - 1)):
                print(f"Invalid input. Please enter a single letter from A to {chr(ord('A') + NUM_COLS - 1)}.")
                continue

            col_index = ord(col_char) - ord('A')

            if board[0][col_index] != ' ':
                print("Column is full. Please choose another column.")
                continue

            return col_index
        except ValueError:
            print("Invalid input. Please enter a valid column letter.")


def drop_checker(col_index, player_checker):
    """
    Drops the player's checker into the specified column.
    Returns True if the checker was placed, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col_index] == ' ':
            board[r][col_index] = player_checker
            return True
    return False  # Should not be reached due to validation in get_column_input


def check_win(player_checker):
    """
    Checks if the given player has won the game.
    Checks horizontally, vertically, and diagonally.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[r][c + i] == player_checker for i in range(WIN_LENGTH)):
                return True

    # Check vertical
    for r in range(NUM_ROWS - WIN_LENGTH + 1):
        for c in range(NUM_COLS):
            if all(board[r + i][c] == player_checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_LENGTH + 1):
        for c in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == player_checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_LENGTH - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == player_checker for i in range(WIN_LENGTH)):
                return True

    return False


def check_draw():
    """Checks if the board is completely full (a draw)."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == ' ':
                return False
    return True


# --- Main Game Loop ---
def main():
    """Main function to run the Connect 4 game."""
    global current_player_index

    create_board()
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    while True:
        player_checker = PLAYER_CHECKERS[current_player_index]
        print_board()

        col_index = get_column_input(player_checker)

        # Drop the checker (validation ensures it's always placed)
        drop_checker(col_index, player_checker)

        print_board()  # Print board immediately after placing to show the move

        if check_win(player_checker):
            print(f"Player {player_checker} won!")
            break
        elif check_draw():
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
