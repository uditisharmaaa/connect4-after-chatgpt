import os
import random
import sys

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5 players
CHECKERS = ["X", "O", "V", "H", "M"]

# --- Global Variables ---
BOARD = []
PLAYER_CHECKERS = CHECKERS[:NUM_PLAYERS]
CURRENT_PLAYER_INDEX = 0

# --- Helper Functions ---

def clear_screen():
    """Clears the console screen."""
    os.system('clear')

def create_board():
    """Initializes the game board with empty spaces."""
    global BOARD
    BOARD = [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board():
    """Prints the current state of the game board."""
    clear_screen()

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_index in range(NUM_COLS):
        print(f"   {chr(ord('A') + col_index)}", end="")
    print("\n" + "+---" * (NUM_COLS + 1) + "+") # Adjusted for correct +---+ alignment

    # Print board rows
    for row in BOARD:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print("\n" + "+---" * (NUM_COLS + 1) + "+")

def get_column_from_input(prompt):
    """
    Prompts the user for a column input and validates it.
    Returns the 0-indexed column number if valid, otherwise None.
    """
    while True:
        try:
            user_input = input(prompt).strip().upper()
            if len(user_input) != 1:
                print("Invalid input: Please enter a single letter (e.g., A, B, C).")
                continue

            col_char = user_input[0]
            col_index = ord(col_char) - ord('A')

            if 0 <= col_index < NUM_COLS:
                return col_index
            else:
                print(f"Invalid input: Column '{col_char}' is out of bounds. Please choose between A and {chr(ord('A') + NUM_COLS - 1)}.")
        except Exception:
            print("Invalid input: Please enter a single letter (e.g., A, B, C).")

def drop_checker(col_index, checker):
    """
    Drops a checker into the specified column.
    Returns True if successful, False if the column is full.
    """
    for row_index in range(NUM_ROWS - 1, -1, -1):
        if BOARD[row_index][col_index] == " ":
            BOARD[row_index][col_index] = checker
            return True
    return False

def check_win(checker):
    """
    Checks if the current player has won the game.
    A win occurs if 4 checkers are in a row (horizontally, vertically, or diagonally).
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - 3):
            if all(BOARD[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLS):
            if all(BOARD[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (positive slope)
    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLS - 3):
            if all(BOARD[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (negative slope)
    for r in range(3, NUM_ROWS):
        for c in range(NUM_COLS - 3):
            if all(BOARD[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def check_draw():
    """
    Checks if the board is full, indicating a draw.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if BOARD[r][c] == " ":
                return False
    return True

# --- Main Game Logic ---

def game_setup():
    """Performs initial game setup."""
    global CURRENT_PLAYER_INDEX
    create_board()
    CURRENT_PLAYER_INDEX = random.randint(0, NUM_PLAYERS - 1)
    print_board()

def game_loop():
    """Main game loop."""
    global CURRENT_PLAYER_INDEX

    while True:
        current_checker = PLAYER_CHECKERS[CURRENT_PLAYER_INDEX]
        prompt = f"Player {current_checker}, please enter a column: "

        col_to_drop = get_column_from_input(prompt)
        if col_to_drop is None:
            # get_column_from_input already prints error messages, so just re-loop
            continue

        if not drop_checker(col_to_drop, current_checker):
            print(f"Column {chr(ord('A') + col_to_drop)} is full. You lose your turn.")
            # Player loses turn if column is full, so we move to next player.
            CURRENT_PLAYER_INDEX = (CURRENT_PLAYER_INDEX + 1) % NUM_PLAYERS
            continue # Loop to print board and continue game

        print_board()

        if check_win(current_checker):
            print(f"Player {current_checker} won!")
            break
        elif check_draw():
            print("It's a draw! The board is full.")
            break
        else:
            CURRENT_PLAYER_INDEX = (CURRENT_PLAYER_INDEX + 1) % NUM_PLAYERS

def main():
    """Entry point of the Connect 4 game."""
    if NUM_COLS > 26:
        print("Error: Maximum number of columns is 26 (A-Z). Please adjust NUM_COLS.")
        sys.exit(1)
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: Number of players must be between 2 and 5. Please adjust NUM_PLAYERS.")
        sys.exit(1)

    game_setup()
    game_loop()

if __name__ == "__main__":
    main()
