import os
import random
import sys

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
CHECKERS = ["X", "O", "V", "H", "M"]

# --- Global Variables ---
BOARD = []
PLAYER_COLORS = CHECKERS[:NUM_PLAYERS]
CURRENT_PLAYER_INDEX = 0

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Initializes a new empty game board."""
    global BOARD
    BOARD = [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board():
    """Prints the current state of the game board."""
    clear_screen()
    
    # Print column labels
    sys.stdout.write("  ")
    for i in range(NUM_COLS):
        sys.stdout.write(f" {chr(ord('A') + i)} ")
    sys.stdout.write("\n")

    # Print board content
    for r in range(NUM_ROWS):
        sys.stdout.write("+")
        for _ in range(NUM_COLS):
            sys.stdout.write("---+")
        sys.stdout.write("\n")

        sys.stdout.write("|")
        for c in range(NUM_COLS):
            sys.stdout.write(f" {BOARD[r][c]} |")
        sys.stdout.write("\n")
    
    sys.stdout.write("+")
    for _ in range(NUM_COLS):
        sys.stdout.write("---+")
    sys.stdout.write("\n")

def get_column_input():
    """Prompts the current player for a column input and validates it."""
    while True:
        player_char = PLAYER_COLORS[CURRENT_PLAYER_INDEX]
        col_input = input(f"Player {player_char}, please enter a column: ").strip().upper()

        if not col_input:
            print("Invalid input. Please enter a column letter (e.g., A).")
            continue
            
        col_char = col_input[0]

        if len(col_input) > 1 or not ('A' <= col_char <= chr(ord('A') + NUM_COLS - 1)):
            print("Invalid column. Please enter a valid column letter.")
            continue

        col_index = ord(col_char) - ord('A')

        if BOARD[0][col_index] != " ":
            print("Column is full. Please choose another column.")
            continue

        return col_index

def place_checker(col_index):
    """Places the current player's checker in the specified column."""
    player_char = PLAYER_COLORS[CURRENT_PLAYER_INDEX]
    for r in range(NUM_ROWS - 1, -1, -1):
        if BOARD[r][col_index] == " ":
            BOARD[r][col_index] = player_char
            return True
    return False # Should not be reached due to validation in get_column_input

def check_win(player_char):
    """Checks if the given player has won the game."""

    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(BOARD[r][c+i] == player_char for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - WIN_CONDITION + 1):
            if all(BOARD[r+i][c] == player_char for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(BOARD[r+i][c+i] == player_char for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(BOARD[r-i][c+i] == player_char for i in range(WIN_CONDITION)):
                return True
    return False

def check_draw():
    """Checks if the board is full, indicating a draw."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if BOARD[r][c] == " ":
                return False
    return True

def switch_player():
    """Switches the turn to the next player."""
    global CURRENT_PLAYER_INDEX
    CURRENT_PLAYER_INDEX = (CURRENT_PLAYER_INDEX + 1) % NUM_PLAYERS

# --- Main Game Logic ---

def main():
    """Main function to run the Connect 4 game."""
    global CURRENT_PLAYER_INDEX

    create_board()
    CURRENT_PLAYER_INDEX = random.randint(0, NUM_PLAYERS - 1) # Randomly select first player
    
    game_over = False
    winner_char = None

    while not game_over:
        print_board()
        
        col_index = get_column_input()
        place_checker(col_index)

        player_char = PLAYER_COLORS[CURRENT_PLAYER_INDEX]

        if check_win(player_char):
            game_over = True
            winner_char = player_char
        elif check_draw():
            game_over = True
        else:
            switch_player()
    
    print_board() # Print final board state
    if winner_char:
        print(f"Player {winner_char} won!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main()
