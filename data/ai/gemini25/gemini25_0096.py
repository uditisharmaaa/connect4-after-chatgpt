import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_SEQUENCE_LENGTH = 4

PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
EMPTY_CELL = " "

# --- Utility Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def create_board():
    """
    Creates an empty Connect 4 board of NUM_ROWS x NUM_COLS dimensions.
    Each cell is initialized with EMPTY_CELL.
    """
    return [[EMPTY_CELL for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """
    Prints the Connect 4 board to the console, including column labels.
    Example:
      A   B   C   D   E   F   G
    +---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |
    ...
    """
    clear_screen()

    # Print column labels
    col_labels = [chr(ord('A') + i) for i in range(NUM_COLS)]
    print("  " + "   ".join(col_labels))

    # Print board
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * NUM_COLS + "+")

def get_column_input(current_player_checker):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    Keeps asking until a valid input is provided.
    """
    while True:
        try:
            prompt = f"Player {current_player_checker}, please enter a column: "
            user_input = input(prompt).strip().upper()

            if not user_input:
                print("Input cannot be empty. Please enter a column letter.")
                continue

            if len(user_input) != 1:
                print("Invalid input. Please enter a single column letter (e.g., A, B).")
                continue

            col_char = user_input[0]
            col_index = ord(col_char) - ord('A')

            if not (0 <= col_index < NUM_COLS):
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + NUM_COLS - 1)}.")
                continue

            return col_index
        except KeyboardInterrupt:
            print("\nGame interrupted by user. Exiting.")
            sys.exit(0)
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")

def drop_checker(board, col_index, checker):
    """
    Drops the checker into the specified column.
    Returns True if the checker was placed successfully, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Iterate from bottom row upwards
        if board[r][col_index] == EMPTY_CELL:
            board[r][col_index] = checker
            return True
    return False  # Column is full

def check_win(board, checker):
    """
    Checks if the given checker has won the game by forming a sequence
    of WIN_SEQUENCE_LENGTH horizontally, vertically, or diagonally.
    """

    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check vertical
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r + i][c] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(NUM_ROWS - WIN_SEQUENCE_LENGTH + 1):
        for c in range(NUM_COLS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(WIN_SEQUENCE_LENGTH - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_SEQUENCE_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_SEQUENCE_LENGTH)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == EMPTY_CELL:
                return False  # Found an empty cell, not a draw yet
    return True  # No empty cells found, it's a draw

# --- Main Game Logic ---

def play_game():
    """
    Main function to run the Connect 4 game.
    Initializes the board, handles turns, checks for wins/draws.
    """
    board = create_board()
    player_turn_index = random.randrange(NUM_PLAYERS) # Randomly select first player
    game_over = False
    
    # Pre-game setup output
    print("Welcome to Connect 4!")
    print(f"Board dimensions: {NUM_ROWS} rows x {NUM_COLS} columns")
    print(f"Number of players: {NUM_PLAYERS}")
    print(f"Player checkers: {PLAYER_CHECKERS}")
    print(f"First player will be: Player {PLAYER_CHECKERS[player_turn_index]}")
    input("Press Enter to start the game...")

    while not game_over:
        current_player_checker = PLAYER_CHECKERS[player_turn_index]
        print_board(board)

        col_index = get_column_input(current_player_checker)

        if drop_checker(board, col_index, current_player_checker):
            # Checker was placed successfully, now check for win or draw
            if check_win(board, current_player_checker):
                print_board(board)
                print(f"Player {current_player_checker} won!")
                game_over = True
            elif check_draw(board):
                print_board(board)
                print("It's a draw! The board is full.")
                game_over = True
            else:
                # Game continues, switch to next player
                player_turn_index = (player_turn_index + 1) % NUM_PLAYERS
        else:
            # Column was full, inform the player and let them try again (turn not lost)
            print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
            input("Press Enter to continue...") # Pause to let user read message


if __name__ == "__main__":
    play_game()
