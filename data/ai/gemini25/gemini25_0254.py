import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
CHECKERS = ["X", "O", "V", "H", "M"]

# --- Global Variables ---
board = []
player_checkers = []


# --- Board Functions ---
def create_board(rows, cols):
    """Creates an empty game board with the specified dimensions."""
    global board
    board = [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(rows, cols):
    """Prints the current state of the game board."""
    os.system('clear')  # Clear the screen

    # Print column labels
    for col in range(cols):
        print(f"  {chr(ord('A') + col)} ", end="")
    print()

    # Print top border
    print("+", end="")
    for _ in range(cols):
        print("---+", end="")
    print()

    # Print board rows
    for row in range(rows):
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
        print("+", end="")
        for _ in range(cols):
            print("---+", end="")
        print()


# --- Game Logic Functions ---
def get_column_input(prompt, cols):
    """Gets and validates column input from the player."""
    while True:
        try:
            col_char = input(prompt).strip().upper()
            if not col_char:
                print("Input cannot be empty. Please try again.")
                continue
            col_index = ord(col_char) - ord('A')

            if 0 <= col_index < cols:
                return col_index
            else:
                print(f"Invalid column '{col_char}'. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")
        except TypeError:
            print("Invalid input. Please enter a letter.")
        except Exception:
            print("An unexpected error occurred. Please try again.")


def place_checker(col_index, current_player_checker, rows, cols):
    """Places the checker in the lowest available space in the chosen column."""
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = current_player_checker
            return True, row, col_index  # Return True if placement was successful, and the coordinates
    return False, -1, -1  # Return False if column is full


def check_win(last_row, last_col, player_checker, rows, cols, win_condition):
    """Checks if the last placed checker resulted in a win."""

    # Check horizontal
    count = 0
    for col in range(cols):
        if board[last_row][col] == player_checker:
            count += 1
            if count >= win_condition:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for row in range(rows):
        if board[row][last_col] == player_checker:
            count += 1
            if count >= win_condition:
                return True
        else:
            count = 0

    # Check diagonal (top-left to bottom-right)
    for r_start in range(rows - win_condition + 1):
        for c_start in range(cols - win_condition + 1):
            count = 0
            for i in range(win_condition):
                if board[r_start + i][c_start + i] == player_checker:
                    count += 1
            if count >= win_condition:
                return True

    # Check diagonal (bottom-left to top-right)
    for r_start in range(win_condition - 1, rows):
        for c_start in range(cols - win_condition + 1):
            count = 0
            for i in range(win_condition):
                if board[r_start - i][c_start + i] == player_checker:
                    count += 1
            if count >= win_condition:
                return True

    return False


def check_draw(rows, cols):
    """Checks if the board is completely filled (a draw)."""
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == " ":
                return False  # An empty space found, not a draw yet
    return True  # No empty spaces, it's a draw


# --- Main Game Loop ---
def main():
    global player_checkers

    # Initialize player checkers based on NUM_PLAYERS
    player_checkers = CHECKERS[:NUM_PLAYERS]

    create_board(NUM_ROWS, NUM_COLS)

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    while not game_over:
        current_player_checker = player_checkers[current_player_index]
        print_board(NUM_ROWS, NUM_COLS)

        print(f"Player {current_player_checker}, please enter a column:")
        
        valid_turn = False
        last_placed_row = -1
        last_placed_col = -1

        while not valid_turn:
            col_to_place = get_column_input(f"Your turn ({current_player_checker}): ", NUM_COLS)
            
            placement_successful, last_placed_row, last_placed_col = place_checker(
                col_to_place, current_player_checker, NUM_ROWS, NUM_COLS
            )

            if placement_successful:
                valid_turn = True
            else:
                print("Column is full. Please choose another column.")
                # The turn is not lost, player is asked for another input

        if check_win(last_placed_row, last_placed_col, current_player_checker, NUM_ROWS, NUM_COLS, WIN_CONDITION):
            print_board(NUM_ROWS, NUM_COLS)
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(NUM_ROWS, NUM_COLS):
            print_board(NUM_ROWS, NUM_COLS)
            print("It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
