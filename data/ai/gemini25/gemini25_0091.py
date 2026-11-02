import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels
NUM_PLAYERS = 2  # Between 2 and 5 players

# Checkers available
CHECKERS = ["X", "O", "V", "H", "M"]

# Determine checkers for the current game based on NUM_PLAYERS
GAME_CHECKERS = CHECKERS[:NUM_PLAYERS]


# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')


def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board, initialized with spaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board


def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    num_cols = len(board[0])

    # Print column headers (A, B, C, ...)
    col_labels = [chr(ord('A') + i) for i in range(num_cols)]
    print("  " + "   ".join(col_labels))

    # Print the board rows
    for r in range(len(board)):
        print("+---" * num_cols + "+")
        row_str = "|"
        for c in range(num_cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * num_cols + "+")


def get_column_input(player_checker, board):
    """
    Prompts the current player for a column input and validates it.

    Args:
        player_checker (str): The checker symbol of the current player.
        board (list): The current state of the game board.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    num_cols = len(board[0])
    while True:
        try:
            prompt = f"Player {player_checker}, please enter a column: "
            col_char = input(prompt).strip().upper()

            if not col_char:
                print("Invalid input: Column cannot be empty. Please try again.")
                continue

            # Check if the input is a single uppercase letter
            if len(col_char) != 1 or not ('A' <= col_char <= chr(ord('A') + num_cols - 1)):
                print(f"Invalid input: Please enter a single letter from A to {chr(ord('A') + num_cols - 1)}. Please try again.")
                continue

            col_index = ord(col_char) - ord('A')

            # Check if the column is full
            if board[0][col_index] != " ":
                print("Column is full. Please choose another column.")
                continue

            return col_index
        except (ValueError, IndexError):
            print("Invalid input: Please enter a valid column letter. Please try again.")


def place_checker(board, col, checker):
    """
    Places the checker in the lowest available row of the specified column.

    Args:
        board (list): The game board.
        col (int): The 0-indexed column where the checker is to be placed.
        checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the checker was successfully placed, False if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Iterate from bottom row upwards
        if board[r][col] == " ":
            board[r][col] = checker
            return True
    return False  # Column is full (should be caught by validation earlier, but good for safety)


def check_win(board, checker):
    """
    Checks if the given player (with `checker`) has won the game.

    Args:
        board (list): The current state of the game board.
        checker (str): The checker symbol of the player to check for a win.

    Returns:
        bool: True if the player has 4 in a row, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical
    for c in range(num_cols):
        for r in range(num_rows - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (positive slope)
    for r in range(num_rows - 3):
        for c in range(num_cols - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (negative slope)
    for r in range(3, num_rows):
        for c in range(num_cols - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False


def check_draw(board):
    """
    Checks if the board is completely filled, indicating a draw.

    Args:
        board (list): The current state of the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True  # No empty spaces, it's a draw


def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_checker = GAME_CHECKERS[current_player_index]

    game_over = False
    
    # Game loop
    while not game_over:
        print_board(board)
        
        col_index = get_column_input(current_checker, board)
        
        # Place the checker
        if place_checker(board, col_index, current_checker):
            # Check for win after placing
            if check_win(board, current_checker):
                print_board(board)
                print(f"Player {current_checker} won!")
                game_over = True
            elif check_draw(board):
                print_board(board)
                print("It's a draw! The board is full.")
                game_over = True
            else:
                # Switch to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
                current_checker = GAME_CHECKERS[current_player_index]
        else:
            # This case should ideally not be reached due to `get_column_input` validation,
            # but it's here for robustness.
            print("Column is full. Please choose another column.") # Player loses turn if this happens.
            # Player does NOT lose turn due to assignment: "the player will be asked to provide another input until the input is valid (the turn is not lost)"
            # So, if this were to happen, the player should be prompted again.
            # However, `get_column_input` already handles this.

    print("Game Over!")


if __name__ == "__main__":
    main()
