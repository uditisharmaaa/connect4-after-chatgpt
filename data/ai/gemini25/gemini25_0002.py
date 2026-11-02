import os
import random
import sys

# --- Global Constants ---
# Board dimensions (can be customized)
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z

# Number of players (between 2 and 5)
NUM_PLAYERS = 2

# Checkers for players
# X, O, V, H, M (5 checkers total)
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# Number of checkers in a row to win
CONNECT_N = 4

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    # 'clear' for Unix/Linux, 'cls' for Windows
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.
    The board is a list of lists, initialized with whitespaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board

def print_board(board):
    """
    Prints the Connect 4 board with column labels.
    Example:
      A   B   C   D   E   F   G
    +---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |
    ...
    """
    clear_screen() # Clear screen before printing the updated board

    # Print column labels (A, B, C...)
    col_labels = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(col_labels))

    # Print the board
    for r in range(len(board)):
        print("+---" * len(board[0]) + "+")
        row_str = "|"
        for c in range(len(board[0])):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * len(board[0]) + "+")

def get_player_input(current_player_checker, board_cols):
    """
    Prompts the current player for their move and validates the input.
    Returns the 0-indexed column number if valid.
    Keeps asking until valid input is received.
    """
    while True:
        try:
            # Get input from the player
            user_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()

            # Check if input is a single letter
            if not (len(user_input) == 1 and 'A' <= user_input <= chr(ord('A') + board_cols - 1)):
                print("Invalid input. Please enter a single uppercase letter corresponding to a column (e.g., A, B, C).")
                continue

            # Convert letter to 0-indexed column number
            col = ord(user_input) - ord('A')
            return col
        except Exception:
            # Catch any unexpected errors, though the specific checks above should handle most
            print("An unexpected error occurred. Please try again.")

def drop_checker(board, col, checker):
    """
    Drops the checker into the specified column.
    Returns True if successful, False if the column is full.
    """
    # Iterate from the bottom row upwards to find the first empty spot
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True # Checker placed successfully
    return False # Column is full

def check_win(board, checker, connect_n):
    """
    Checks if the current player has won the game.
    A win is 4 (or connect_n) checkers in a row horizontally, vertically, or diagonally.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal wins
    for r in range(rows):
        for c in range(cols - connect_n + 1):
            if all(board[r][c + i] == checker for i in range(connect_n)):
                return True

    # Check vertical wins
    for c in range(cols):
        for r in range(rows - connect_n + 1):
            if all(board[r + i][c] == checker for i in range(connect_n)):
                return True

    # Check positive slope diagonal wins (bottom-left to top-right)
    for r in range(rows - connect_n + 1):
        for c in range(cols - connect_n + 1):
            if all(board[r + i][c + i] == checker for i in range(connect_n)):
                return True

    # Check negative slope diagonal wins (top-left to bottom-right)
    for r in range(rows - connect_n + 1):
        for c in range(connect_n - 1, cols):
            if all(board[r + i][c - i] == checker for i in range(connect_n)):
                return True

    return False

def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False # Found an empty spot, not a draw yet
    return True # No empty spots, it's a draw

def main():
    """
    Main function to run the Connect 4 game.
    Initializes the board, handles game turns, and checks for win/draw conditions.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    players = CHECKERS # Using the global CHECKERS list

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Game loop
    while True:
        current_player_checker = players[current_player_index]
        
        print_board(board) # Print the board before each turn

        # Get valid input from the current player
        col = get_player_input(current_player_checker, NUM_COLS)

        # Attempt to drop the checker
        if not drop_checker(board, col, current_player_checker):
            print(f"Column {chr(ord('A') + col)} is full. Player {current_player_checker} loses their turn!")
            # The player loses their turn, so we don't change the current_player_index
            # and they will be prompted again after the next player's turn if no one wins.
            # This interpretation differs from "turn is not lost" if the column is full.
            # Rereading: "If the column is already completely filled with checkers, the turn is invalid and the player loses the turn."
            # This implies the turn is simply skipped for this player, and it moves to the next player.
            # So, the player index *should* advance. Let's adjust this.
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue # Skip to the next iteration of the loop
        
        # After a successful move, check for win condition
        if check_win(board, current_player_checker, CONNECT_N):
            print_board(board)
            print(f"Player {current_player_checker} won!")
            break # End the game

        # After a successful move, check for draw condition
        if check_draw(board):
            print_board(board)
            print("The board is full. It's a draw!")
            break # End the game

        # If no win or draw, switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
