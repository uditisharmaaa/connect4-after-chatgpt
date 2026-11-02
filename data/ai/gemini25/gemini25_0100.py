import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_SEQUENCE_LENGTH = 4

# Player checkers
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYERS = CHECKERS[:NUM_PLAYERS]

# --- Board Functions ---
def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    """
    Clears the terminal screen.
    """
    os.system('clear' if os.name == 'posix' else 'cls')

def print_board(board):
    """
    Prints the Connect 4 board with column labels.
    """
    clear_screen()

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col_idx in range(NUM_COLS):
        print(f"{chr(ord('A') + col_idx)}   ", end="")
    print()

    # Print board content
    for row_idx in range(NUM_ROWS):
        print("+---+---+---+---+---+---+---+")
        print("|", end="")
        for col_idx in range(NUM_COLS):
            print(f" {board[row_idx][col_idx]} |", end="")
        print()
    print("+---+---+---+---+---+---+---+")

def get_column_input(current_player_checker):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        try:
            col_char = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()

            if not col_char.isalpha() or len(col_char) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(col_char) - ord('A')

            if not (0 <= col_index < NUM_COLS):
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + NUM_COLS - 1)}.")
                continue

            return col_index
        except Exception:
            print("An unexpected error occurred. Please try again.")

def place_checker(board, col_index, player_checker):
    """
    Places the player's checker in the lowest available space of the given column.
    Returns True if successful, False if the column is full.
    """
    for row_idx in range(NUM_ROWS - 1, -1, -1):  # Start from bottom row
        if board[row_idx][col_index] == " ":
            board[row_idx][col_index] = player_checker
            return True
    return False # Column is full

# --- Win Condition Functions ---
def check_win(board, player_checker):
    """
    Checks if the current player has won horizontally, vertically, or diagonally.
    """
    return (check_horizontal_win(board, player_checker) or
            check_vertical_win(board, player_checker) or
            check_diagonal_win(board, player_checker))

def check_horizontal_win(board, player_checker):
    """
    Checks for a horizontal win.
    """
    for row_idx in range(NUM_ROWS):
        for col_idx in range(NUM_COLS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[row_idx][col_idx + i] == player_checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True
    return False

def check_vertical_win(board, player_checker):
    """
    Checks for a vertical win.
    """
    for col_idx in range(NUM_COLS):
        for row_idx in range(NUM_ROWS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[row_idx + i][col_idx] == player_checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True
    return False

def check_diagonal_win(board, player_checker):
    """
    Checks for diagonal wins (both directions).
    """
    # Check diagonals from bottom-left to top-right (positive slope)
    for row_idx in range(NUM_ROWS - WIN_SEQUENCE_LENGTH + 1):
        for col_idx in range(NUM_COLS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[row_idx + i][col_idx + i] == player_checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check diagonals from top-left to bottom-right (negative slope)
    for row_idx in range(WIN_SEQUENCE_LENGTH - 1, NUM_ROWS):
        for col_idx in range(NUM_COLS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[row_idx - i][col_idx + i] == player_checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True
    return False

def check_draw(board):
    """
    Checks if the board is completely filled (draw).
    """
    for row_idx in range(NUM_ROWS):
        for col_idx in range(NUM_COLS):
            if board[row_idx][col_idx] == " ":
                return False  # An empty space found, not a draw
    return True  # Board is full

# --- Game Logic ---
def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Game loop
    while True:
        current_player_checker = PLAYERS[current_player_index]
        print_board(board)
        
        col_index = get_column_input(current_player_checker)

        if not place_checker(board, col_index, current_player_checker):
            print("That column is full. Please choose another column.")
            # Player does not lose turn if column is full
            continue 

        # Check for win
        if check_win(board, current_player_checker):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            break

        # Check for draw
        if check_draw(board):
            print_board(board)
            print("The board is full. It's a draw!")
            break

        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

# --- Main Execution ---
if __name__ == "__main__":
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if not (1 <= NUM_COLS <= 26): # Max 26 for A-Z labels
        print("Error: NUM_COLS must be between 1 and 26.")
        sys.exit(1)
    if not (WIN_SEQUENCE_LENGTH <= min(NUM_ROWS, NUM_COLS)):
        print(f"Error: WIN_SEQUENCE_LENGTH ({WIN_SEQUENCE_LENGTH}) cannot be greater than board dimensions ({NUM_ROWS}x{NUM_COLS}).")
        sys.exit(1)

    play_game()
