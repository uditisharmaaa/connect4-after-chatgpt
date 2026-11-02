import os
import random

# --- Constants ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers needed to win

# Player checkers (X, O, V, H, M)
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# Column labels (A, B, C, ...)
COLUMN_LABELS = [chr(ord('A') + i) for i in range(NUM_COLS)]


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
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Prints the Connect 4 board to the console.

    Args:
        board (list): The 2D list representing the game board.
    """
    clear_screen()

    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS[:len(board[0])]))

    # Print board rows
    for r in range(len(board)):
        print("+---" * len(board[0]) + "+")
        row_str = "|"
        for c in range(len(board[0])):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * len(board[0]) + "+")


def is_valid_column_input(col_input, num_cols):
    """
    Validates if the user's column input is a valid letter and within bounds.

    Args:
        col_input (str): The user's raw input for the column.
        num_cols (int): The total number of columns on the board.

    Returns:
        int or None: The 0-indexed column number if valid, None otherwise.
    """
    if not isinstance(col_input, str) or len(col_input) != 1 or not col_input.isalpha():
        return None

    col_input = col_input.upper()
    if col_input not in COLUMN_LABELS[:num_cols]:
        return None

    return ord(col_input) - ord('A')


def get_next_available_row(board, col):
    """
    Finds the lowest available row in a given column.

    Args:
        board (list): The game board.
        col (int): The 0-indexed column number.

    Returns:
        int or None: The 0-indexed row number if space is available, None if column is full.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def place_checker(board, col, player_checker):
    """
    Places a checker in the specified column.

    Args:
        board (list): The game board.
        col (int): The 0-indexed column number.
        player_checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was placed successfully, False if the column was full.
    """
    row = get_next_available_row(board, col)
    if row is not None:
        board[row][col] = player_checker
        return True
    return False


def check_win(board, player_checker, win_condition):
    """
    Checks if the current player has won the game.

    Args:
        board (list): The game board.
        player_checker (str): The checker symbol for the current player.
        win_condition (int): The number of checkers needed for a win.

    Returns:
        bool: True if the current player has won, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - win_condition + 1):
            if all(board[r][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check vertical
    for r in range(rows - win_condition + 1):
        for c in range(cols):
            if all(board[r + i][c] == player_checker for i in range(win_condition)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - win_condition + 1):
        for c in range(cols - win_condition + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(win_condition - 1, rows):
        for c in range(cols - win_condition + 1):
            if all(board[r - i][c + i] == player_checker for i in range(win_condition)):
                return True

    return False


def check_draw(board):
    """
    Checks if the board is completely filled (game is a draw).

    Args:
        board (list): The game board.

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
    players = PLAYER_CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    game_over = False
    winner_checker = None

    while not game_over:
        current_player_checker = players[current_player_index]
        print_board(board)
        print(f"Player {current_player_checker}, please enter a column:")

        valid_turn = False
        while not valid_turn:
            col_input = input().strip()
            col_index = is_valid_column_input(col_input, NUM_COLS)

            if col_index is None:
                print("Invalid column. Please enter a letter from A to "
                      f"{COLUMN_LABELS[NUM_COLS - 1]}:")
            else:
                if place_checker(board, col_index, current_player_checker):
                    valid_turn = True
                else:
                    print(f"Column {col_input.upper()} is full. Please choose another column:")

        # After a valid turn, check for win or draw
        if check_win(board, current_player_checker, WIN_CONDITION):
            print_board(board)
            winner_checker = current_player_checker
            game_over = True
        elif check_draw(board):
            print_board(board)
            game_over = True  # It's a draw
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # Game end
    if winner_checker:
        print(f"Player {winner_checker} won!")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    play_connect_4()
