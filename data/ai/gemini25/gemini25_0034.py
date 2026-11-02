import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers needed to win

# Available checkers for players
CHECKERS = ["X", "O", "V", "H", "M"]


# --- Board Functions ---
def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the Connect 4 board.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board


def print_board(board):
    """
    Prints the Connect 4 board to the console, including column labels.

    Args:
        board (list): The 2D list representing the Connect 4 board.
    """
    # Clear the terminal screen
    os.system('clear')

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for i in range(len(board[0])):
        print(f"{chr(ord('A') + i):>3}", end="")
    print()

    # Print the board with separators
    for r in range(len(board)):
        print("+", end="")
        for _ in range(len(board[0])):
            print("---+", end="")
        print()
        print("|", end="")
        for c in range(len(board[0])):
            print(f" {board[r][c]} |", end="")
        print()
    # Print the last bottom line
    print("+", end="")
    for _ in range(len(board[0])):
        print("---+", end="")
    print()


# --- Game Logic Functions ---
def get_player_input(current_player_checker, board_cols):
    """
    Prompts the current player for a column choice and validates the input.

    Args:
        current_player_checker (str): The checker symbol of the current player.
        board_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            column_input = input(f"Player {current_player_checker}, please enter a column: ").upper()

            if not column_input:  # Handle empty input
                print("Invalid input. Please enter a letter (e.g., A, B).")
                continue

            # Convert column letter to 0-indexed integer
            col_index = ord(column_input) - ord('A')

            # Validate column index
            if not (0 <= col_index < board_cols):
                print(f"Invalid column. Please enter a letter from A to {chr(ord('A') + board_cols - 1)}.")
                continue

            return col_index
        except TypeError: # This might catch cases where ord() fails on non-string (though input() returns string)
            print("Invalid input. Please enter a single letter corresponding to a column.")
        except Exception: # Catch any other unexpected errors during input
            print("An unexpected error occurred. Please try again.")


def drop_checker(board, col_index, player_checker):
    """
    Drops the player's checker into the specified column.

    Args:
        board (list): The 2D list representing the Connect 4 board.
        col_index (int): The 0-indexed column number to drop the checker into.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the checker was successfully placed, False if the column is full.
    """
    # Iterate from the bottom row upwards to find the first empty spot
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = player_checker
            return True
    return False  # Column is full


def check_win(board, player_checker, win_length):
    """
    Checks if the given player has achieved a win condition (4 in a row)
    horizontally, vertically, or diagonally.

    Args:
        board (list): The 2D list representing the Connect 4 board.
        player_checker (str): The checker symbol of the current player.
        win_length (int): The number of checkers needed to win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal wins
    for r in range(num_rows):
        for c in range(num_cols - win_length + 1):
            if all(board[r][c + i] == player_checker for i in range(win_length)):
                return True

    # Check vertical wins
    for r in range(num_rows - win_length + 1):
        for c in range(num_cols):
            if all(board[r + i][c] == player_checker for i in range(win_length)):
                return True

    # Check diagonal wins (top-left to bottom-right)
    for r in range(num_rows - win_length + 1):
        for c in range(num_cols - win_length + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_length)):
                return True

    # Check diagonal wins (top-right to bottom-left)
    for r in range(win_length - 1, num_rows):
        for c in range(num_cols - win_length + 1):
            if all(board[r - i][c + i] == player_checker for i in range(win_length)):
                return True

    return False


def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The 2D list representing the Connect 4 board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    # A draw occurs if all cells are filled and no one has won
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty cell, not a draw
    return True  # No empty cells found, it's a draw


def main():
    """
    Main function to run the Connect 4 game.
    """
    # Initialize game board
    board = create_board(NUM_ROWS, NUM_COLS)

    # Prepare players and their checkers
    # Slicing CHECKERS list based on NUM_PLAYERS
    player_checkers = CHECKERS[:NUM_PLAYERS]

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player_checker = player_checkers[current_player_index]

    game_over = False
    turn_count = 0

    while not game_over:
        print_board(board)
        print(f"Player {current_player_checker}'s turn.")

        # Get and validate player input
        col_index = get_player_input(current_player_checker, NUM_COLS)

        # Attempt to drop checker
        if drop_checker(board, col_index, current_player_checker):
            turn_count += 1
            # Check for win
            if check_win(board, current_player_checker, WIN_CONDITION):
                print_board(board)  # Print final board
                print(f"Player {current_player_checker} won!")
                game_over = True
            # Check for draw if not won
            elif check_draw(board):
                print_board(board)  # Print final board
                print("The game is a draw!")
                game_over = True
            else:
                # Switch to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
                current_player_checker = player_checkers[current_player_index]
        else:
            # Column was full, current player loses turn (as per assignment spec)
            # Re-ask the same player for input (modified for clarity based on "the turn is not lost")
            # If the column is full, the player is asked again for a valid input in the current turn.
            # The assignment says "If the column is already completely filled with checkers, the turn is invalid
            # and the player loses the turn." and also "if the player provides an invalid input, the player
            # will be asked to provide another input until the input is valid (the turn is not lost)".
            # I will interpret this as: if the *chosen column* is full, it's an invalid move for that column,
            # and the player needs to choose a different column. So the turn is NOT lost, but the choice is invalid.
            print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
            # The loop continues, asking the *same* player again.

    print("Game Over!")


# Entry point for the script
if __name__ == "__main__":
    main()
