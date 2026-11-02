import os
import random
import sys

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# --- Global Variables ---
board = []
players = []
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
    sys.stdout.write("  ")
    for col_index in range(NUM_COLS):
        sys.stdout.write(f" {chr(ord('A') + col_index)} ")
    sys.stdout.write("\n")

    # Print board rows
    for row_index in range(NUM_ROWS):
        sys.stdout.write("+")
        for _ in range(NUM_COLS):
            sys.stdout.write("---+")
        sys.stdout.write("\n")

        sys.stdout.write("|")
        for col_index in range(NUM_COLS):
            sys.stdout.write(f" {board[row_index][col_index]} |")
        sys.stdout.write("\n")

    # Print bottom border
    sys.stdout.write("+")
    for _ in range(NUM_COLS):
        sys.stdout.write("---+")
    sys.stdout.write("\n")


def get_column_input(prompt):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number if valid, otherwise None.
    """
    while True:
        user_input = input(prompt).strip().upper()

        if not user_input:
            print("Input cannot be empty. Please enter a column letter.")
            continue

        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter for the column (e.g., A).")
            continue

        col_char_code = ord(user_input)
        first_col_char_code = ord('A')
        max_col_char_code = ord('A') + NUM_COLS - 1

        if not (first_col_char_code <= col_char_code <= max_col_char_code):
            print(f"Invalid column. Please enter a letter between A and {chr(max_col_char_code)}.")
            continue

        col_index = col_char_code - first_col_char_code
        return col_index


def drop_checker(col_index, checker):
    """
    Drops the checker into the specified column.
    Returns True if the checker was placed, False if the column is full.
    """
    for row_index in range(NUM_ROWS - 1, -1, -1):
        if board[row_index][col_index] == " ":
            board[row_index][col_index] = checker
            return True
    return False


def check_win(checker):
    """
    Checks if the current player has won the game.
    A player wins if they have WIN_CONDITION checkers in a row horizontally,
    vertically, or diagonally.
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

    # Check positive diagonal (bottom-left to top-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check negative diagonal (top-left to bottom-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    return False


def check_draw():
    """Checks if the board is full, indicating a draw."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Board is not full
    return True  # Board is full


def setup_game():
    """Sets up the game by creating the board and players."""
    global players, current_player_index
    create_board()
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)


def next_turn():
    """Advances to the next player's turn."""
    global current_player_index
    current_player_index = (current_player_index + 1) % NUM_PLAYERS


def main():
    """Main game loop."""
    setup_game()
    game_over = False
    winner = None

    while not game_over:
        print_board()
        current_player_checker = players[current_player_index]
        print(f"Player {current_player_checker}, please enter a column:")

        column_placed = False
        while not column_placed:
            col_input = get_column_input(f"Player {current_player_checker}'s turn: ")
            if col_input is not None:
                if drop_checker(col_input, current_player_checker):
                    column_placed = True
                else:
                    print("That column is full! Please choose another column.")
            else:
                # get_column_input already printed an error
                pass

        # After a valid move, print the board again before checking win/draw
        print_board()

        if check_win(current_player_checker):
            winner = current_player_checker
            game_over = True
            print(f"Player {winner} won!")
        elif check_draw():
            game_over = True
            print("It's a draw!")
        else:
            next_turn()

    print("Game Over!")


if __name__ == "__main__":
    main()
