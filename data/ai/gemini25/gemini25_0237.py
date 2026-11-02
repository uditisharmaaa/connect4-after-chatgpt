import os
import random
import sys

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5
WIN_CONDITION = 4

# Player checkers, ordered for selection
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# --- Global Variables ---
board = []
players = []  # List of checker symbols for active players

# --- Utility Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board():
    """Initializes the game board with empty spaces."""
    global board
    board = [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board():
    """Prints the current state of the game board."""
    clear_screen()

    # Print column labels
    sys.stdout.write("  ")
    for col_idx in range(NUM_COLS):
        sys.stdout.write(f" {chr(ord('A') + col_idx)} ")
    sys.stdout.write("\n")

    # Print board rows
    for row_idx in range(NUM_ROWS):
        sys.stdout.write("+")
        for _ in range(NUM_COLS):
            sys.stdout.write("---+")
        sys.stdout.write("\n")

        sys.stdout.write("|")
        for col_idx in range(NUM_COLS):
            sys.stdout.write(f" {board[row_idx][col_idx]} |")
        sys.stdout.write("\n")
    
    # Print bottom border
    sys.stdout.write("+")
    for _ in range(NUM_COLS):
        sys.stdout.write("---+")
    sys.stdout.write("\n")

def get_column_input(current_player_checker):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            col_char = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if not col_char.isalpha() or len(col_char) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(col_char) - ord('A')

            if not (0 <= col_index < NUM_COLS):
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + NUM_COLS - 1)}.")
                continue

            return col_index
        except Exception:
            print("Invalid input. Please try again.")

def place_checker(col_index, current_player_checker):
    """
    Places the checker in the specified column.
    Returns True if successful, False if the column is full.
    """
    for row_idx in range(NUM_ROWS - 1, -1, -1):
        if board[row_idx][col_index] == " ":
            board[row_idx][col_index] = current_player_checker
            return True
    return False

def check_win(current_player_checker):
    """
    Checks if the current player has achieved a Connect 4.
    Returns True if a win is found, False otherwise.
    """

    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c + i] == current_player_checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - WIN_CONDITION + 1):
            if all(board[r + i][c] == current_player_checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == current_player_checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == current_player_checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw():
    """
    Checks if the board is completely filled (draw condition).
    Returns True if it's a draw, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True  # No empty spaces found, it's a draw

def main():
    """Main function to run the Connect 4 game."""
    global players

    # Initialization
    create_board()
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    while not game_over:
        current_player_checker = players[current_player_index]
        print_board()

        column_full = True
        chosen_col_index = -1

        while column_full:
            chosen_col_index = get_column_input(current_player_checker)
            column_full = not place_checker(chosen_col_index, current_player_checker)
            if column_full:
                print(f"Column {chr(ord('A') + chosen_col_index)} is full. Please choose another column.")
                # Player does not lose turn, re-prompt

        print_board() # Print board after successful placement

        if check_win(current_player_checker):
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw():
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
