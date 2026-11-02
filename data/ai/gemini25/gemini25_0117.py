import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns for A-Z labels
NUM_PLAYERS = 2
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
WIN_CONDITION = 4  # Number of checkers in a row to win

# --- Global Variables ---
board = []


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

    # Print column labels
    col_labels = [chr(ord('A') + i) for i in range(NUM_COLS)]
    print("  " + "   ".join(col_labels))

    # Print board rows
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * NUM_COLS + "+")


def get_column_input(player_checker):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").upper()

        if not col_input:
            print("Invalid input. Please enter a column letter (A-{}).".format(chr(ord('A') + NUM_COLS - 1)))
            continue

        if len(col_input) != 1 or not 'A' <= col_input <= chr(ord('A') + NUM_COLS - 1):
            print("Invalid input. Please enter a single column letter (A-{}).".format(chr(ord('A') + NUM_COLS - 1)))
            continue

        col_index = ord(col_input) - ord('A')

        if not (0 <= col_index < NUM_COLS):
            print("Column out of bounds. Please choose a column between A and {}.".format(chr(ord('A') + NUM_COLS - 1)))
            continue

        if board[0][col_index] != ' ':  # Check if the top row of the column is full
            print("Column {} is full. Please choose another column.".format(col_input))
            continue

        return col_index


def drop_checker(col_index, player_checker):
    """
    Drops the player's checker into the specified column.
    Returns True if the checker was successfully placed, False if the column was full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col_index] == ' ':
            board[r][col_index] = player_checker
            return True
    return False


def check_win(player_checker):
    """
    Checks if the current player has won the game.
    Checks horizontally, vertically, and diagonally.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - WIN_CONDITION + 1):
            if all(board[r + i][c] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    return False


def check_draw():
    """Checks if the board is completely full, indicating a draw."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == ' ':
                return False  # An empty space is found, so it's not a draw yet
    return True


def play_game():
    """Main function to run the Connect 4 game."""
    create_board()

    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        player_checker = PLAYER_CHECKERS[current_player_index]
        print_board()
        
        col_index = get_column_input(player_checker)
        
        # Drop checker, re-prompt if column was full (though get_column_input already handles this for us)
        # This redundant check is kept for robustness, although the current get_column_input design
        # should prevent it from ever being False here.
        if not drop_checker(col_index, player_checker): 
            continue # Should not be reached with current get_column_input logic


        if check_win(player_checker):
            print_board()
            print(f"Player {player_checker} won!")
            break
        elif check_draw():
            print_board()
            print("The board is full. It's a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
