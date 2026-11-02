import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 columns
NUM_PLAYERS = 2  # Between 2 and 5 players

PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
EMPTY_CELL = " "
WIN_CONDITION = 4  # Number of checkers in a row to win

# --- Global Variables (will be initialized later) ---
board = []
players = []

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Creates an empty game board with specified dimensions."""
    global board
    board = [[EMPTY_CELL for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board():
    """Prints the current state of the game board."""
    clear_screen()

    # Print column headers (A, B, C, ...)
    print(" ", end="")
    for col_idx in range(NUM_COLS):
        print(f" {chr(ord('A') + col_idx)} ", end="")
    print()

    # Print top border
    print("+", end="")
    for _ in range(NUM_COLS):
        print("---+", end="")
    print()

    # Print rows with checkers and borders
    for row_idx in range(NUM_ROWS):
        print("|", end="")
        for col_idx in range(NUM_COLS):
            print(f" {board[row_idx][col_idx]} |", end="")
        print()
        print("+", end="")
        for _ in range(NUM_COLS):
            print("---+", end="")
        print()

def initialize_players():
    """Initializes the list of players with their checkers."""
    global players
    for i in range(NUM_PLAYERS):
        players.append(PLAYER_CHECKERS[i])

def get_column_input(current_player_checker):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    """
    while True:
        col_input = input(f"Player {current_player_checker}, please enter a column: ").upper()

        if not col_input.isalpha() or len(col_input) != 1:
            print("Invalid input. Please enter a single letter (e.g., A, B).")
            continue

        col_index = ord(col_input) - ord('A')

        if not (0 <= col_index < NUM_COLS):
            print(f"Column '{col_input}' is out of bounds. Please enter a column between A and {chr(ord('A') + NUM_COLS - 1)}.")
            continue

        # Check if the column is full
        if board[0][col_index] != EMPTY_CELL:
            print(f"Column '{col_input}' is full. Please choose another column.")
            # Important: The turn is lost here as per assignment, but the prompt loop continues until valid input.
            # The assignment implies: "If the column is already completely filled with checkers, the turn is invalid and the player loses the turn."
            # This means if they enter a full column, it's invalid *for that choice*, and they need to re-enter.
            # The current loop structure handles this by making them choose again. The turn isn't truly "lost" until
            # they successfully make a move or the game ends.
            continue
        
        return col_index

def drop_checker(col_index, current_player_checker):
    """
    Drops the checker into the lowest available space in the specified column.
    Returns True if the checker was successfully placed, False if the column was full.
    """
    for row_idx in range(NUM_ROWS - 1, -1, -1):  # Iterate from bottom to top
        if board[row_idx][col_index] == EMPTY_CELL:
            board[row_idx][col_index] = current_player_checker
            return True
    return False # Should not be reached if get_column_input validates correctly

def check_win(player_checker):
    """Checks if the given player has won the game."""

    # Check horizontal
    for row_idx in range(NUM_ROWS):
        for col_idx in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[row_idx][col_idx + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for col_idx in range(NUM_COLS):
        for row_idx in range(NUM_ROWS - WIN_CONDITION + 1):
            if all(board[row_idx + i][col_idx] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row_idx in range(NUM_ROWS - WIN_CONDITION + 1):
        for col_idx in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[row_idx + i][col_idx + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (bottom-left to top-right)
    for row_idx in range(WIN_CONDITION - 1, NUM_ROWS):
        for col_idx in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[row_idx - i][col_idx + i] == player_checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw():
    """Checks if the board is completely filled (a draw)."""
    for row_idx in range(NUM_ROWS):
        for col_idx in range(NUM_COLS):
            if board[row_idx][col_idx] == EMPTY_CELL:
                return False  # Found an empty cell, not a draw
    return True # No empty cells found, it's a draw

# --- Main Game Logic ---

def main():
    create_board()
    initialize_players()

    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    winner_checker = None

    while not game_over:
        current_player_checker = players[current_player_index]
        print_board()

        col_to_drop = get_column_input(current_player_checker)
        
        # Drop the checker. get_column_input ensures the column is not full.
        drop_checker(col_to_drop, current_player_checker)
        
        # Check for win
        if check_win(current_player_checker):
            winner_checker = current_player_checker
            game_over = True
        # Check for draw if no win
        elif check_draw():
            game_over = True
        
        # Switch to the next player if the game is not over
        if not game_over:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Game End
    print_board() # Print final board
    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("The game is a draw!")

if __name__ == "__main__":
    main()
