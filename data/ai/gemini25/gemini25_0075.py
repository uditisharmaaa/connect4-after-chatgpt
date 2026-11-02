import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5 players
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_CONDITION = 4  # Number of checkers in a row to win

# --- Global Variables ---
board = []
current_player_index = 0

# --- Helper Functions ---
def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def get_column_letter(col_index):
    """Converts a column index (0-25) to its corresponding letter (A-Z)."""
    return chr(ord('A') + col_index)

def get_column_index(col_letter):
    """Converts a column letter (A-Z) to its corresponding index (0-25)."""
    return ord(col_letter.upper()) - ord('A')

def initialize_board():
    """Initializes the game board with empty spaces."""
    global board
    board = [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board():
    """Prints the current state of the game board."""
    clear_screen()

    # Print column headers (A, B, C, ...)
    print("  " + "   ".join([get_column_letter(i) for i in range(NUM_COLS)]))
    
    # Print board rows
    for r in range(NUM_ROWS):
        print("+" + "---+" * NUM_COLS)
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+" + "---+" * NUM_COLS)

def is_valid_column_input(col_input):
    """
    Checks if the user's column input is valid.
    A valid input is a single uppercase letter within the board's column range.
    """
    if len(col_input) != 1 or not col_input.isalpha():
        return False
    
    col_index = get_column_index(col_input)
    return 0 <= col_index < NUM_COLS

def get_player_move():
    """
    Prompts the current player for a column choice and validates the input.
    Returns the valid column index.
    """
    player_checker = CHECKERS[current_player_index]
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").upper()
        
        if not is_valid_column_input(col_input):
            print("Invalid input. Please enter a single letter (e.g., A, B, C) within the board range.")
            continue
        
        col_index = get_column_index(col_input)
        
        if board[0][col_index] != " ": # Check if the top row of the column is occupied
            print("That column is full. Please choose another column.")
            continue
            
        return col_index

def drop_checker(col_index, checker):
    """
    Drops the checker into the lowest available space in the specified column.
    Returns True if the checker was placed, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True
    return False # Should not be reached if get_player_move validates column full

def check_win(checker):
    """
    Checks if the current player (with 'checker') has won the game.
    Checks horizontally, vertically, and diagonally.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw():
    """Checks if the board is completely filled, indicating a draw."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True # No empty spaces found

def main():
    """Main function to run the Connect 4 game."""
    global current_player_index

    initialize_board()
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    game_over = False
    winner_checker = None

    while not game_over:
        print_board()

        current_player_checker = CHECKERS[current_player_index]
        
        col_to_drop = get_player_move()
        
        # Drop checker and update board
        drop_successful = drop_checker(col_to_drop, current_player_checker)

        # After every turn, the board must be checked for a possible win.
        if check_win(current_player_checker):
            winner_checker = current_player_checker
            game_over = True
        elif check_draw():
            game_over = True # It's a draw
        else:
            # Alternate turns
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
    
    # Game end
    print_board() # Print final board
    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main()
