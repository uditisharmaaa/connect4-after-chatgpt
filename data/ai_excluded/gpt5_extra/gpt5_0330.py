import os
import random
import time

# -------------------------
# Constants (adjustable)
# -------------------------
ROWS = 6               # Number of rows (default per submission: 6)
COLS = 7               # Number of columns (default per submission: 7) - max supported: 26
NUM_PLAYERS = 2        # Number of players (2 to 5, default per submission: 2)

# Player checkers in order; use the first NUM_PLAYERS of these
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# -------------------------
# Utility and game functions
# -------------------------

def clear_screen():
    """Clear the terminal screen (Linux/Unix)."""
    os.system('clear')


def create_board(rows, cols):
    """Create a 2D board initialized with spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Print the board with column headers and a grid.
    Example formatting as shown in the assignment.
    """
    rows = len(board)
    cols = len(board[0])

    # Header with letters A.. up to number of columns
    letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(letters))

    # Horizontal separator line
    sep = "+" + "+".join(['---'] * cols) + "+"

    for r in range(rows):
        print(sep)
        # Print each cell with surrounding pipes
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)


def get_players(num_players):
    """Return a list of player checker symbols for the given number of players."""
    if not (2 <= num_players <= 5):
        raise ValueError("Number of players must be between 2 and 5.")
    return CHECKERS[:num_players]


def column_letter_to_index(letter):
    """Convert a column letter (A-Z) to a zero-based column index."""
    return ord(letter) - ord('A')


def is_valid_column_letter(letter, cols):
    """Check if a letter is a valid column within range A..(A+cols-1)."""
    if len(letter) != 1 or not letter.isalpha() or not letter.isupper():
        return False
    idx = column_letter_to_index(letter)
    return 0 <= idx < cols


def find_drop_row(board, col):
    """
    Given a column index, find the row index where the checker would land.
    Returns the row index if available, else returns None if the column is full.
    """
    for r in range(len(board) - 1, -1, -1):  # Start from bottom row upwards
        if board[r][col] == ' ':
            return r
    return None


def drop_checker(board, col, checker):
    """
    Attempt to drop a checker into the given column.
    Returns (row_index, col_index) if placed, or (None, None) if the column is full.
    """
    row = find_drop_row(board, col)
    if row is None:
        return None, None
    board[row][col] = checker
    return row, col


def count_in_direction(board, start_r, start_c, delta_r, delta_c, checker):
    """
    Count how many consecutive 'checker' pieces including the starting cell exist
    along the direction specified by (delta_r, delta_c) and its opposite.
    """
    rows = len(board)
    cols = len(board[0])

    count = 1  # Count the starting position

    # Check one direction
    r, c = start_r + delta_r, start_c + delta_c
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += delta_r
        c += delta_c

    # Check the opposite direction
    r, c = start_r - delta_r, start_c - delta_c
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r -= delta_r
        c -= delta_c

    return count


def check_win_from(board, row, col, checker):
    """
    Check if placing 'checker' at (row, col) creates a win (4 in a row)
    in any direction: horizontal, vertical, or either diagonal.
    """
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    for dr, dc in directions:
        if count_in_direction(board, row, col, dr, dc, checker) >= 4:
            return True
    return False


def is_board_full(board):
    """Return True if the board has no empty spaces, otherwise False."""
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == ' ':
                return False
    return True


def game_loop():
    """Main game loop for Connect 4."""
    # Enforce supported maximum columns (26 for A-Z)
    if COLS > 26:
        raise ValueError("Maximum supported columns is 26 (A-Z).")

    # Initialize
    board = create_board(ROWS, COLS)
    players = get_players(NUM_PLAYERS)

    # Randomly choose starting player
    current_player_idx = random.randrange(len(players))

    # Initial display before game starts
    clear_screen()
    print_board(board)

    # Main turn loop
    while True:
        current_checker = players[current_player_idx]
        last_col_letter = chr(ord('A') + COLS - 1)

        # Prompt for valid column input
        while True:
            user_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
            if is_valid_column_letter(user_input, COLS):
                break
            # Invalid input: prompt again (turn is not lost)
            clear_screen()
            print_board(board)
            print(f"Invalid input. Please enter a column between A and {last_col_letter} (uppercase letters only).")

        col = column_letter_to_index(user_input)

        # Attempt to place checker
        row, col_placed = drop_checker(board, col, current_checker)

        if row is None:
            # Column full: turn is invalid and player loses the turn
            clear_screen()
            print_board(board)
            print(f"Column {user_input} is full. Turn lost.")
            time.sleep(1.2)  # Short pause so player can see the message
            # Move to next player
            current_player_idx = (current_player_idx + 1) % len(players)
            clear_screen()
            print_board(board)
            continue

        # After a valid placement, clear and show updated board
        clear_screen()
        print_board(board)

        # Check for a win from the last placed position
        if check_win_from(board, row, col_placed, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for a draw (board full)
        if is_board_full(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % len(players)


if __name__ == "__main__":
    game_loop()
