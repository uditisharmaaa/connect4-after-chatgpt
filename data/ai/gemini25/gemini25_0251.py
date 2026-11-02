import os
import random
import sys

# --- Global Constants ---
NUM_ROWS = 6
NUM_COLS = 7  # Max 26 for column labels A-Z
NUM_PLAYERS = 2  # Between 2 and 5 players
WIN_SEQUENCE_LENGTH = 4

# Player checkers, chosen in order
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]


# --- Helper Functions ---
def clear_screen():
    """Clears the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')


def create_board(rows, cols):
    """
    Creates an empty Connect 4 board initialized with whitespaces.

    Args:
        rows (int): The number of rows for the board.
        cols (int): The number of columns for the board.

    Returns:
        list: A 2D list representing the game board.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Prints the Connect 4 board to the console with column labels.

    Args:
        board (list): The 2D list representing the game board.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Print column labels (A, B, C, ...)
    print("  ", end="")
    for col_index in range(num_cols):
        print(f"{chr(ord('A') + col_index)}   ", end="")
    print()

    # Print board rows
    for row in range(num_rows):
        print("+---" * num_cols + "+")
        print("|", end="")
        for col in range(num_cols):
            print(f" {board[row][col]} |", end="")
        print()
    print("+---" * num_cols + "+")


def is_valid_column_input(col_input, num_cols):
    """
    Validates if the user's column input is a single uppercase letter
    within the valid range of columns.

    Args:
        col_input (str): The user's input for the column.
        num_cols (int): The total number of columns on the board.

    Returns:
        int or None: The 0-based column index if valid, None otherwise.
    """
    if len(col_input) != 1 or not col_input.isalpha():
        return None

    col_index = ord(col_input.upper()) - ord('A')
    if 0 <= col_index < num_cols:
        return col_index
    return None


def get_next_available_row(board, col_index):
    """
    Finds the lowest available row in a given column.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column.

    Returns:
        int or None: The 0-based row index if space is available,
                     None if the column is full.
    """
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_index] == " ":
            return row
    return None


def place_checker(board, col_index, player_checker):
    """
    Places a player's checker in the specified column at the lowest available spot.

    Args:
        board (list): The game board.
        col_index (int): The 0-based index of the column.
        player_checker (str): The checker symbol for the current player.

    Returns:
        bool: True if the checker was successfully placed, False if the column is full.
    """
    row_index = get_next_available_row(board, col_index)
    if row_index is not None:
        board[row_index][col_index] = player_checker
        return True
    return False


def check_win(board, player_checker, sequence_length):
    """
    Checks if the current player has won the game by getting `sequence_length`
    checkers in a row horizontally, vertically, or diagonally.

    Args:
        board (list): The game board.
        player_checker (str): The checker symbol of the player to check.
        sequence_length (int): The number of checkers needed to win (e.g., 4 for Connect 4).

    Returns:
        bool: True if the player has won, False otherwise.
    """
    num_rows = len(board)
    num_cols = len(board[0])

    # Check horizontal
    for r in range(num_rows):
        for c in range(num_cols - sequence_length + 1):
            if all(board[r][c + i] == player_checker for i in range(sequence_length)):
                return True

    # Check vertical
    for r in range(num_rows - sequence_length + 1):
        for c in range(num_cols):
            if all(board[r + i][c] == player_checker for i in range(sequence_length)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(num_rows - sequence_length + 1):
        for c in range(num_cols - sequence_length + 1):
            if all(board[r + i][c + i] == player_checker for i in range(sequence_length)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(sequence_length - 1, num_rows):
        for c in range(num_cols - sequence_length + 1):
            if all(board[r - i][c + i] == player_checker for i in range(sequence_length)):
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
    for row in board:
        if " " in row:
            return False
    return True


# --- Main Game Logic ---
def play_connect4():
    """
    Main function to run the Connect 4 game.
    """
    board = create_board(NUM_ROWS, NUM_COLS)
    num_players = len(PLAYER_CHECKERS)

    # Randomly select the first player
    current_player_index = random.randint(0, num_players - 1)

    game_over = False
    winning_player = None

    while not game_over:
        clear_screen()
        print_board(board)

        current_player_checker = PLAYER_CHECKERS[current_player_index]
        print(f"Player {current_player_checker}, please enter a column: ", end="")

        valid_turn = False
        while not valid_turn:
            try:
                col_input = input().strip().upper()
                col_index = is_valid_column_input(col_input, NUM_COLS)

                if col_index is None:
                    print("Invalid input. Please enter a single letter (A-{}): ".format(
                        chr(ord('A') + NUM_COLS - 1)), end="")
                    continue

                if place_checker(board, col_index, current_player_checker):
                    valid_turn = True
                else:
                    # If column is full, it's an invalid turn and player loses turn
                    print("Column {} is full. Please choose another column: ".format(col_input), end="")
                    # Do not set valid_turn = True here, let them try again in this loop
            except EOFError: # Handles Ctrl+D in some terminals
                print("\nGame interrupted. Exiting.")
                sys.exit()


        # After a valid placement, check for win or draw
        if check_win(board, current_player_checker, WIN_SEQUENCE_LENGTH):
            winning_player = current_player_checker
            game_over = True
        elif check_draw(board):
            game_over = True
        else:
            # Switch to the next player
            current_player_index = (current_player_index + 1) % num_players

    # Game over - print final board and result
    clear_screen()
    print_board(board)

    if winning_player:
        print(f"Player {winning_player} won!")
    else:
        print("It's a draw!")


# --- Entry Point ---
if __name__ == "__main__":
    play_connect4()
