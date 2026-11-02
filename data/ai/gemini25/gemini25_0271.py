import os
import random
import sys

# --- Global Constants (for easy modification as per assignment) ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission as required
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
WIN_CONDITION = 4  # Number of checkers in a row to win

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """
    Creates and returns an empty Connect 4 board.
    The board is a list of lists, initialized with whitespaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the Connect 4 board with column labels.
    """
    clear_screen()

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col_idx in range(NUM_COLS):
        print(f"{chr(ord('A') + col_idx):>2} ", end="")
    print()

    # Print the board with separators
    for row_idx in range(NUM_ROWS):
        print("+", end="")
        for _ in range(NUM_COLS):
            print("---+", end="")
        print()
        print("|", end="")
        for col_idx in range(NUM_COLS):
            print(f" {board[row_idx][col_idx]} |", end="")
        print()
    print("+", end="")
    for _ in range(NUM_COLS):
        print("---+", end="")
    print()

def get_column_input(current_player_checker):
    """
    Prompts the current player for a column input and validates it.
    Returns the 0-indexed column number.
    Keeps asking until a valid input is received.
    """
    while True:
        try:
            user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()

            if not user_input.isalpha() or len(user_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_char = user_input[0]
            col_index = ord(col_char) - ord('A')

            if not (0 <= col_index < NUM_COLS):
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + NUM_COLS - 1)}.")
                continue

            return col_index
        except Exception:
            print("An unexpected error occurred. Please try again.")

def drop_checker(board, col_index, checker):
    """
    Places the checker in the lowest available space of the given column.
    Returns True if the checker was placed successfully, False if the column is full.
    """
    for row_idx in range(NUM_ROWS - 1, -1, -1):
        if board[row_idx][col_index] == " ":
            board[row_idx][col_index] = checker
            return True
    return False # Column is full

def check_win(board, checker):
    """
    Checks if the given player (checker) has won the game.
    Checks horizontally, vertically, and diagonally.
    """
    # Check horizontal
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r][c+i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS):
            if all(board[r+i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check positive diagonal (bottom-left to top-right)
    for r in range(NUM_ROWS - WIN_CONDITION + 1):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r+i][c+i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check negative diagonal (top-left to bottom-right)
    for r in range(WIN_CONDITION - 1, NUM_ROWS):
        for c in range(NUM_COLS - WIN_CONDITION + 1):
            if all(board[r-i][c+i] == checker for i in range(WIN_CONDITION)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True  # Board is full

# --- Main Game Logic ---

def main():
    """
    Main function to run the Connect 4 game.
    """
    # 1. Initialization
    board = create_board(NUM_ROWS, NUM_COLS)
    
    # Select checkers based on NUM_PLAYERS
    current_players_checkers = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    game_over = False
    
    # 2. Game Phase
    while not game_over:
        current_player_checker = current_players_checkers[current_player_index]
        
        print_board(board)
        
        col_index = get_column_input(current_player_checker)
        
        if not drop_checker(board, col_index, current_player_checker):
            print(f"Column {chr(ord('A') + col_index)} is full. Player {current_player_checker} loses turn.")
            # Note: The assignment specifies "the player loses the turn" if column is full.
            # So, we don't re-ask for input for the same player, we proceed to the next player.
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue # Skip win/draw check for this invalid turn

        print_board(board) # Print board after successful drop

        if check_win(board, current_player_checker):
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print("The board is full. It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    print("\n--- Game Over ---")

if __name__ == "__main__":
    main()
