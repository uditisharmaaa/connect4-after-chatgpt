import os
import random
import string
import sys

# Constants (adjustable, but submission requires ROWS=6, COLS=7, NUM_PLAYERS=2)
ROWS = 6
COLS = 7  # Max 26 columns because of letter labels A-Z
NUM_PLAYERS = 2  # Supports 2 to 5 players
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checker symbols for up to 5 players
WIN_LENGTH = 4  # Number of checkers in a row to win

# Safety checks for configuration
if not (2 <= NUM_PLAYERS <= 5):
    print("Error: NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if not (1 <= COLS <= 26):
    print("Error: COLS must be between 1 and 26.")
    sys.exit(1)
if ROWS < 1:
    print("Error: ROWS must be at least 1.")
    sys.exit(1)

# The checkers to use based on number of players
PLAYER_CHECKERS = CHECKERS[:NUM_PLAYERS]


def clear_screen():
    """
    Clears the terminal screen. Uses 'clear' as per Linux/Unix specification.
    """
    os.system('clear')


def create_board(rows, cols):
    """
    Creates a 2D list representing the game board initialized with spaces.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Prints the board in the specified format with column labels A, B, C, ...
    """
    clear_screen()

    cols = len(board[0])

    # Header with column letters
    letters = [string.ascii_uppercase[i] for i in range(cols)]
    header = "  " + "   ".join(letters)
    print(header)

    # Horizontal separator for a row
    hsep = "+" + "+".join(["---"] * cols) + "+"

    # Print each row from top to bottom
    for r in range(len(board)):
        print(hsep)
        row_cells = "|" + "|".join(f" {cell} " for cell in board[r]) + "|"
        print(row_cells)
    print(hsep)


def find_row_for_column(board, col):
    """
    Given a column index, returns the row index where the checker would land,
    or None if the column is full.
    """
    rows = len(board)
    # Start from the bottom row and move up to find first empty cell
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def place_checker(board, col, checker):
    """
    Places a checker in the specified column if possible.
    Returns True if placed, False if the column is full.
    """
    row = find_row_for_column(board, col)
    if row is None:
        return False
    board[row][col] = checker
    return True


def in_bounds(r, c, rows, cols):
    """
    Checks if (r, c) is within the board bounds.
    """
    return 0 <= r < rows and 0 <= c < cols


def check_direction(board, start_r, start_c, dr, dc, checker):
    """
    Counts consecutive checkers in a specific direction (dr, dc) starting from (start_r, start_c).
    Returns the total count including the starting position.
    """
    rows, cols = len(board), len(board[0])
    count = 0
    r, c = start_r, start_c
    while in_bounds(r, c, rows, cols) and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count


def is_winning_move(board, last_r, last_c, checker):
    """
    Checks if placing 'checker' at (last_r, last_c) resulted in a win.
    Checks horizontally, vertically, and both diagonal directions.
    """
    # Directions to check: horizontal (0,1), vertical (1,0), diagonal (1,1), anti-diagonal (1,-1)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for dr, dc in directions:
        # Count in positive direction
        count_pos = 0
        r, c = last_r, last_c
        while in_bounds(r, c, len(board), len(board[0])) and board[r][c] == checker:
            count_pos += 1
            r += dr
            c += dc

        # Count in negative direction (excluding the starting cell to avoid double count)
        count_neg = 0
        r, c = last_r - dr, last_c - dc
        while in_bounds(r, c, len(board), len(board[0])) and board[r][c] == checker:
            count_neg += 1
            r -= dr
            c -= dc

        total = count_pos + count_neg
        if total >= WIN_LENGTH:
            return True

    return False


def check_draw(board):
    """
    Returns True if the board is full (no empty spaces), else False.
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def prompt_for_column(current_checker, cols):
    """
    Prompts the user for a column letter. Validates input type and range.
    Returns a 0-based column index when valid.
    Keeps prompting on invalid input (non-letter, out of range).
    Note: If the user enters a valid letter but the column is full, the caller handles losing the turn.
    """
    while True:
        user_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()

        # Validate single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter corresponding to a column.")
            continue

        # Validate letter and range
        if user_input < 'A' or ord(user_input) >= ord('A') + cols:
            print("Invalid column. Please enter a valid column letter shown at the top.")
            continue

        col_index = ord(user_input) - ord('A')
        return col_index


def find_last_placed_row(board, col):
    """
    Finds the topmost occupied cell in the given column and returns its row index.
    Useful to determine the coordinates of the last placed checker.
    Assumes that the column is not empty (should be called right after placing).
    """
    for r in range(len(board)):
        if board[r][col] != " ":
            return r
    return None


def game_loop():
    """
    Main game loop: initializes the board, selects a random starting player,
    alternates turns, accepts input, places checkers, checks for wins and draw.
    """
    board = create_board(ROWS, COLS)

    # Randomly select first player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Initial board display
    print_board(board)

    # Game continues until a win or a draw
    while True:
        current_checker = PLAYER_CHECKERS[current_player_idx]

        # Check for draw before asking input (board might already be full)
        if check_draw(board):
            print("The game is a draw!")
            break

        # Show prompt under the current printed board
        col = prompt_for_column(current_checker, COLS)

        # Attempt to place checker
        placed = place_checker(board, col, current_checker)

        # Update screen and board view after the attempt
        print_board(board)

        if not placed:
            # Column is full; lose the turn without reprompt
            print(f"Column {chr(ord('A') + col)} is full. Player {current_checker} loses the turn.")
            # Switch to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Determine the row where the checker was placed to check for a win efficiently
        placed_row = find_last_placed_row(board, col)

        # Check for a win
        if placed_row is not None and is_winning_move(board, placed_row, col, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw after a valid move
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    game_loop()
