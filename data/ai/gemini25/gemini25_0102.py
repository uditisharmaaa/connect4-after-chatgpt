import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5 players
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_LENGTH = 4

# --- Global Variables ---
board = []
current_player_index = 0

# --- Helper Functions ---
def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Initializes the game board with empty spaces."""
    global board
    board = [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board():
    """Prints the current state of the game board."""
    clear_screen()

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col in range(NUM_COLS):
        print(f" {chr(ord('A') + col)} ", end="")
    print()

    # Print the board with separators
    for row in range(NUM_ROWS):
        print("+", end="")
        for col in range(NUM_COLS):
            print("---+", end="")
        print()
        print("|", end="")
        for col in range(NUM_COLS):
            print(f" {board[row][col]} |", end="")
        print()
    print("+", end="")
    for col in range(NUM_COLS):
        print("---+", end="")
    print()

def get_column_input(player_checker):
    """
    Prompts the current player for a column input and validates it.
    Returns the valid column index (0-based).
    """
    while True:
        try:
            col_char = input(f"Player {player_checker}, please enter a column: ").upper()
            if len(col_char) != 1 or not ('A' <= col_char <= chr(ord('A') + NUM_COLS - 1)):
                print(f"Invalid input. Please enter a single letter from A to {chr(ord('A') + NUM_COLS - 1)}.")
                continue

            col_index = ord(col_char) - ord('A')
            return col_index
        except Exception:
            print("Invalid input. Please enter a single letter.")

def place_checker(col_index, player_checker):
    """
    Places the player's checker in the lowest available space in the given column.
    Returns True if the checker was placed successfully, False if the column is full.
    """
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = player_checker
            return True
    return False

def check_win(player_checker):
    """
    Checks if the current player has won the game.
    Checks horizontally, vertically, and diagonally.
    """
    # Check horizontal
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True

    # Check vertical
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == player_checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(NUM_ROWS - WIN_LENGTH + 1):
        for col in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, NUM_ROWS):
        for col in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[row - i][col + i] == player_checker for i in range(WIN_LENGTH)):
                return True

    return False

def check_draw():
    """
    Checks if the board is full, indicating a draw.
    """
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if board[row][col] == ' ':
                return False  # Board is not full
    return True  # Board is full

# --- Main Game Logic ---
def play_game():
    """Manages the main Connect 4 game flow."""
    global current_player_index

    create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    game_over = False
    while not game_over:
        current_player_checker = CHECKERS[current_player_index]
        print_board()

        column_filled = True
        valid_column_index = -1
        while column_filled:
            valid_column_index = get_column_input(current_player_checker)
            column_filled = not place_checker(valid_column_index, current_player_checker)
            if column_filled:
                print(f"Column {chr(ord('A') + valid_column_index)} is full. Please choose another column.")
                # Player does not lose turn for choosing a full column

        # After placing a checker, print the board again to show the change
        print_board()

        if check_win(current_player_checker):
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw():
            print("It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
