import os
import random
import string

# --- Constants (Can be changed for different game setups) ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Between 2 and 5 players
CHECKERS = ["X", "O", "V", "H", "M"]

# --- Global Variables ---
board = []
current_player_index = 0
players_checkers = CHECKERS[:NUM_PLAYERS]


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
    print("  ", end="")
    for i in range(NUM_COLS):
        print(f"{string.ascii_uppercase[i]:^3}", end="")
    print()

    # Print board content
    for r in range(NUM_ROWS):
        print("+---+" * NUM_COLS + "+")
        print("|", end="")
        for c in range(NUM_COLS):
            print(f" {board[r][c]} |", end="")
        print()
    print("+---+" * NUM_COLS + "+")


def get_column_input(player_checker):
    """
    Prompts the current player for a column input and validates it.
    Returns the valid column index (0-based).
    """
    while True:
        try:
            column_letter = input(f"Player {player_checker}, please enter a column: ").upper()
            if len(column_letter) != 1 or not column_letter.isalpha():
                print("Invalid input. Please enter a single letter (e.g., A).")
                continue

            col_index = ord(column_letter) - ord('A')

            if 0 <= col_index < NUM_COLS:
                # Check if the column is full
                if board[0][col_index] != " ":
                    print("That column is full. Please choose another column.")
                else:
                    return col_index
            else:
                print(f"Invalid column. Please enter a letter between A and {string.ascii_uppercase[NUM_COLS - 1]}.")
        except ValueError:
            print("Invalid input. Please enter a single letter (e.g., A).")


def drop_checker(col_index, player_checker):
    """
    Drops the player's checker into the specified column.
    Returns True if the checker was placed, False if the column was full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Start from bottom row
        if board[r][col_index] == " ":
            board[r][col_index] = player_checker
            return True
    return False  # Should not be reached if validation in get_column_input is correct


def check_win(player_checker):
    """
    Checks if the current player has won the game.
    Checks horizontally, vertically, and diagonally.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - 3):
            if all(board[r][c + i] == player_checker for i in range(4)):
                return True

    # Check vertical
    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLS):
            if all(board[r + i][c] == player_checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLS - 3):
            if all(board[r + i][c + i] == player_checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(3, NUM_ROWS):
        for c in range(NUM_COLS - 3):
            if all(board[r - i][c + i] == player_checker for i in range(4)):
                return True

    return False


def check_draw():
    """Checks if the board is completely filled (a draw)."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # There's an empty space, so not a draw yet
    return True


def next_player_turn():
    """Switches to the next player's turn."""
    global current_player_index
    current_player_index = (current_player_index + 1) % NUM_PLAYERS


# --- Main Game Logic ---
def play_game():
    """Manages the main game loop."""
    global current_player_index

    create_board()

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    winner_found = False
    game_draw = False

    while not winner_found and not game_draw:
        print_board()
        current_player_checker = players_checkers[current_player_index]

        col_index = get_column_input(current_player_checker)

        # Drop the checker (already validated that column isn't full)
        drop_checker(col_index, current_player_checker)

        # Check for win
        if check_win(current_player_checker):
            print_board()  # Print final board with winning move
            print(f"Player {current_player_checker} won!")
            winner_found = True
        elif check_draw():
            print_board()  # Print final board
            print("The game is a draw!")
            game_draw = True
        else:
            next_player_turn()

    print("Game Over!")


if __name__ == "__main__":
    play_game()
