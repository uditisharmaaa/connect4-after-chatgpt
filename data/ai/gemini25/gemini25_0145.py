import os
import random
import string

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win
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
        list: A 2D list representing the board, initialized with spaces.
    """
    board = []
    for _ in range(rows):
        board.append([" "] * cols)
    return board


def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the current state of the board.
    """
    clear_screen()
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print(" ", end="")
    for i in range(num_cols):
        print(f" {string.ascii_uppercase[i]} ", end="")
    print()

    # Print board content
    for r in range(len(board)):
        print("+---+" * num_cols)
        print("|", end="")
        for c in range(num_cols):
            print(f" {board[r][c]} |", end="")
        print()
    print("+---+" * num_cols)


def get_column_index(column_char, num_cols):
    """
    Converts a column character (e.g., 'A', 'B') to its corresponding index.

    Args:
        column_char (str): The uppercase character representing the column.
        num_cols (int): The total number of columns on the board.

    Returns:
        int or None: The 0-based index of the column, or None if invalid.
    """
    if len(column_char) == 1 and 'A' <= column_char <= string.ascii_uppercase[num_cols - 1]:
        return ord(column_char) - ord('A')
    return None


def get_player_input(current_player_checker, num_cols):
    """
    Prompts the current player for a column choice and validates it.

    Args:
        current_player_checker (str): The checker symbol for the current player.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-based index of the chosen column.
    """
    while True:
        try:
            prompt = f"Player {current_player_checker}, please enter a column: "
            user_input = input(prompt).upper()
            col_index = get_column_index(user_input, num_cols)

            if col_index is not None:
                return col_index
            else:
                print(f"Invalid input. Please enter a letter between A and {string.ascii_uppercase[num_cols - 1]}.")
        except EOFError:  # Handle Ctrl+D or unexpected input termination
            print("\nGame interrupted. Exiting.")
            exit()
        except Exception:
            print("An unexpected error occurred. Please try again.")


def drop_checker(board, col_index, player_checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The 2D list representing the board.
        col_index (int): The 0-based index of the column to drop the checker into.
        player_checker (str): The checker symbol of the current player.

    Returns:
        bool: True if the checker was successfully placed, False if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Start from the bottom row
        if board[r][col_index] == " ":
            board[r][col_index] = player_checker
            return True
    return False  # Column is full


def check_win(board, player_checker, win_condition):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The 2D list representing the board.
        player_checker (str): The checker symbol of the current player.
        win_condition (int): Number of checkers in a row to win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check vertical
    for c in range(num_cols):
        for r in range(num_rows - win_condition + 1):
            if all(board[r + i][c] == player_checker for i in range(win_condition)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols - win_condition + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(win_condition - 1, num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r - i][c + i] == player_checker for i in range(win_condition)):
                return True

    return False


def check_draw(board):
    """
    Checks if the board is completely full, indicating a draw.

    Args:
        board (list): The 2D list representing the board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw yet
    return True  # No empty spaces found


# --- Main Game Logic ---

def play_connect_4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    players = CHECKERS
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)
    print(f"Player {players[current_player_index]} goes first!")

    game_over = False
    while not game_over:
        current_player_checker = players[current_player_index]
        num_cols = len(board[0])

        col_index = get_player_input(current_player_checker, num_cols)

        # Validate if column is full
        if board[0][col_index] != " ":  # Check the top-most row
            print("Column is full. Please choose another column.")
            # Player does not lose turn, loop continues for the same player
            continue

        # Drop the checker
        if drop_checker(board, col_index, current_player_checker):
            print_board(board)

            # Check for win
            if check_win(board, current_player_checker, WIN_CONDITION):
                print(f"Player {current_player_checker} won!")
                game_over = True
            # Check for draw
            elif check_draw(board):
                print("It's a draw! The board is full.")
                game_over = True
            else:
                # Switch to the next player
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            # This case should ideally be caught by the board[0][col_index] check above,
            # but serves as a failsafe if `drop_checker` returns False unexpectedly.
            print("Could not place checker. Column might be full.")
            # Player does not lose turn, loop continues for the same player
            continue


if __name__ == "__main__":
    play_connect_4()
