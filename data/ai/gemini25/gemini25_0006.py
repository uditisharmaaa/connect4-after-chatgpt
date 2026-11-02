import os
import random
import sys

# --- Global Constants (Editable for different game configurations) ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for A-Z column labels
NUM_PLAYERS = 2
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (up to 5 players supported by the assignment description)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]


# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.
    Args:
        rows (int): The number of rows in the board.
        cols (int): The number of columns in the board.
    Returns:
        list: A 2D list representing the game board.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Prints the Connect 4 board to the console with column labels.
    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col_index in range(num_cols):
        print(f"{chr(ord('A') + col_index)}   ", end="")
    print()

    # Print board content
    for r in range(len(board)):
        print("+---" * num_cols + "+")
        print("|", end="")
        for c in range(num_cols):
            print(f" {board[r][c]} |", end="")
        print()
    print("+---" * num_cols + "+")


def get_column_input(current_player_checker, num_cols):
    """
    Prompts the current player for a column input and validates it.
    Args:
        current_player_checker (str): The checker symbol of the current player.
        num_cols (int): The total number of columns on the board.
    Returns:
        int: The 0-indexed column number if input is valid.
    """
    while True:
        try:
            prompt = f"Player {current_player_checker}, please enter a column: "
            user_input = input(prompt).strip().upper()

            if not user_input:
                print("Invalid input: Column cannot be empty. Please try again.")
                continue

            # Check if input is a single letter
            if len(user_input) != 1 or not user_input.isalpha():
                print("Invalid input: Please enter a single letter (e.g., A, B, C).")
                continue

            # Convert letter to 0-indexed column number
            col_index = ord(user_input) - ord('A')

            # Check if column index is within board bounds
            if 0 <= col_index < num_cols:
                return col_index
            else:
                print(f"Invalid input: Column '{user_input}' is out of board range. Valid columns are A-{chr(ord('A') + num_cols - 1)}.")
        except Exception:
            print("An unexpected error occurred. Please try again.")


def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.
    Args:
        board (list): The game board.
        col_index (int): The 0-indexed column number.
        checker (str): The checker symbol to place.
    Returns:
        bool: True if the checker was placed successfully, False if the column is full.
    """
    for r in range(len(board) - 1, -1, -1):  # Start from bottom row
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True
    return False  # Column is full


def check_win(board, checker, win_condition):
    """
    Checks if the given player (checker) has won the game.
    Args:
        board (list): The game board.
        checker (str): The checker symbol of the player to check.
        win_condition (int): The number of checkers in a row needed to win.
    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal wins
    for r in range(num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r][c + i] == checker for i in range(win_condition)):
                return True

    # Check vertical wins
    for c in range(num_cols):
        for r in range(num_rows - win_condition + 1):
            if all(board[r + i][c] == checker for i in range(win_condition)):
                return True

    # Check positive slope diagonal wins (bottom-left to top-right)
    for r in range(win_condition - 1, num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r - i][c + i] == checker for i in range(win_condition)):
                return True

    # Check negative slope diagonal wins (top-left to bottom-right)
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols - win_condition + 1):
            if all(board[r + i][c + i] == checker for i in range(win_condition)):
                return True

    return False


def check_draw(board):
    """
    Checks if the board is completely full (a draw).
    Args:
        board (list): The game board.
    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True  # No empty spaces found, it's a draw


def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Game loop
    while True:
        current_player_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)
        
        col_index = get_column_input(current_player_checker, NUM_COLS)

        if drop_checker(board, col_index, current_player_checker):
            # Checker was successfully placed
            
            # Check for win
            if check_win(board, current_player_checker, WIN_CONDITION):
                print_board(board)
                print(f"Player {current_player_checker} won!")
                break
            
            # Check for draw
            if check_draw(board):
                print_board(board)
                print("It's a draw! The board is full.")
                break
            
            # Move to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            print(f"Column {chr(ord('A') + col_index)} is full. Player {current_player_checker}, you lose your turn. Please choose another column.")
            # Player does not lose turn according to assignment, re-prompt for input
            # The assignment description is slightly ambiguous here: "the turn is not lost" vs "player loses the turn"
            # I will interpret "the turn is not lost" to mean they get to try again.
            # If "player loses the turn" is the intended behaviour, simply remove this print and the next line
            # and the loop will naturally re-prompt for the same player.
            # I will stick to "turn is not lost" as stated earlier, which implies re-prompt for current player.
            # The current implementation (not incrementing current_player_index if drop fails) already does this.
            input("Press Enter to continue...") # Pause to let user read the message

if __name__ == "__main__":
    main()
