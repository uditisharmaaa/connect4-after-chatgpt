import os
import random
import sys

# Constants (adjustable)
ROWS = 6            # Number of rows (default per assignment: 6)
COLS = 7            # Number of columns (default per assignment: 7), max 26
NUM_PLAYERS = 2     # Number of players (2 to 5)

# Player checker symbols in order; first NUM_PLAYERS are used
CHECKERS = ["X", "O", "V", "H", "M"]

# Safety checks for configuration
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if not (1 <= COLS <= 26):
    print("COLS must be between 1 and 26.")
    sys.exit(1)
if ROWS < 1:
    print("ROWS must be at least 1.")
    sys.exit(1)


def clear_screen():
    """Clear the terminal screen (Unix/Linux/macOS)."""
    os.system('clear')


def create_board(rows, cols):
    """Create a rows x cols board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board, message=None, current_symbol=None):
    """
    Print the board in the specified ASCII-art format.
    Optionally print a message and prompt line for the current player.
    """
    rows = len(board)
    cols = len(board[0])

    # Header letters A.. up to number of columns
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    sep = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
        print(sep)

    if message:
        print(message)
    if current_symbol is not None:
        print(f"Player {current_symbol}, please enter a column:")


def col_letter_to_index(letter):
    """Convert a column letter (A..Z) to zero-based index."""
    return ord(letter) - ord('A')


def is_valid_column_input(text, cols):
    """
    Validate user input for a column:
    - Single alphabetic character
    - Within the range of existing columns
    Returns (True, index) or (False, None)
    """
    if not text:
        return False, None
    s = text.strip()
    if len(s) != 1 or not s.isalpha():
        return False, None
    s = s.upper()
    idx = col_letter_to_index(s)
    if 0 <= idx < cols:
        return True, idx
    return False, None


def drop_checker(board, col, symbol):
    """
    Attempt to drop 'symbol' into column 'col'.
    Returns the row index where the checker lands, or None if the column is full.
    """
    rows = len(board)
    # Start from bottom-most row up to top
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return r
    return None  # Column is full


def check_win(board, symbol):
    """
    Check if 'symbol' has 4 in a row in any direction on the board.
    Returns True if win; otherwise False.
    """
    rows = len(board)
    cols = len(board[0])
    in_a_row = 4

    # Directions: (dr, dc)
    directions = [
        (0, 1),    # horizontal right
        (1, 0),    # vertical down
        (1, 1),    # diagonal down-right
        (1, -1),   # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == symbol:
                    count += 1
                    if count == in_a_row:
                        return True
                    rr += dr
                    cc += dc
    return False


def check_draw(board):
    """
    Check if the game is a draw: board is full (no spaces).
    Returns True if draw; otherwise False.
    """
    # If top row has no spaces in any column, the board is full
    return all(cell != " " for cell in board[0])


def main():
    # Initialize game
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select the starting player
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial render
    clear_screen()
    print_board(board)

    last_message = None

    # Main game loop
    while True:
        current_symbol = players[current_player_idx]

        # Render board with optional message and prompt
        clear_screen()
        print_board(board, message=last_message, current_symbol=current_symbol)
        last_message = None  # Clear message after showing it once

        # Get valid input (does not lose turn on invalid input)
        col_index = None
        while True:
            user_input = input().strip()
            valid, idx = is_valid_column_input(user_input, COLS)
            if valid:
                col_index = idx
                break
            else:
                # Re-render with error and prompt again for same player
                clear_screen()
                print_board(board, message="Invalid input. Please enter a valid column letter.", current_symbol=current_symbol)

        # Try to drop checker (lose turn if column is full)
        row_landed = drop_checker(board, col_index, current_symbol)
        if row_landed is None:
            last_message = f"Column {chr(ord('A') + col_index)} is full. Turn lost."
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Check for win
        if check_win(board, current_symbol):
            clear_screen()
            print_board(board)
            print(f"Player {current_symbol} won!")
            break

        # Check for draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
