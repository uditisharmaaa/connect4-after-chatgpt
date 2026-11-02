import os
import random
import sys

# --- GLOBAL CONSTANTS ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_LENGTH = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# --- HELPER FUNCTIONS ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def get_column_label(col_index):
    """Converts a column index to its corresponding letter label (A, B, C...)."""
    return chr(ord('A') + col_index)

def print_board(board):
    """Prints the Connect 4 board to the console."""
    clear_screen()

    # Print column labels
    col_labels = [get_column_label(i) for i in range(NUM_COLS)]
    print("  " + "   ".join(col_labels))

    # Print top border
    print("+---" * NUM_COLS + "+")

    # Print rows with checkers
    for r in range(NUM_ROWS):
        row_str = "|"
        for c in range(NUM_COLS):
            row_str += f" {board[r][c]} |"
        print(row_str)
        print("+---" * NUM_COLS + "+")

def create_board(rows, cols):
    """Creates an empty Connect 4 board initialized with whitespaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def is_valid_column_input(col_input):
    """
    Checks if the user's column input is valid.
    Valid input is a single uppercase letter within the board's column range.
    """
    if len(col_input) != 1:
        return False
    if not 'A' <= col_input <= get_column_label(NUM_COLS - 1):
        return False
    return True

def get_column_index(col_label):
    """Converts a column letter label to its integer index."""
    return ord(col_label) - ord('A')

def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.
    Returns True if successful, False if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):  # Start from bottom row
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True
    return False # Column is full

def check_win(board, checker):
    """
    Checks if the given player's checker has achieved a Connect 4.
    Checks horizontally, vertically, and diagonally.
    """
    # Check horizontal wins
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check vertical wins
    for c in range(NUM_COLS):
        for r in range(NUM_ROWS - WIN_LENGTH + 1):
            if all(board[r + i][c] == checker for i in range(WIN_LENGTH)):
                return True

    # Check positive diagonal wins (bottom-left to top-right)
    for r in range(NUM_ROWS - WIN_LENGTH + 1):
        for c in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check negative diagonal wins (top-left to bottom-right)
    for r in range(WIN_LENGTH - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    return False

def check_draw(board):
    """Checks if the board is completely full, indicating a draw."""
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True  # Board is full

# --- MAIN GAME LOGIC ---

def play_game():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print("Welcome to Connect 4!")
    print(f"Number of players: {NUM_PLAYERS}")
    print(f"Checkers: {', '.join(PLAYER_CHECKERS)}")
    input("Press Enter to start the game...")

    game_over = False
    while not game_over:
        current_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)
        print(f"Player {current_checker}, please enter a column:")

        valid_turn = False
        while not valid_turn:
            try:
                col_input = input().strip().upper()
                
                if not is_valid_column_input(col_input):
                    print("Invalid input. Please enter a single uppercase letter (e.g., A, B, C) corresponding to a column.")
                    continue

                col_index = get_column_index(col_input)

                if not (0 <= col_index < NUM_COLS):
                    print(f"Column '{col_input}' is out of bounds. Please enter a column between A and {get_column_label(NUM_COLS - 1)}.")
                    continue

                if drop_checker(board, col_index, current_checker):
                    valid_turn = True
                else:
                    print(f"Column {col_input} is full. Please choose another column.")
                    # Player loses turn if column is full as per assignment rules
                    # To not lose turn, valid_turn should remain False here,
                    # and the loop should continue for the same player.
                    # The current implementation lets the player lose turn.
                    break # Break from inner loop to advance to next player
            except EOFError:
                print("\nGame interrupted. Exiting.")
                sys.exit()
            except Exception as e:
                print(f"An unexpected error occurred: {e}. Please try again.")

        if not valid_turn: # If the player's column was full, they lost their turn.
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue # Skip win/draw check for this "lost" turn and go to next player

        # Check for win
        if check_win(board, current_checker):
            print_board(board)
            print(f"Player {current_checker} won!")
            game_over = True
            break

        # Check for draw
        if check_draw(board):
            print_board(board)
            print("The board is full. It's a draw!")
            game_over = True
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print("\n--- Game Over ---")

if __name__ == "__main__":
    play_game()
