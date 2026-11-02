import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_SEQUENCE_LENGTH = 4

PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
EMPTY_CELL = " "

# --- Global Variables ---
board = []
current_player_index = 0

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Initializes the game board with empty cells."""
    global board
    board = [[EMPTY_CELL for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board():
    """Prints the current state of the game board."""
    clear_screen()

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col_index in range(NUM_COLS):
        print(f" {chr(ord('A') + col_index)} ", end="")
    print()

    # Print board rows
    for row_index in range(NUM_ROWS):
        print("+", end="")
        for _ in range(NUM_COLS):
            print("---+", end="")
        print()

        print("|", end="")
        for col_index in range(NUM_COLS):
            print(f" {board[row_index][col_index]} |", end="")
        print()

    # Print bottom border
    print("+", end="")
    for _ in range(NUM_COLS):
        print("---+", end="")
    print()

def get_column_input(player_checker):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            column_letter = input(f"Player {player_checker}, please enter a column: ").upper()
            if len(column_letter) != 1:
                print("Invalid input. Please enter a single letter (e.g., A).")
                continue

            col_index = ord(column_letter) - ord('A')

            if not (0 <= col_index < NUM_COLS):
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + NUM_COLS - 1)}.")
                continue

            # Check if the column is full
            if board[0][col_index] != EMPTY_CELL:
                print("That column is full. Please choose another column.")
                continue

            return col_index
        except TypeError: # Should not happen with upper(), but good for robustness
            print("Invalid input. Please enter a letter.")
        except Exception: # Catch any other unexpected errors
            print("An unexpected error occurred. Please try again.")


def drop_checker(col_index, player_checker):
    """
    Places the player's checker in the lowest available row of the given column.
    Returns True if the checker was dropped successfully, False if the column is full.
    """
    for row_index in range(NUM_ROWS - 1, -1, -1):
        if board[row_index][col_index] == EMPTY_CELL:
            board[row_index][col_index] = player_checker
            return True, row_index
    return False, -1 # Column is full (should be caught by get_column_input already)


def check_win(row, col, player_checker):
    """
    Checks if the given player has won by placing their checker at (row, col).
    Checks horizontally, vertically, and both diagonals.
    """
    # Check horizontal
    count = 0
    for c in range(NUM_COLS):
        if board[row][c] == player_checker:
            count += 1
            if count >= WIN_SEQUENCE_LENGTH:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(NUM_ROWS):
        if board[r][col] == player_checker:
            count += 1
            if count >= WIN_SEQUENCE_LENGTH:
                return True
        else:
            count = 0

    # Check diagonal (top-left to bottom-right)
    count = 0
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    while start_row < NUM_ROWS and start_col < NUM_COLS:
        if board[start_row][start_col] == player_checker:
            count += 1
            if count >= WIN_SEQUENCE_LENGTH:
                return True
        else:
            count = 0
        start_row += 1
        start_col += 1

    # Check diagonal (top-right to bottom-left)
    count = 0
    start_row = row - min(row, NUM_COLS - 1 - col)
    start_col = col + min(row, NUM_COLS - 1 - col)
    while start_row < NUM_ROWS and start_col >= 0:
        if board[start_row][start_col] == player_checker:
            count += 1
            if count >= WIN_SEQUENCE_LENGTH:
                return True
        else:
            count = 0
        start_row += 1
        start_col -= 1

    return False

def check_draw():
    """Checks if the board is completely full (a draw)."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == EMPTY_CELL:
                return False  # There's still an empty cell
    return True  # Board is full

# --- Main Game Logic ---

def play_game():
    """Manages the main game loop."""
    global current_player_index

    create_board()

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner_found = False

    while not game_over:
        print_board()
        current_player_checker = PLAYER_CHECKERS[current_player_index]

        col_to_drop = get_column_input(current_player_checker)
        
        # drop_checker returns (True, row_index) or (False, -1)
        # We already validated the column isn't full in get_column_input,
        # so this should always return True
        placed_successfully, actual_row = drop_checker(col_to_drop, current_player_checker)
        
        # Check for win condition
        if check_win(actual_row, col_to_drop, current_player_checker):
            print_board()
            print(f"Player {current_player_checker} won!")
            winner_found = True
            game_over = True
        elif check_draw():
            print_board()
            print("It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
