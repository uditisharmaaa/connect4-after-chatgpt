import os
import random
import string

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]


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
    num_cols = len(board[0])
    num_rows = len(board)

    # Print column headers (A, B, C, ...)
    print("  " + "   ".join(string.ascii_uppercase[:num_cols]))

    # Print board content
    for r in range(num_rows):
        print("+---" * num_cols + "+")
        row_content = []
        for c in range(num_cols):
            row_content.append(f"| {board[r][c]} ")
        print("".join(row_content) + "|")
    print("+---" * num_cols + "+")


def get_column_input(current_player_checker, num_cols):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker of the current player.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The validated column index (0-based).
    """
    while True:
        try:
            col_char = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
            if not col_char:
                print("Invalid input. Please enter a letter (e.g., A).")
                continue

            col_index = ord(col_char) - ord('A')

            if 0 <= col_index < num_cols:
                return col_index
            else:
                print(f"Invalid column. Please enter a letter between A and {string.ascii_uppercase[num_cols-1]}.")
        except TypeError:
            print("Invalid input. Please enter a single letter corresponding to a column.")
        except IndexError:
            print("Invalid input. Please enter a single letter corresponding to a column.")


def drop_checker(board, col_index, player_checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column to drop the checker into.
        player_checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was successfully dropped, False if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Start from bottom row
        if board[r][col_index] == " ":
            board[r][col_index] = player_checker
            return True
    return False  # Column is full


def check_win(board, player_checker, win_condition):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        player_checker (str): The checker symbol for the current player.
        win_condition (int): The number of checkers in a row needed to win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal wins
    for r in range(num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check vertical wins
    for c in range(num_cols):
        for r in range(num_rows - win_condition + 1):
            if all(board[r + i][c] == player_checker for i in range(win_condition)):
                return True

    # Check diagonal (positive slope) wins
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols - win_condition + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check diagonal (negative slope) wins
    for r in range(win_condition - 1, num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r - i][c + i] == player_checker for i in range(win_condition)):
                return True

    return False


def check_draw(board):
    """
    Checks if the game is a draw (board is full).

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


def main():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    num_cols = len(board[0])

    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_player_checker = PLAYER_CHECKERS[current_player_index]

    game_over = False

    while not game_over:
        print_board(board)
        print(f"Player {current_player_checker}'s turn.")

        col_index = get_column_input(current_player_checker, num_cols)

        if drop_checker(board, col_index, current_player_checker):
            # Checker was successfully placed
            if check_win(board, current_player_checker, WIN_CONDITION):
                print_board(board)
                print(f"Player {current_player_checker} won!")
                game_over = True
            elif check_draw(board):
                print_board(board)
                print("It's a draw!")
                game_over = True
            else:
                # Next player's turn
                current_player_index = (current_player_index + 1) % NUM_PLAYERS
                current_player_checker = PLAYER_CHECKERS[current_player_index]
        else:
            print(f"Column {string.ascii_uppercase[col_index]} is full. Please choose another column.")
            # Player does not lose turn if column is full, they are prompted again


if __name__ == "__main__":
    main()
