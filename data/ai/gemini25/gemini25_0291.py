import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
COLUMN_LABELS = [chr(ord('A') + i) for i in range(NUM_COLS)]

# --- Global Variables ---
board = []
current_player_index = 0

# --- Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board():
    """Initializes the game board with empty spaces."""
    global board
    board = [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board():
    """Prints the current state of the game board."""
    clear_screen()
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    for r in range(NUM_ROWS):
        # Print top border for each row
        print("+---" * NUM_COLS + "+")
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    # Print bottom border for the last row
    print("+---" * NUM_COLS + "+")

def get_player_input(player_checker):
    """
    Prompts the current player for a column choice and validates the input.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            col_char = input(f"Player {player_checker}, please enter a column: ").strip().upper()
            if not col_char:
                raise ValueError("Input cannot be empty.")
            
            col_index = COLUMN_LABELS.index(col_char)
            
            if not (0 <= col_index < NUM_COLS):
                print("Invalid column. Please enter a letter within the board range.")
            elif board[0][col_index] != " ": # Check if the top row of the column is occupied
                print("Column is full. Please choose another column.")
            else:
                return col_index
        except ValueError:
            print("Invalid input. Please enter a single uppercase letter corresponding to a column (e.g., A, B, C).")
        except IndexError:
            print("Invalid column. Please enter a letter within the board range.")


def drop_checker(col_index, player_checker):
    """
    Drops the player's checker into the specified column.
    Returns True if the checker was successfully placed, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = player_checker
            return True
    return False # Should not be reached if validation in get_player_input is correct

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

    # Check positive diagonal (bottom-left to top-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check negative diagonal (top-left to bottom-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r - i][c + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw():
    """Checks if the board is completely filled (a draw)."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # An empty space found, not a draw yet
    return True # No empty spaces, it's a draw

def main():
    global current_player_index

    create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1) # Randomly select first player

    game_over = False
    while not game_over:
        player_checker = PLAYER_CHECKERS[current_player_index]
        print_board()

        col_index = get_player_input(player_checker)
        
        # Drop checker and only proceed if successful (column not full, which is now handled in get_player_input)
        if drop_checker(col_index, player_checker):
            if check_win(player_checker):
                print_board()
                print(f"Player {player_checker} won!")
                game_over = True
            elif check_draw():
                print_board()
                print("It's a draw!")
                game_over = True
            else:
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        # Else branch is not strictly needed anymore because get_player_input ensures a valid, non-full column.
        # However, if validation was less strict and drop_checker could fail, we would not change player turn here.

if __name__ == "__main__":
    main()
