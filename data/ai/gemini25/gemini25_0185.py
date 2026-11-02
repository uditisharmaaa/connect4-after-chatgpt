import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

# --- Global Variables (initialized later) ---
board = []
players_checkers = []


# --- Functions ---

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
    col_labels = [chr(ord('A') + i) for i in range(NUM_COLS)]
    print("  " + "   ".join(col_labels))

    # Print board rows
    for r in range(NUM_ROWS):
        print("+---+" * NUM_COLS + "+")
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---+" * NUM_COLS + "+")


def get_column_input(current_player_checker):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number if valid.
    """
    while True:
        try:
            user_input = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if not user_input.isalpha() or len(user_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B).")
                continue

            col_index = ord(user_input) - ord('A')

            if not (0 <= col_index < NUM_COLS):
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + NUM_COLS - 1)}.")
                continue

            # Check if the column is full
            if board[0][col_index] != " ":  # Check the topmost row
                print("Column is full. Please choose another column.")
                continue

            return col_index

        except ValueError:
            print("Invalid input. Please enter a valid column letter.")


def place_checker(col_index, current_player_checker):
    """
    Places the current player's checker in the lowest available space
    of the specified column. Returns the row where the checker was placed.
    """
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = current_player_checker
            return r
    return -1  # Should not happen if column full check is done beforehand


def check_win(last_row, last_col, checker):
    """
    Checks if the last placed checker resulted in a win.
    Checks horizontally, vertically, and diagonally.
    """

    # Check horizontal
    count = 0
    for c in range(NUM_COLS):
        if board[last_row][c] == checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(NUM_ROWS):
        if board[r][last_col] == checker:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0

    # Check diagonal (top-left to bottom-right)
    # Start from the 'anchor' position that is WIN_LENGTH-1 steps up-left from (last_row, last_col)
    # and iterate down-right
    for start_row in range(max(0, last_row - WIN_LENGTH + 1), min(NUM_ROWS - WIN_LENGTH + 1, last_row + 1)):
        for start_col in range(max(0, last_col - WIN_LENGTH + 1), min(NUM_COLS - WIN_LENGTH + 1, last_col + 1)):
            count = 0
            for i in range(WIN_LENGTH):
                if (start_row + i < NUM_ROWS and
                        start_col + i < NUM_COLS and
                        board[start_row + i][start_col + i] == checker):
                    count += 1
                else:
                    count = 0 # reset if a non-matching checker is found in the sequence
                    break # break from this inner loop and try next diagonal starting position
            if count >= WIN_LENGTH:
                return True


    # Check diagonal (bottom-left to top-right)
    # Start from the 'anchor' position that is WIN_LENGTH-1 steps down-left from (last_row, last_col)
    # and iterate up-right
    for start_row in range(max(WIN_LENGTH - 1, last_row - WIN_LENGTH + 1), min(NUM_ROWS, last_row + 1)):
        for start_col in range(max(0, last_col - WIN_LENGTH + 1), min(NUM_COLS - WIN_LENGTH + 1, last_col + 1)):
            count = 0
            for i in range(WIN_LENGTH):
                if (start_row - i >= 0 and
                        start_col + i < NUM_COLS and
                        board[start_row - i][start_col + i] == checker):
                    count += 1
                else:
                    count = 0 # reset if a non-matching checker is found in the sequence
                    break # break from this inner loop and try next diagonal starting position
            if count >= WIN_LENGTH:
                return True

    return False


def check_draw():
    """Checks if the board is full (a draw)."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # An empty space found, not a draw
    return True  # Board is full


def main():
    """Main function to run the Connect 4 game."""
    global players_checkers

    # Initialization
    players_checkers = CHECKERS[:NUM_PLAYERS]
    create_board()

    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    while not game_over:
        current_player_checker = players_checkers[current_player_index]
        print_board()

        col_index = get_column_input(current_player_checker)
        last_row = place_checker(col_index, current_player_checker)

        if check_win(last_row, col_index, current_player_checker):
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
