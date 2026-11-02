import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']


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
        board.append([' '] * cols)
    return board


def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()  # Clear screen before printing
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for i in range(num_cols):
        print(f"  {chr(ord('A') + i)} ", end="")
    print()

    # Print the board with separators
    for row in board:
        print("+", end="")
        for _ in range(num_cols):
            print("---+", end="")
        print()
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()

    # Print bottom separator
    print("+", end="")
    for _ in range(num_cols):
        print("---+", end="")
    print()


def get_column_input(current_player_checker, board):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker of the current player.
        board (list): The 2D list representing the game board.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    num_cols = len(board[0])
    while True:
        try:
            player_input = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if len(player_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_char = player_input[0]
            col_index = ord(col_char) - ord('A')

            # Check if the column index is within the valid range
            if 0 <= col_index < num_cols:
                # Check if the column is full
                if board[0][col_index] == ' ':  # Check the top row of the chosen column
                    return col_index
                else:
                    print("That column is full. Please choose another column.")
            else:
                print(f"Invalid column '{col_char}'. Please choose a column between A and {chr(ord('A') + num_cols - 1)}.")
        except IndexError:
            print("Invalid input. Please enter a single letter (e.g., A, B, C).")
        except TypeError:
            print("Invalid input type. Please enter a letter.")


def drop_checker(board, col, checker):
    """
    Drops a checker into the specified column on the board.

    Args:
        board (list): The 2D list representing the game board.
        col (int): The 0-indexed column to drop the checker into.
        checker (str): The checker symbol ('X', 'O', etc.).

    Returns:
        bool: True if the checker was successfully dropped, False if the column was full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Iterate from bottom row upwards
        if board[r][col] == ' ':
            board[r][col] = checker
            return True
    return False  # Column is full


def check_win(board, checker):
    """
    Checks if the given player has won the game.

    Args:
        board (list): The 2D list representing the game board.
        checker (str): The checker symbol of the player to check.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal wins
    for r in range(num_rows):
        for c in range(num_cols - (WIN_CONDITION - 1)):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical wins
    for r in range(num_rows - (WIN_CONDITION - 1)):
        for c in range(num_cols):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check positive diagonal wins (bottom-left to top-right)
    for r in range(num_rows - (WIN_CONDITION - 1)):
        for c in range(num_cols - (WIN_CONDITION - 1)):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check negative diagonal wins (top-left to bottom-right)
    for r in range(WIN_CONDITION - 1, num_rows):
        for c in range(num_cols - (WIN_CONDITION - 1)):
            if all(board[r - i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    return False


def check_draw(board):
    """
    Checks if the board is completely filled, resulting in a draw.

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    num_cols = len(board[0])
    # Check if the top row of every column is filled
    for c in range(num_cols):
        if board[0][c] == ' ':
            return False  # An empty space found, so not a draw yet
    return True  # All columns are full


def main():
    """
    Main function to run the Connect 4 game.
    """
    # Initialize game variables
    board = create_board(NUM_ROWS, NUM_COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]  # Get checkers for the specified number of players

    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player_checker = players[current_player_index]

    game_over = False

    print_board(board)
    print(f"Player {current_player_checker} goes first!")

    while not game_over:
        # Get valid column input from the current player
        col_to_drop = get_column_input(current_player_checker, board)

        # Drop the checker
        if drop_checker(board, col_to_drop, current_player_checker):
            print_board(board)

            # Check for a win
            if check_win(board, current_player_checker):
                print(f"Player {current_player_checker} won!")
                game_over = True
            # Check for a draw if no win
            elif check_draw(board):
                print("It's a draw!")
                game_over = True
            else:
                # Switch to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
                current_player_checker = players[current_player_index]
        else:
            # This case should ideally not be reached if get_column_input correctly checks for full columns.
            # However, it's good practice to have a fallback.
            print("Error: Could not drop checker. Column might be full (should have been caught earlier).")


if __name__ == "__main__":
    main()
