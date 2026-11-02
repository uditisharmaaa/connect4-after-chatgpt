import os
import random
import string

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# --- Global Variables ---
board = []
players = []


def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')


def create_board():
    """Initializes the game board with empty spaces."""
    global board
    board = [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]


def create_players():
    """Initializes the list of players with their checkers."""
    global players
    players = PLAYER_CHECKERS[:NUM_PLAYERS]


def print_board():
    """Prints the current state of the game board."""
    clear_screen()

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col in range(NUM_COLS):
        print(f"{string.ascii_uppercase[col]:^3}", end="")
    print()

    # Print board rows
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        print("|", end="")
        for c in range(NUM_COLS):
            print(f" {board[r][c]} |", end="")
        print()
    print("+---" * NUM_COLS + "+")


def get_column_input(current_player_checker):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            col_char = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if len(col_char) != 1 or not 'A' <= col_char <= string.ascii_uppercase[NUM_COLS - 1]:
                raise ValueError("Invalid column. Please enter a single letter between A and "
                                 f"{string.ascii_uppercase[NUM_COLS - 1]}.")

            col_index = ord(col_char) - ord('A')
            return col_index
        except ValueError as e:
            print(f"Error: {e}")


def place_checker(col_index, current_player_checker):
    """
    Places the current player's checker in the specified column.
    Returns True if successful, False if the column is full.
    """
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = current_player_checker
            return True
    return False  # Column is full


def check_win(current_player_checker):
    """Checks if the current player has won the game."""

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
    """Checks if the board is full, indicating a draw."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == ' ':
                return False  # Board is not full
    return True  # Board is full


def main():
    """Main function to run the Connect 4 game."""
    create_board()
    create_players()

    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    while not game_over:
        current_player_checker = players[current_player_index]
        print_board()

        column_placed = False
        while not column_placed:
            col_index = get_column_input(current_player_checker)
            if place_checker(col_index, current_player_checker):
                column_placed = True
            else:
                print(f"Column {string.ascii_uppercase[col_index]} is full. Please choose another column.")
                # Player does not lose turn

        if check_win(current_player_checker):
            print_board()
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw():
            print_board()
            print("It's a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
