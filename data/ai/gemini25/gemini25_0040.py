import os
import random

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]


# --- Helper Functions ---
def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')


def create_board(rows, cols):
    """
    Creates an empty Connect 4 board.

    Args:
        rows (int): The number of rows on the board.
        cols (int): The number of columns on the board.

    Returns:
        list: A 2D list representing the game board, initialized with spaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()
    num_rows = len(board)
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for i in range(num_cols):
        print(f"{chr(ord('A') + i)}   ", end="")
    print()

    # Print the board content
    for r in range(num_rows):
        print("+---" * num_cols + "+")
        print("|", end="")
        for c in range(num_cols):
            print(f" {board[r][c]} |", end="")
        print()
    print("+---" * num_cols + "+")


def get_column_input(player_checker, num_cols):
    """
    Prompts the current player for a column input and validates it.

    Args:
        player_checker (str): The checker symbol of the current player.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The validated column index (0-based).
    """
    while True:
        try:
            col_char = input(f"Player {player_checker}, please enter a column: ").upper()
            if len(col_char) != 1:
                raise ValueError
            col_index = ord(col_char) - ord('A')

            if 0 <= col_index < num_cols:
                return col_index
            else:
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + num_cols - 1)}.")
        except ValueError:
            print("Invalid input. Please enter a single letter for the column.")


def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column to drop the checker into.
        checker (str): The checker symbol to place.

    Returns:
        bool: True if the checker was successfully placed, False if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return True
    return False  # Column is full


def check_win(board, checker, win_condition):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the player to check for a win.
        win_condition (int): The number of checkers in a row required to win.

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

    # Check diagonal wins (positive slope)
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols - win_condition + 1):
            if all(board[r + i][c + i] == checker for i in range(win_condition)):
                return True

    # Check diagonal wins (negative slope)
    for r in range(win_condition - 1, num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r - i][c + i] == checker for i in range(win_condition)):
                return True

    return False


def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The game board.

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
        current_checker = CHECKERS[current_player_index]
        print_board(board)

        col_index = get_column_input(current_checker, NUM_COLS)

        if drop_checker(board, col_index, current_checker):
            if check_win(board, current_checker, WIN_CONDITION):
                winner = current_checker
                game_over = True
            elif check_draw(board):
                game_over = True
            else:
                # Move to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column. (Turn not lost)")
            input("Press Enter to continue...") # Pause to allow user to read the message

    print_board(board)  # Print final board state

    if winner:
        print(f"Player {winner} won!")
    else:
        print("It's a draw!")


# --- Entry Point ---
if __name__ == "__main__":
    play_game()
