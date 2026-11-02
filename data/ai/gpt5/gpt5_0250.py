import os
import random
import string
import sys

# ===========================
# Constants (feel free to change to test; submission requires 6x7 and 2 players)
# ===========================
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Supports 2 to 5 players
CHECKERS = ["X", "O", "V", "H", "M"]  # In order of assignment requirement
WIN_LENGTH = 4  # Always 4, regardless of board size or #players

# ===========================
# Utility functions
# ===========================

def clear_screen():
    """
    Clears the terminal screen (Linux/Unix).
    """
    os.system('clear')


def create_board(rows, cols):
    """
    Creates a 2D board initialized with spaces.
    Board is a list of lists: board[row][col]
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Prints the board in the format specified in the assignment.
    Columns are labeled A, B, C, ...
    """
    rows = len(board)
    cols = len(board[0])

    # Header letters
    header_letters = []
    for c in range(cols):
        header_letters.append(f"  {string.ascii_uppercase[c]}  ")
    print("".join(header_letters))

    # Horizontal separator
    sep = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(f"| {board[r][c]} ")
        print("".join(row_cells) + "|")
    print(sep)


def col_from_input(inp):
    """
    Converts user input (a single uppercase letter) to a column index.
    Returns None if invalid.
    """
    if len(inp) != 1:
        return None
    if inp not in string.ascii_uppercase:
        return None
    idx = ord(inp) - ord('A')
    if idx < 0 or idx >= COLS:
        return None
    return idx


def get_valid_input(current_checker):
    """
    Prompts the current player for input until a syntactically valid column letter is given.
    Does not check if the column is full here (that's handled during placement).
    Returns a valid column index (int).
    """
    while True:
        try:
            user_in = input(f"Player {current_checker}, please enter a column: ").strip().upper()
        except EOFError:
            # If input stream closes, exit gracefully
            print("\nInput closed. Exiting game.")
            sys.exit(0)
        except KeyboardInterrupt:
            print("\nGame interrupted by user.")
            sys.exit(0)

        col = col_from_input(user_in)
        if col is None:
            # Invalid input: not a single valid letter or out of range
            print("Invalid input. Please enter a valid column letter (e.g., A, B, C).")
            continue
        return col


def drop_checker(board, col, checker):
    """
    Attempts to drop the checker into the given column.
    Returns the row index where it lands, or None if the column is full.
    """
    rows = len(board)
    # Start from the bottom row and find the first empty space going upwards
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return None  # Column is full


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win_from_cell(board, start_r, start_c, checker):
    """
    Checks if placing 'checker' at (start_r, start_c) results in a win.
    Checks 4 directions: horizontal, vertical, and two diagonals.
    """
    rows = len(board)
    cols = len(board[0])

    # Directions: (dr, dc)
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # Count the starting cell

        # Look forward in direction (dr, dc)
        r, c = start_r + dr, start_c + dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Look backward in direction (-dr, -dc)
        r, c = start_r - dr, start_c - dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_LENGTH:
            return True

    return False


def is_draw(board):
    """
    Returns True if the board is full (no spaces in top row of any column).
    """
    top_row = board[0]
    return all(cell != " " for cell in top_row)


def select_players(num_players):
    """
    Returns a list of checker symbols for the given number of players.
    Supports between 2 and 5 players as required.
    """
    if not (2 <= num_players <= 5):
        raise ValueError("Number of players must be between 2 and 5.")
    return CHECKERS[:num_players]


# ===========================
# Game loop
# ===========================

def main():
    # Ensure column constraint
    if COLS > 26:
        raise ValueError("Maximum number of columns is 26 (A-Z).")

    # Initialize board and players
    board = create_board(ROWS, COLS)
    players = select_players(NUM_PLAYERS)

    # Randomly select the starting player index
    current_index = random.randint(0, len(players) - 1)

    # Initial display
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        current_checker = players[current_index]

        # Get valid input (only syntactically valid column letter)
        col = get_valid_input(current_checker)

        # Attempt to drop the checker; if column full, turn is lost
        row = drop_checker(board, col, current_checker)
        clear_screen()
        if row is None:
            print_board(board)
            # Inform about losing the turn due to full column
            print(f"Column {string.ascii_uppercase[col]} is full. Player {current_checker} loses the turn.")
            # Move to next player
            current_index = (current_index + 1) % len(players)
            # Continue to next turn without win/draw check
            continue

        # Print the updated board
        print_board(board)

        # Check for a win from the last placed position
        if check_win_from_cell(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_index = (current_index + 1) % len(players)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
        sys.exit(0)
