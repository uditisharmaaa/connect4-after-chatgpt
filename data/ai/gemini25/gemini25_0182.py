import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_CONDITION = 4  # Number of checkers in a row to win

# --- Global Variables ---
BOARD = []
PLAYER_CHECKERS = []


def initialize_game():
    """Initializes the game board and player checkers."""
    global BOARD, PLAYER_CHECKERS

    # Create an empty board filled with whitespaces
    BOARD = [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

    # Assign checkers to players
    PLAYER_CHECKERS = CHECKERS[:NUM_PLAYERS]


def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')


def print_board():
    """Prints the current state of the game board."""
    clear_screen()

    # Print column headers (A, B, C, ...)
    print("  ", end="")
    for i in range(NUM_COLS):
        print(f"{chr(ord('A') + i)}   ", end="")
    print()

    # Print the board rows
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        print("|", end="")
        for c in range(NUM_COLS):
            print(f" {BOARD[r][c]} |", end="")
        print()
    print("+---" * NUM_COLS + "+")


def get_column_input(current_player_index):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        player_char = PLAYER_CHECKERS[current_player_index]
        column_input = input(f"Player {player_char}, please enter a column: ").upper()

        if len(column_input) != 1:
            print("Invalid input. Please enter a single letter (e.g., A, B).")
            continue

        col_char = column_input[0]
        col_index = ord(col_char) - ord('A')

        if not (0 <= col_index < NUM_COLS):
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + NUM_COLS - 1)}.")
            continue

        if BOARD[0][col_index] != " ":  # Check if the top row of the column is full
            print("This column is full. Please choose another column.")
            continue

        return col_index


def place_checker(col_index, player_char):
    """
    Places the player's checker in the specified column at the lowest available spot.
    Returns True if successful, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Iterate from bottom to top
        if BOARD[r][col_index] == " ":
            BOARD[r][col_index] = player_char
            return True
    return False  # Should not be reached if validation in get_column_input is correct


def check_win(player_char):
    """
    Checks if the current player has achieved a winning condition (4 in a row).
    Checks horizontally, vertically, and diagonally.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(BOARD[r][c + i] == player_char for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - WIN_CONDITION + 1):
            if all(BOARD[r + i][c] == player_char for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(BOARD[r + i][c + i] == player_char for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(BOARD[r - i][c + i] == player_char for i in range(WIN_CONDITION)):
                return True

    return False


def check_draw():
    """Checks if the board is completely full, indicating a draw."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if BOARD[r][c] == " ":
                return False  # There's an empty space, not a draw
    return True  # Board is full


def main():
    """Main function to run the Connect 4 game."""
    initialize_game()

    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    while not game_over:
        print_board()

        player_char = PLAYER_CHECKERS[current_player_index]
        col_index = get_column_input(current_player_index)

        # Place the checker
        place_checker(col_index, player_char)

        # Check for win
        if check_win(player_char):
            print_board()  # Print final board with winning move
            print(f"Player {player_char} won!")
            game_over = True
        elif check_draw():
            print_board()  # Print final board
            print("It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
