import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_LENGTH = 4

# Player checkers (X, O, V, H, M)
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]


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
        list: A 2D list representing the empty board.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board


def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the current game board.
    """
    clear_screen()
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for col_idx in range(num_cols):
        print(f" {chr(ord('A') + col_idx)} ", end="")
    print()

    # Print board rows
    for row_idx in range(len(board)):
        print("+", end="")
        for _ in range(num_cols):
            print("---+", end="")
        print()
        print("|", end="")
        for col_idx in range(num_cols):
            print(f" {board[row_idx][col_idx]} |", end="")
        print()
    # Print bottom border
    print("+", end="")
    for _ in range(num_cols):
        print("---+", end="")
    print()


def get_column_input(current_player_checker):
    """
    Gets and validates the player's column input.

    Args:
        current_player_checker (str): The checker of the current player.

    Returns:
        int: The 0-based index of the chosen column.
    """
    num_cols = NUM_COLS
    while True:
        try:
            user_input = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if len(user_input) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B).")
                continue

            col_char = user_input[0]
            col_index = ord(col_char) - ord('A')

            if 0 <= col_index < num_cols:
                return col_index
            else:
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")
        except (ValueError, TypeError):
            print("Invalid input. Please enter a valid column letter.")


def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The 2D list representing the game board.
        col_index (int): The 0-based index of the column to drop the checker into.
        checker (str): The checker symbol (e.g., "X", "O").

    Returns:
        bool: True if the checker was successfully dropped, False if the column is full.
    """
    num_rows = len(board)
    for row_idx in range(num_rows - 1, -1, -1):  # Iterate from bottom to top
        if board[row_idx][col_index] == " ":
            board[row_idx][col_index] = checker
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
        for c in range(num_cols - WIN_LENGTH + 1):
            if all(board[r][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check vertical wins
    for r in range(num_rows - WIN_LENGTH + 1):
        for c in range(num_cols):
            if all(board[r + i][c] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal wins (top-left to bottom-right)
    for r in range(num_rows - WIN_LENGTH + 1):
        for c in range(num_cols - WIN_LENGTH + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    # Check diagonal wins (bottom-left to top-right)
    for r in range(WIN_LENGTH - 1, num_rows):
        for c in range(num_cols - WIN_LENGTH + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
                return True

    return False


def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The 2D list representing the game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])
    for r in range(num_rows):
        for c in range(num_cols):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True  # Board is full


# --- Main Game Logic ---

def play_game():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False
    winner = None

    while not game_over:
        current_player_checker = CHECKERS[current_player_index]
        print_board(board)

        col_index = get_column_input(current_player_checker)

        if drop_checker(board, col_index, current_player_checker):
            # Checker was successfully dropped
            if check_win(board, current_player_checker):
                winner = current_player_checker
                game_over = True
            elif check_draw(board):
                game_over = True
            else:
                # Move to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            # Column was full, player's turn is invalid, they retry
            print("That column is full. Please choose another column.")
            # The player does not lose their turn here, they are asked again

    print_board(board)  # Print final board state

    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    play_game()
