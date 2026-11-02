import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns for A-Z labels
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_SEQUENCE_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

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
    board = [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board():
    """Prints the current state of the game board."""
    clear_screen()

    # Print column labels (A, B, C, ...)
    print("  " + "   ".join([chr(ord('A') + i) for i in range(NUM_COLS)]))
    for r in range(NUM_ROWS):
        print("+---+" * NUM_COLS + "+")
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---+" * NUM_COLS + "+")

def get_column_input(player_checker):
    """
    Prompts the current player for a column input, validates it,
    and returns the 0-indexed column number.
    """
    while True:
        try:
            col_char = input(f"Player {player_checker}, please enter a column: ").upper()
            if not col_char.isalpha() or len(col_char) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(col_char) - ord('A')

            if not (0 <= col_index < NUM_COLS):
                print(f"Column '{col_char}' is out of board range. Please choose between A and {chr(ord('A') + NUM_COLS - 1)}.")
                continue

            # Check if the column is full
            if board[0][col_index] != " ":
                print(f"Column '{col_char}' is full. Please choose another column.")
                continue

            return col_index
        except Exception:
            print("An unexpected error occurred. Please try again.")

def drop_checker(col_index, player_checker):
    """
    Places the player's checker in the lowest available space
    of the specified column.
    Returns True if the checker was placed, False if the column was full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = player_checker
            return True
    return False # Should not be reached due to validation in get_column_input

def check_win(player_checker):
    """
    Checks if the current player has achieved a win condition
    (4 in a row horizontally, vertically, or diagonally).
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r][c + i] == player_checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check vertical
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r + i][c] == player_checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_SEQUENCE_LENGTH + 1):
        for c in range(NUM_COLS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r + i][c + i] == player_checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check diagonal (top-right to bottom-left)
    for r in range(NUM_ROWS - WIN_SEQUENCE_LENGTH + 1):
        for c in range(WIN_SEQUENCE_LENGTH - 1, NUM_COLS):
            if all(board[r + i][c - i] == player_checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    return False

def check_draw():
    """Checks if the board is completely full, indicating a draw."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False
    return True

def main():
    """Main function to run the Connect 4 game."""
    global current_player_index

    create_board()
    available_checkers = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    game_over = False
    winner_found = False

    while not game_over:
        current_player_checker = available_checkers[current_player_index]
        print_board()

        col_index = get_column_input(current_player_checker)

        # Drop the checker (validation ensures it's a valid move)
        drop_checker(col_index, current_player_checker)

        # Check for win
        if check_win(current_player_checker):
            print_board()
            print(f"Player {current_player_checker} won!")
            winner_found = True
            game_over = True
        # Check for draw
        elif check_draw():
            print_board()
            print("The game is a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
