import os
import random
import string

# --- Global Constants (for easy modification as per assignment) ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Max 5 players
WIN_SEQUENCE_LENGTH = 4

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
    num_rows = len(board)
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print("  " + "   ".join(string.ascii_uppercase[:num_cols]))

    # Print board rows
    for r in range(num_rows):
        print("+---" * num_cols + "+")
        row_str = "|"
        for c in range(num_cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * num_cols + "+")


def get_column_input(current_player_checker, num_cols):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker symbol of the current player.
        num_cols (int): The total number of columns on the board.

    Returns:
        int: The 0-indexed column number chosen by the player.
    """
    while True:
        try:
            col_char = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if len(col_char) != 1 or not 'A' <= col_char <= string.ascii_uppercase[num_cols - 1]:
                print(f"Invalid input. Please enter a single letter from A to {string.ascii_uppercase[num_cols - 1]}.")
            else:
                return ord(col_char) - ord('A')
        except ValueError:
            print("Invalid input. Please enter a valid column letter.")


def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-indexed column where the checker is to be dropped.
        checker (str): The checker symbol to drop.

    Returns:
        int or None: The 0-indexed row where the checker landed, or None if the column is full.
    """
    num_rows = len(board)
    for r in range(num_rows - 1, -1, -1):  # Start from bottom row
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return r  # Return the row where the checker was placed
    return None  # Column is full


def check_win(board, checker, win_length):
    """
    Checks if the given player (with `checker`) has won the game.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the player to check.
        win_length (int): The number of checkers in a row required to win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Helper function to check a line segment
    def check_line(r_start, c_start, r_delta, c_delta):
        count = 0
        for i in range(win_length):
            r, c = r_start + i * r_delta, c_start + i * c_delta
            if 0 <= r < num_rows and 0 <= c < num_cols and board[r][c] == checker:
                count += 1
            else:
                count = 0  # Reset if the sequence is broken
            if count == win_length:
                return True
        return False

    # Check horizontal wins
    for r in range(num_rows):
        for c in range(num_cols - win_length + 1):
            if all(board[r][c + i] == checker for i in range(win_length)):
                return True

    # Check vertical wins
    for c in range(num_cols):
        for r in range(num_rows - win_length + 1):
            if all(board[r + i][c] == checker for i in range(win_length)):
                return True

    # Check diagonal (top-left to bottom-right) wins
    for r in range(num_rows - win_length + 1):
        for c in range(num_cols - win_length + 1):
            if all(board[r + i][c + i] == checker for i in range(win_length)):
                return True

    # Check diagonal (bottom-left to top-right) wins
    for r in range(win_length - 1, num_rows):
        for c in range(num_cols - win_length + 1):
            if all(board[r - i][c + i] == checker for i in range(win_length)):
                return True

    return False


def check_draw(board):
    """
    Checks if the board is completely filled (a draw condition).

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # Found an empty space, not a draw
    return True  # Board is full


# --- Main Game Logic ---
def play_game():
    """
    Orchestrates the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randrange(NUM_PLAYERS)  # Randomly select first player

    game_over = False
    winner_checker = None

    while not game_over:
        current_player_checker = CHECKERS[current_player_index]
        print_board(board)
        print(f"Player {current_player_checker}, it's your turn.")

        col_input_valid = False
        while not col_input_valid:
            col_index = get_column_input(current_player_checker, NUM_COLS)
            row_placed = drop_checker(board, col_index, current_player_checker)

            if row_placed is None:
                print(f"Column {string.ascii_uppercase[col_index]} is full. Please choose another column.")
            else:
                col_input_valid = True

        # Check for win
        if check_win(board, current_player_checker, WIN_SEQUENCE_LENGTH):
            winner_checker = current_player_checker
            game_over = True
        # Check for draw if no win
        elif check_draw(board):
            game_over = True
            winner_checker = None  # Indicate a draw

        # Switch to next player if game is not over
        if not game_over:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Game over - print final board and result
    print_board(board)
    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("It's a draw!")


# --- Entry Point ---
if __name__ == "__main__":
    play_game()
