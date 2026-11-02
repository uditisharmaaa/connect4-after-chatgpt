import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_SEQUENCE_LENGTH = 4

PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
EMPTY_CELL = " "

# --- Board Initialization and Display ---

def create_board(rows, cols):
    """Creates an empty game board with specified dimensions."""
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def get_column_label(col_index):
    """Converts a column index to its corresponding letter label (A, B, C, ...)."""
    return chr(ord('A') + col_index)

def print_board(board):
    """Prints the game board with column labels and appropriate formatting."""
    clear_screen()

    # Print column labels
    print(" ", end="")
    for col in range(len(board[0])):
        print(f" {get_column_label(col)} ", end="")
    print()

    # Print board content
    for row in range(len(board)):
        print("+", end="")
        for _ in range(len(board[0])):
            print("---+", end="")
        print()
        print("|", end="")
        for col in range(len(board[0])):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+", end="")
    for _ in range(len(board[0])):
        print("---+", end="")
    print()

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

# --- Game Logic ---

def get_player_input(current_player_checker, board):
    """
    Prompts the current player for a column input, validates it,
    and returns the 0-indexed column number.
    Handles invalid input gracefully without losing the turn.
    """
    num_cols = len(board[0])
    while True:
        try:
            prompt = f"Player {current_player_checker}, please enter a column: "
            user_input = input(prompt).strip().upper()

            if not user_input:
                print("Invalid input: Column cannot be empty. Please try again.")
                continue

            # Check if input is a single letter
            if len(user_input) != 1 or not 'A' <= user_input <= get_column_label(num_cols - 1):
                print(f"Invalid input: Please enter a single letter from A to {get_column_label(num_cols - 1)}. Please try again.")
                continue

            col_index = ord(user_input) - ord('A')

            # Check if column index is within board bounds
            if not (0 <= col_index < num_cols):
                print(f"Invalid input: Column {user_input} is out of bounds. Please enter a column from A to {get_column_label(num_cols - 1)}. Please try again.")
                continue

            # Check if column is full
            if board[0][col_index] != EMPTY_CELL:
                print(f"Column {user_input} is full. Please choose another column. You do not lose your turn.")
                continue

            return col_index

        except KeyboardInterrupt:
            print("\nGame interrupted by user. Exiting.")
            sys.exit()
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")


def place_checker(board, col_index, checker):
    """
    Places the checker in the lowest available space in the specified column.
    Returns the (row, col) coordinates where the checker was placed, or None if the column is full.
    """
    num_rows = len(board)
    for row in range(num_rows - 1, -1, -1):
        if board[row][col_index] == EMPTY_CELL:
            board[row][col_index] = checker
            return row, col_index
    return None # Column is full, though this should be checked by get_player_input

def check_win(board, last_placed_row, last_placed_col, checker):
    """
    Checks if the last placed checker resulted in a win (4 in a row)
    horizontally, vertically, or diagonally.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Helper function to check a specific direction
    def check_direction(dr, dc):
        count = 0
        # Check in both positive and negative directions from the last placed checker
        for i in range(-WIN_SEQUENCE_LENGTH + 1, WIN_SEQUENCE_LENGTH):
            r, c = last_placed_row + i * dr, last_placed_col + i * dc
            if 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
                count += 1
                if count >= WIN_SEQUENCE_LENGTH:
                    return True
            else:
                count = 0 # Reset count if the sequence is broken
        return False

    # Check horizontal
    if check_direction(0, 1):
        return True
    # Check vertical
    if check_direction(1, 0):
        return True
    # Check diagonal (top-left to bottom-right)
    if check_direction(1, 1):
        return True
    # Check anti-diagonal (top-right to bottom-left)
    if check_direction(1, -1):
        return True

    return False

def check_draw(board):
    """Checks if the board is completely full, indicating a draw."""
    num_rows = len(board)
    num_cols = len(board[0])
    for r in range(num_rows):
        for c in range(num_cols):
            if board[r][c] == EMPTY_CELL:
                return False
    return True

# --- Main Game Function ---

def play_connect_4():
    """Main function to run the Connect 4 game."""
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit()

    if not (1 <= NUM_COLS <= 26):
        print("Error: NUM_COLS must be between 1 and 26 (for A-Z labels).")
        sys.exit()

    if not (WIN_SEQUENCE_LENGTH <= NUM_ROWS and WIN_SEQUENCE_LENGTH <= NUM_COLS):
        print("Error: WIN_SEQUENCE_LENGTH must not exceed NUM_ROWS or NUM_COLS.")
        sys.exit()


    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    winner_found = False

    print_board(board)
    print(f"First player is {players[current_player_index]}!")

    while not game_over:
        current_player_checker = players[current_player_index]

        col_index = get_player_input(current_player_checker, board)
        last_placed_coords = place_checker(board, col_index, current_player_checker)

        if last_placed_coords is None:
            # This case should ideally not be reached due to validation in get_player_input,
            # but as a safeguard, if column is somehow full, just re-ask for input for current player.
            # The assignment specifies "the turn is invalid and the player loses the turn" for full column,
            # but previous sentence says "the player will be asked to provide another input until the input is valid (the turn is not lost)".
            # I will follow the "turn is not lost" for full column as it aligns better with input validation.
            # If "loses the turn" is strictly required, remove the continue and let current_player_index increment.
            print(f"Error placing checker in column {get_column_label(col_index)}. Please try again.")
            continue # Re-ask current player
        
        last_placed_row, last_placed_col = last_placed_coords

        print_board(board) # Print board after every valid move

        if check_win(board, last_placed_row, last_placed_col, current_player_checker):
            print(f"Player {current_player_checker} won!")
            winner_found = True
            game_over = True
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        else:
            # Move to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_connect_4()
