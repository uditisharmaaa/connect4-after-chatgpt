import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5 players
CHECKERS = ["X", "O", "V", "H", "M"]

# --- Global Variables ---
board = []
current_player_index = 0
player_checkers = []

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Creates a new game board initialized with whitespaces."""
    global board
    board = [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board():
    """Prints the Connect 4 board to the console."""
    clear_screen()

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for i in range(NUM_COLS):
        print(f" {chr(ord('A') + i)} ", end="")
    print()

    # Print board rows
    for r in range(NUM_ROWS):
        print("+", end="")
        for _ in range(NUM_COLS):
            print("---+", end="")
        print()

        print("|", end="")
        for c in range(NUM_COLS):
            print(f" {board[r][c]} |", end="")
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
            col_char = input(f"Player {player_checker}, please enter a column: ").upper()
            if len(col_char) != 1 or not ('A' <= col_char <= chr(ord('A') + NUM_COLS - 1)):
                raise ValueError("Invalid column. Please enter a single letter (A-" + chr(ord('A') + NUM_COLS - 1) + ").")

            col = ord(col_char) - ord('A')
            return col
        except ValueError as e:
            print(f"Error: {e}")

def place_checker(col, checker):
    """
    Places the checker in the lowest available row of the specified column.
    Returns True if successful, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Start from bottom row
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False # Column is full

def check_win(checker):
    """
    Checks if the given checker has formed a Connect 4 horizontally, vertically, or diagonally.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(3, NUM_ROWS):
        for c in range(NUM_COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def check_draw():
    """
    Checks if the board is completely filled (game is a draw).
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # An empty space is found, not a draw
    return True  # No empty spaces, it's a draw

def setup_game():
    """Initializes game settings and variables."""
    global player_checkers, current_player_index

    # Initialize player checkers based on NUM_PLAYERS
    player_checkers = CHECKERS[:NUM_PLAYERS]

    create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1) # Randomly choose first player

# --- Main Game Loop ---

def play_game():
    """Manages the main Connect 4 game flow."""
    global current_player_index

    setup_game()

    game_over = False
    while not game_over:
        print_board()

        current_checker = player_checkers[current_player_index]
        print(f"It's Player {current_checker}'s turn.")

        col = get_column_input(current_checker)

        if place_checker(col, current_checker):
            if check_win(current_checker):
                print_board()
                print(f"Player {current_checker} won!")
                game_over = True
            elif check_draw():
                print_board()
                print("It's a draw!")
                game_over = True
            else:
                # Next player's turn
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            print(f"Column {chr(ord('A') + col)} is full. Player {current_checker}, you lose your turn.")
            # The assignment states "the turn is not lost", but also "the turn is invalid and the player loses the turn"
            # The latter interpretation is implemented here. If the former is intended, remove the `else` block
            # and just re-ask for input for the same player.
            # For now, sticking to the "player loses the turn" for a full column.
            # If "turn is not lost" for full column is required, change this:
            # print("Column is full. Please choose another column.")
            # continue # This would make the player retry
            current_player_index = (current_player_index + 1) % NUM_PLAYERS # Move to next player if turn is lost


# --- Run the game ---
if __name__ == "__main__":
    play_game()
