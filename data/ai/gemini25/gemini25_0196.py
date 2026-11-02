import os
import random
import sys

# --- Global Constants ---
NUM_COLUMNS = 7  # Maximum 26 columns (A-Z)
NUM_ROWS = 6
NUM_PLAYERS = 2  # Between 2 and 5 players

# Checkers for players
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYER_CHECKERS = CHECKERS[:NUM_PLAYERS]

# Column labels (A, B, C, ...)
COLUMN_LABELS = [chr(ord('A') + i) for i in range(NUM_COLUMNS)]

# --- Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows on the board.
        cols (int): The number of columns on the board.

    Returns:
        list: A 2D list representing the game board, initialized with spaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()

    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))

    # Print top border
    print("+---" * NUM_COLUMNS + "+")

    # Print rows
    for r in range(NUM_ROWS):
        row_str = "|"
        for c in range(NUM_COLUMNS):
            row_str += f" {board[r][c]} |"
        print(row_str)
        print("+---" * NUM_COLUMNS + "+")

def get_player_input(player_name, checker):
    """
    Prompts the current player for a column input and validates it.

    Args:
        player_name (str): The name of the current player (e.g., "Player X").
        checker (str): The checker symbol for the current player.

    Returns:
        int: The 0-based index of the chosen column.
    """
    while True:
        try:
            user_input = input(f"{player_name}, please enter a column: ").upper()
            if len(user_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            column_char = user_input[0]
            if column_char not in COLUMN_LABELS:
                print(f"Invalid column '{column_char}'. Please choose a column from {COLUMN_LABELS[0]} to {COLUMN_LABELS[-1]}.")
                continue

            return COLUMN_LABELS.index(column_char)
        except KeyboardInterrupt:
            print("\nGame ended by player. Goodbye!")
            sys.exit()
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")


def place_checker(board, col_index, checker):
    """
    Places a checker in the lowest available space in the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-based index of the column.
        checker (str): The checker symbol to place.

    Returns:
        bool: True if the checker was placed successfully, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Start from bottom row
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """
    Checks if the given checker has achieved 4 in a row (horizontally, vertically, or diagonally).

    Args:
        board (list): The 2D list representing the game board.
        checker (str): The checker symbol to check for a win.

    Returns:
        bool: True if the checker has won, False otherwise.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLUMNS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLUMNS):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - 3):
        for c in range(NUM_COLUMNS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(3, NUM_ROWS):
        for c in range(NUM_COLUMNS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely filled, resulting in a draw.

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLUMNS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True  # No empty spaces found, it's a draw

def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLUMNS)

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Initialize player names for output
    player_names = [f"Player {checker}" for checker in PLAYER_CHECKERS]

    game_over = False

    while not game_over:
        current_checker = PLAYER_CHECKERS[current_player_index]
        current_player_name = player_names[current_player_index]

        print_board(board)
        print(f"{current_player_name}, please enter a column:")

        col_index = get_player_input(current_player_name, current_checker)

        if place_checker(board, col_index, current_checker):
            # Checker was placed successfully
            if check_win(board, current_checker):
                print_board(board)
                print(f"{current_player_name} won!")
                game_over = True
            elif check_draw(board):
                print_board(board)
                print("It's a draw!")
                game_over = True
            else:
                # Switch to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            # Column was full, current player doesn't lose turn, just re-prompts
            print("That column is full! Please choose another column.")
            # Do not change current_player_index, the same player tries again

    print("\nGame Over!")

if __name__ == "__main__":
    main()
