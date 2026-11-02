import os
import random
import string

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_CONDITION = 4  # Number of checkers in a row to win

# --- Global Variables (initialized later) ---
board = []
player_turn_index = 0

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Initializes the game board with empty spaces."""
    global board
    board = [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board():
    """Prints the current state of the Connect 4 board."""
    clear_screen()
    # Print column labels (A, B, C, ...)
    print("  " + "   ".join(string.ascii_uppercase[:NUM_COLS]))
    
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * NUM_COLS + "+")

def get_column_input(current_player_checker):
    """
    Prompts the current player for column input and validates it.
    Returns the valid column index (0-based).
    """
    while True:
        try:
            col_char = input(f"Player {current_player_checker}, please enter a column: ").upper()
            
            # 1. Check if input is a single character
            if len(col_char) != 1:
                print("Invalid input: Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(col_char) - ord('A')

            # 2. Check if column index is within board bounds
            if not (0 <= col_index < NUM_COLS):
                print(f"Invalid column: Please enter a letter between A and {string.ascii_uppercase[NUM_COLS - 1]}.")
                continue

            # 3. Check if the column is full
            if board[0][col_index] != " ":
                print("That column is full! Please choose another column.")
                continue

            return col_index
        except TypeError: # Should not happen with validation above, but good for robustness
            print("Invalid input: Please enter a valid column letter.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")

def place_checker(col_index, checker):
    """
    Places the given checker in the lowest available spot of the specified column.
    Returns True if successful, False if the column is full (should be handled by validation).
    """
    for r in range(NUM_ROWS - 1, -1, -1): # Iterate from bottom row upwards
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True
    return False # Should not be reached if validation is correct

def check_win(checker):
    """
    Checks if the given player's checker has achieved a win condition (4 in a row).
    Checks horizontally, vertically, and diagonally.
    """
    # Helper function to check a specific direction
    def check_direction(r_start, c_start, dr, dc, current_checker):
        count = 0
        for i in range(WIN_CONDITION):
            r = r_start + i * dr
            c = c_start + i * dc
            if not (0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == current_checker):
                return False
        return True

    # 1. Check Horizontal wins
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if check_direction(r, c, 0, 1, checker):
                return True

    # 2. Check Vertical wins
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - WIN_CONDITION + 1):
            if check_direction(r, c, 1, 0, checker):
                return True

    # 3. Check Diagonal (top-left to bottom-right) wins
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if check_direction(r, c, 1, 1, checker):
                return True

    # 4. Check Diagonal (bottom-left to top-right) wins
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if check_direction(r, c, -1, 1, checker):
                return True

    return False

def check_draw():
    """Checks if the board is completely full, indicating a draw."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True  # No empty spaces found, it's a draw

# --- Main Game Logic ---

def play_game():
    """Main function to run the Connect 4 game."""
    global player_turn_index

    create_board()

    # Randomly select the first player
    player_turn_index = random.randint(0, NUM_PLAYERS - 1)
    print(f"Player {CHECKERS[player_turn_index]} goes first!")
    input("Press Enter to start...")

    game_over = False
    winner_checker = None

    while not game_over:
        current_player_checker = CHECKERS[player_turn_index]
        print_board()

        col_index = get_column_input(current_player_checker)
        place_checker(col_index, current_player_checker)

        if check_win(current_player_checker):
            winner_checker = current_player_checker
            game_over = True
        elif check_draw():
            game_over = True
        else:
            # Switch to the next player
            player_turn_index = (player_turn_index + 1) % NUM_PLAYERS
    
    # Game Over
    print_board() # Print final board state

    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("It's a draw! The board is full.")

# --- Run the game ---
if __name__ == "__main__":
    play_game()
