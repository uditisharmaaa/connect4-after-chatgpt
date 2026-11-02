import os
import random
import sys

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- Global Variables ---
BOARD = []
CURRENT_PLAYER_INDEX = 0

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board():
    """Initializes the game board with empty spaces."""
    global BOARD
    BOARD = [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board():
    """Prints the current state of the game board."""
    clear_screen()
    
    # Print column headers (A, B, C, ...)
    print("  ", end="")
    for i in range(NUM_COLS):
        print(f"{chr(ord('A') + i)}   ", end="")
    print()

    # Print board rows
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        print("|", end="")
        for c in range(NUM_COLS):
            print(f" {BOARD[r][c]} |", end="")
        print()
    print("+---" * NUM_COLS + "+")

def get_column_input():
    """Prompts the current player for a column input and validates it."""
    while True:
        try:
            player_char = CHECKERS[CURRENT_PLAYER_INDEX]
            col_input = input(f"Player {player_char}, please enter a column: ").upper()

            if not col_input.isalpha() or len(col_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(col_input) - ord('A')

            if not (0 <= col_index < NUM_COLS):
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + NUM_COLS - 1)}.")
                continue
            
            # Check if column is full
            if BOARD[0][col_index] != " ":
                print("Column is full. Please choose another column.")
                continue

            return col_index

        except ValueError:
            print("Invalid input. Please enter a valid column letter.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def drop_checker(col_index, player_char):
    """Drops the player's checker into the specified column."""
    for r in range(NUM_ROWS - 1, -1, -1):
        if BOARD[r][col_index] == " ":
            BOARD[r][col_index] = player_char
            return True
    return False # Should not be reached if column full check is done before calling

def check_win(player_char):
    """Checks if the current player has won the game."""
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(BOARD[r][c + i] == player_char for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS):
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
    """Checks if the board is full, indicating a draw."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if BOARD[r][c] == " ":
                return False  # Board is not full
    return True  # Board is full

# --- Main Game Logic ---

def game_loop():
    """Main function to run the Connect 4 game."""
    global CURRENT_PLAYER_INDEX

    create_board()
    CURRENT_PLAYER_INDEX = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board()
        current_player_char = CHECKERS[CURRENT_PLAYER_INDEX]
        
        col_index = get_column_input()
        
        drop_successful = drop_checker(col_index, current_player_char)
        
        # If drop_checker returns False, it means the column was full,
        # but get_column_input already handles this, so it should always be True here.

        if check_win(current_player_char):
            print_board()
            print(f"Player {current_player_char} won!")
            break
        
        if check_draw():
            print_board()
            print("It's a draw!")
            break

        # Switch to the next player
        CURRENT_PLAYER_INDEX = (CURRENT_PLAYER_INDEX + 1) % NUM_PLAYERS

if __name__ == "__main__":
    game_loop()
