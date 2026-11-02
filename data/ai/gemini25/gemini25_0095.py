import os
import random
import sys

# --- GLOBAL CONSTANTS ---
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2  # Set to 2 for submission
WIN_CONDITION = 4  # Number of checkers in a row to win

# Available checkers for players
CHECKERS = ["X", "O", "V", "H", "M"]
PLAYER_CHECKERS = CHECKERS[:NUM_PLAYERS]


# --- HELPER FUNCTIONS ---
def clear_screen():
    """Clears the terminal screen."""
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')


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
    num_cols = len(board[0])

    # Print column headers (A, B, C, ...)
    header = "  "
    for i in range(num_cols):
        header += chr(ord('A') + i) + "   "
    print(header)

    # Print the board rows
    for r in range(len(board)):
        print("+---" * num_cols + "+")
        row_str = "|"
        for c in range(num_cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print("+---" * num_cols + "+")


def is_valid_column_input(col_input, num_cols):
    """
    Validates the user's column input.

    Args:
        col_input (str): The column input provided by the user.
        num_cols (int): The total number of columns on the board.

    Returns:
        int or None: The 0-indexed column number if valid, None otherwise.
    """
    if not isinstance(col_input, str) or len(col_input) != 1:
        return None

    col_input = col_input.upper()
    col_index = ord(col_input) - ord('A')

    if 0 <= col_index < num_cols:
        return col_index
    return None


def get_available_row(board, col):
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


def drop_checker(board, col, player_checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col (int): The 0-indexed column number.
        player_checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was successfully dropped, False if the column was full.
    """
    row = get_available_row(board, col)
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
        win_condition (int): Number of checkers needed in a row to win.

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

    # Check positive slope diagonal wins (bottom-left to top-right)
    for r in range(num_rows - win_condition + 1):
        for c in range(num_cols - win_condition + 1):
            if all(board[r + i][c + i] == player_checker for i in range(win_condition)):
                return True

    # Check negative slope diagonal wins (top-left to bottom-right)
    for r in range(win_condition - 1, num_rows):
        for c in range(num_cols - win_condition + 1):
            if all(board[r - i][c + i] == player_checker for i in range(win_condition)):
                return True

    return False


def check_draw(board):
    """
    Checks if the board is full, indicating a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False  # An empty space found, game is not a draw yet
    return True  # No empty spaces, board is full


def get_player_turn(current_player_index, num_players):
    """
    Calculates the next player's turn.

    Args:
        current_player_index (int): The 0-indexed index of the current player.
        num_players (int): The total number of players.

    Returns:
        int: The 0-indexed index of the next player.
    """
    return (current_player_index + 1) % num_players


# --- MAIN GAME LOGIC ---
def play_connect4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    while not game_over:
        player_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)
        print(f"Player {player_checker}, please enter a column:")

        column_chosen = False
        while not column_chosen:
            user_input = input().strip()
            col_index = is_valid_column_input(user_input, NUM_COLS)

            if col_index is None:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            if not drop_checker(board, col_index, player_checker):
                print(f"Column {user_input.upper()} is full. Please choose another column.")
                continue

            column_chosen = True

        if check_win(board, player_checker, WIN_CONDITION):
            print_board(board)
            print(f"Player {player_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("The board is full. It's a draw!")
            game_over = True
        else:
            current_player_index = get_player_turn(current_player_index, NUM_PLAYERS)


if __name__ == "__main__":
    play_connect4()
