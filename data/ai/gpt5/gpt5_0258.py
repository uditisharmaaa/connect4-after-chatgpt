import os
import random
import sys

# -----------------------------
# Configuration constants
# -----------------------------
ROWS = 6            # Number of rows on the board (default submission: 6)
COLS = 7            # Number of columns on the board (default submission: 7); must be <= 26
NUM_PLAYERS = 2     # Number of players (2..5). Checkers assigned in order: X, O, V, H, M
WIN_LENGTH = 4      # Number of consecutive checkers needed to win (always 4)

# Checkers for up to 5 players in order
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# -----------------------------
# Utility functions
# -----------------------------

def clear_screen():
    """
    Clear the terminal screen using the 'clear' command (Linux/Unix).
    """
    os.system('clear')


def create_board(rows, cols):
    """
    Create a 2D list representing the board initialized with spaces.

    Args:
        rows (int): number of rows
        cols (int): number of columns

    Returns:
        list[list[str]]: rows x cols board filled with " "
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Print the board to the terminal following the required format.
    Column labels are letters starting from 'A'. Rows are unlabeled.

    Args:
        board (list[list[str]]): the current game board
    """
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Column labels
    labels = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(labels)

    # Horizontal separator for columns
    sep = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(sep)
        # Each cell in the row
        row_str = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row_str)
    print(sep)


def get_valid_column_input(cols):
    """
    Prompt the current player for a column letter and validate the input.
    Keeps asking until a valid letter within the board's columns is provided.

    Args:
        cols (int): number of columns

    Returns:
        int: zero-based column index
    """
    max_label = chr(ord('A') + cols - 1)
    while True:
        user_input = input(f"Please enter a column (A-{max_label}): ").strip()
        if not user_input:
            print("Invalid input: empty. Try again.")
            continue
        # Accept lowercase by converting to uppercase (more user-friendly)
        col_letter = user_input.upper()

        if len(col_letter) != 1 or not ('A' <= col_letter <= max_label):
            print(f"Invalid input: please enter a single letter between A and {max_label}.")
            continue

        col_idx = ord(col_letter) - ord('A')
        return col_idx


def drop_checker(board, col_idx, checker):
    """
    Drop a checker into the specified column. The checker falls to the lowest
    available cell in that column.

    Args:
        board (list[list[str]]): game board
        col_idx (int): target column index (0-based)
        checker (str): player's checker symbol

    Returns:
        tuple[int, int] | None: (row_idx, col_idx) where checker landed, or None if column is full
    """
    rows = len(board)

    # Start from the bottom row and find the first empty space
    for r in range(rows - 1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return (r, col_idx)

    # Column full
    return None


def in_bounds(r, c, rows, cols):
    """
    Check whether a row, col pair is within the board bounds.
    """
    return 0 <= r < rows and 0 <= c < cols


def count_consecutive(board, start_r, start_c, dr, dc, checker):
    """
    Count consecutive checkers starting from (start_r, start_c) moving in direction (dr, dc)
    including the starting cell, as long as the checker matches.

    Args:
        board (list[list[str]]): game board
        start_r (int): starting row
        start_c (int): starting column
        dr (int): row direction increment
        dc (int): column direction increment
        checker (str): checker symbol to match

    Returns:
        int: number of consecutive checkers in the given direction including start
    """
    rows = len(board)
    cols = len(board[0])
    r, c = start_r, start_c
    count = 0
    while in_bounds(r, c, rows, cols) and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count


def check_win(board, last_r, last_c, checker):
    """
    Check if placing 'checker' at (last_r, last_c) results in a win.
    A win is 4 consecutive checkers horizontally, vertically, or diagonally.

    Args:
        board (list[list[str]]): game board
        last_r (int): row index of last placed checker
        last_c (int): column index of last placed checker
        checker (str): player's checker symbol

    Returns:
        bool: True if this move wins the game, False otherwise
    """
    # Directions to check (pairs of opposite directions):
    # Horizontal: (0, 1) and (0, -1)
    # Vertical: (1, 0) and (-1, 0)
    # Diagonal down-right/up-left: (1, 1) and (-1, -1)
    # Diagonal up-right/down-left: (-1, 1) and (1, -1)
    directions = [
        ((0, 1), (0, -1)),
        ((1, 0), (-1, 0)),
        ((1, 1), (-1, -1)),
        ((-1, 1), (1, -1)),
    ]

    for (dr1, dc1), (dr2, dc2) in directions:
        # Count the current cell once, then extend in both directions and subtract 1 to avoid double counting
        count1 = count_consecutive(board, last_r, last_c, dr1, dc1, checker)
        count2 = count_consecutive(board, last_r, last_c, dr2, dc2, checker)
        total = count1 + count2 - 1
        if total >= WIN_LENGTH:
            return True

    return False


def check_draw(board):
    """
    Check if the board is completely filled (draw condition).

    Args:
        board (list[list[str]]): game board

    Returns:
        bool: True if draw (no spaces left), False otherwise
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def validate_configuration():
    """
    Validate initial configuration constants. Exit with message if invalid.
    """
    if COLS < 1 or COLS > 26:
        print("Error: COLS must be between 1 and 26.")
        sys.exit(1)
    if ROWS < 1:
        print("Error: ROWS must be >= 1.")
        sys.exit(1)
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: NUM_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if NUM_PLAYERS > len(PLAYER_CHECKERS):
        print("Error: Not enough checker symbols defined for the requested number of players.")
        sys.exit(1)


def main():
    """
    Main game loop for Connect 4.
    - Initializes the board and players.
    - Randomly selects a starting player.
    - Alternates turns, handles input, placing checkers, win/draw detection.
    """
    validate_configuration()

    # Initialize board and player checkers
    board = create_board(ROWS, COLS)
    players = PLAYER_CHECKERS[:NUM_PLAYERS]

    # Randomly select starting player index
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial board display
    clear_screen()
    print_board(board)
    print(f"Player {players[current_player_idx]} starts!")

    # Game loop
    while True:
        # Display current state and prompt
        clear_screen()
        print_board(board)
        current_checker = players[current_player_idx]
        print(f"Player {current_checker}, it's your turn.")
        col_idx = get_valid_column_input(COLS)

        # Attempt to place the checker
        placement = drop_checker(board, col_idx, current_checker)
        if placement is None:
            # Column is full: turn is invalid and player loses the turn
            clear_screen()
            print_board(board)
            col_label = chr(ord('A') + col_idx)
            print(f"Column {col_label} is full. Player {current_checker} loses the turn.")
            # Advance to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            # Continue to next turn
            continue

        last_r, last_c = placement

        # Check for win
        if check_win(board, last_r, last_c, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
