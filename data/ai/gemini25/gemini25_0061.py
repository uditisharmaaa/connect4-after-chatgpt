import os
import random

# --- Constants ---
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
    # Print column labels (A, B, C, ...)
    print("  " + "   ".join([chr(ord('A') + i) for i in range(num_cols)]))
    for r_idx, row in enumerate(board):
        # Print top border for each row
        print("+---" * num_cols + "+")
        # Print cell content
        print("| " + " | ".join(row) + " |")
    # Print bottom border of the last row
    print("+---" * num_cols + "+")


def get_column_input(current_player_checker, board_cols):
    """
    Prompts the current player for a column input and validates it.

    Args:
        current_player_checker (str): The checker symbol of the current player.
        board_cols (int): The total number of columns on the board.

    Returns:
        int: The validated column index (0-based).
    """
    while True:
        try:
            col_letter = input(f"Player {current_player_checker}, please enter a column: ").upper()
            if not col_letter.isalpha() or len(col_letter) != 1:
                print("Invalid input. Please enter a single letter (e.g., A, B, C).")
                continue

            col_index = ord(col_letter) - ord('A')

            if 0 <= col_index < board_cols:
                return col_index
            else:
                print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + board_cols - 1)}.")
        except Exception:
            print("Invalid input. Please try again.")


def drop_checker(board, col_index, checker):
    """
    Drops a checker into the specified column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column to drop the checker into.
        checker (str): The checker symbol to place.

    Returns:
        bool: True if the checker was placed successfully, False if the column is full.
    """
    for r_idx in range(len(board) - 1, -1, -1):
        if board[r_idx][col_index] == " ":
            board[r_idx][col_index] = checker
            return True
    return False


def check_win(board, checker):
    """
    Checks if the given player has won the game.

    Args:
        board (list): The game board.
        checker (str): The checker symbol of the player to check for a win.

    Returns:
        bool: True if the player has won, False otherwise.
    """
    rows = len(board)
    cols = len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check vertical
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(cols):
            if all(board[r + i][c] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(cols - WIN_CONDITION + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_CONDITION)):
                return True

    # Check diagonal (top-right to bottom-left)
    for r in range(rows - WIN_CONDITION + 1):
        for c in range(WIN_CONDITION - 1, cols):
            if all(board[r + i][c - i] == checker for i in range(WIN_CONDITION)):
                return True
    return False


def check_draw(board):
    """
    Checks if the board is full, resulting in a draw.

    Args:
        board (list): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    for row in board:
        if " " in row:
            return False
    return True


# --- Main Game Logic ---
def play_connect_4():
    """Main function to run the Connect 4 game."""
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    while not game_over:
        current_player_checker = PLAYER_CHECKERS[current_player_index]
        print_board(board)

        valid_drop = False
        while not valid_drop:
            col_index = get_column_input(current_player_checker, NUM_COLS)
            if drop_checker(board, col_index, current_player_checker):
                valid_drop = True
            else:
                print(f"Column {chr(ord('A') + col_index)} is full. Please choose another column.")
                # Player does not lose turn for choosing a full column

        if check_win(board, current_player_checker):
            print_board(board)  # Print final board with winning move
            print(f"Player {current_player_checker} won!")
            game_over = True
        elif check_draw(board):
            print_board(board)  # Print final board
            print("The board is full. It's a draw!")
            game_over = True
        else:
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_connect_4()
