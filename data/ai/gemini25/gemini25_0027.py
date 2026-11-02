import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (up to 5 players)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
CURRENT_PLAYERS = PLAYER_CHECKERS[:NUM_PLAYERS]


# --- Helper Functions ---
def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')


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

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for i in range(NUM_COLS):
        print(f" {chr(ord('A') + i)} ", end="")
    print()

    # Print board content
    for r in range(NUM_ROWS):
        print("+---" * NUM_COLS + "+")
        print("|", end="")
        for c in range(NUM_COLS):
            print(f" {board[r][c]} |", end="")
        print()
    print("+---" * NUM_COLS + "+")


def get_column_input(current_player_checker):
    """
    Gets valid column input from the current player.

    Args:
        current_player_checker (str): The checker symbol of the current player.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            player_input = input(f"Player {current_player_checker}, please enter a column: ").upper()

            if len(player_input) != 1 or not ('A' <= player_input <= chr(ord('A') + NUM_COLS - 1)):
                print(f"Invalid input. Please enter a single letter from A to {chr(ord('A') + NUM_COLS - 1)}.")
                continue

            col_index = ord(player_input) - ord('A')
            return col_index
        except KeyboardInterrupt:
            print("\nGame interrupted. Exiting.")
            sys.exit()
        except Exception:
            print("An unexpected error occurred. Please try again.")


def drop_checker(board, col, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col (int): The 0-indexed column to drop the checker into.
        checker (str): The checker symbol to place.

    Returns:
        tuple: (True, row_index) if the checker was placed successfully,
               (False, -1) if the column is full.
    """
    for r in range(NUM_ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return True, r
    return False, -1  # Column is full


def check_win(board, row, col, checker):
    """
    Checks if the last placed checker resulted in a win.

    Args:
        board (list): The game board.
        row (int): The row of the last placed checker.
        col (int): The column of the last placed checker.
        checker (str): The checker symbol of the player who just moved.

    Returns:
        bool: True if the player won, False otherwise.
    """
    # Check horizontal
    count = 0
    for c in range(NUM_COLS):
        if board[row][c] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r_idx in range(NUM_ROWS):
        if board[r_idx][col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0

    # Check positive diagonal (bottom-left to top-right)
    count = 0
    # Start from the bottom-leftmost possible cell of a diagonal containing (row, col)
    start_row = row + min(NUM_ROWS - 1 - row, col)
    start_col = col - min(NUM_ROWS - 1 - row, col)

    while start_row >= 0 and start_col < NUM_COLS:
        if board[start_row][start_col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
        start_row -= 1
        start_col += 1

    # Check negative diagonal (top-left to bottom-right)
    count = 0
    # Start from the top-leftmost possible cell of a diagonal containing (row, col)
    start_row = row - min(row, col)
    start_col = col - min(row, col)

    while start_row < NUM_ROWS and start_col < NUM_COLS:
        if board[start_row][start_col] == checker:
            count += 1
            if count >= WIN_CONDITION:
                return True
        else:
            count = 0
        start_row += 1
        start_col += 1

    return False


def check_draw(board):
    """
    Checks if the board is full, resulting in a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if board[r][c] == " ":
                return False  # There's an empty space
    return True  # Board is full


def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)

    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player_checker = CURRENT_PLAYERS[current_player_index]

    game_over = False

    print_board(board)
    print(f"Player {current_player_checker} goes first!")

    while not game_over:
        col = get_column_input(current_player_checker)

        placed, row_placed = drop_checker(board, col, current_player_checker)

        if not placed:
            print(f"Column {chr(ord('A') + col)} is full! Player {current_player_checker}, please choose another column.")
            # Player does not lose turn, loop continues for the same player
            continue

        print_board(board)

        if check_win(board, row_placed, col, current_player_checker):
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print("The board is full! It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            current_player_checker = CURRENT_PLAYERS[current_player_index]


if __name__ == "__main__":
    main()
