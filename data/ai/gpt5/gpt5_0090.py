import os
import random
import sys

# Constants (you can adjust these for testing; submission should be 6x7 and 2 players)
ROWS = 6
COLS = 7  # Max 26 (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5
TOKENS = ['X', 'O', 'V', 'H', 'M']  # Player tokens in order
CONNECT_N = 4  # Number of checkers needed to win

# Validate constants
if not (2 <= NUM_PLAYERS <= 5):
    print("Error: NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if not (1 <= COLS <= 26):
    print("Error: COLS must be between 1 and 26.")
    sys.exit(1)

if ROWS < 1:
    print("Error: ROWS must be at least 1.")
    sys.exit(1)


def clear_screen():
    """Clear the terminal screen (Unix/Linux/Mac)."""
    os.system('clear')


def create_board(rows, cols):
    """Create a board as a list of lists initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_label(index):
    """Convert zero-based column index to uppercase letter label (0 -> 'A')."""
    return chr(ord('A') + index)


def print_board(board):
    """
    Print the board to stdout in the required format.
    Example:
      A   B   C ...
    +---+---+---...
    |   | X |   ...
    ...
    """
    rows = len(board)
    cols = len(board[0]) if rows else 0

    # Print header with column letters
    header = "  " + "   ".join(column_label(c) for c in range(cols))
    sep = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep)
    for r in range(rows):
        row_str = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row_str)
        print(sep)


def get_valid_column_input(current_token, num_cols):
    """
    Prompt the user for a column letter.
    Keeps asking until input is a single letter A.. corresponding to a valid column index.
    Returns the zero-based column index.
    """
    while True:
        user_input = input(f"Player {current_token}, please enter a column: ").strip().upper()
        if len(user_input) != 1:
            print("Invalid input. Please enter a single uppercase letter corresponding to a column.")
            continue
        ch = user_input[0]
        if not ('A' <= ch <= 'Z'):
            print("Invalid input. Please enter a letter A-Z.")
            continue
        col_index = ord(ch) - ord('A')
        if not (0 <= col_index < num_cols):
            print("Invalid column. Please enter a letter between A and " + column_label(num_cols - 1) + ".")
            continue
        return col_index


def find_row_for_col(board, col):
    """
    Find the lowest available row index in the given column.
    Returns the row index where the checker should be placed, or None if the column is full.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def place_checker(board, row, col, token):
    """Place the token at the specified row and column."""
    board[row][col] = token


def check_win(board, token):
    """
    Check if the given token has a winning sequence of CONNECT_N
    horizontally, vertically, or diagonally.
    """
    rows = len(board)
    cols = len(board[0]) if rows else 0
    n = CONNECT_N

    # Directions: right, down, down-right, down-left
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                end_r = r + (n - 1) * dr
                end_c = c + (n - 1) * dc
                if 0 <= end_r < rows and 0 <= end_c < cols:
                    win = True
                    for k in range(n):
                        rr = r + k * dr
                        cc = c + k * dc
                        if board[rr][cc] != token:
                            win = False
                            break
                    if win:
                        return True
    return False


def board_full(board):
    """Return True if there are no empty spaces left on the board."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def game_loop():
    """Main game loop handling turn order, input, moves, win/draw detection, and display."""
    board = create_board(ROWS, COLS)

    # Determine players' tokens based on NUM_PLAYERS
    players = TOKENS[:NUM_PLAYERS]

    # Randomly select first player
    current_index = random.randrange(NUM_PLAYERS)

    # Show initial empty board
    clear_screen()
    print_board(board)

    while True:
        current_token = players[current_index]

        # Get a valid column input (format and range validation only)
        col = get_valid_column_input(current_token, COLS)

        # Attempt to place the checker
        row = find_row_for_col(board, col)
        if row is None:
            # Column is full: invalid turn, player loses the turn
            clear_screen()
            print_board(board)
            print(f"Column {column_label(col)} is full. Player {current_token} loses the turn.")
            # Next player's turn
            current_index = (current_index + 1) % NUM_PLAYERS
            continue

        # Place the checker
        place_checker(board, row, col, current_token)

        # After placing, check for win or draw
        if check_win(board, current_token):
            clear_screen()
            print_board(board)
            print(f"Player {current_token} won!")
            break

        if board_full(board):
            clear_screen()
            print_board(board)
            print("Game is a draw!")
            break

        # Next player's turn
        current_index = (current_index + 1) % NUM_PLAYERS

        # Print updated board for next turn
        clear_screen()
        print_board(board)


if __name__ == "__main__":
    game_loop()
