import os
import random
import string
import sys

# ---------------------------
# Configuration (constants)
# ---------------------------

# Board dimensions (rows x cols). Assignment requires submission with 6x7.
ROWS = 6
COLS = 7  # Maximum allowed by spec is 26 columns
WIN_RUN = 4  # Number in a row to win (fixed at 4 per spec)

# Number of players (between 2 and 5). Submission requires 2 players enabled.
NUM_PLAYERS = 2

# Player checker symbols in order. First NUM_PLAYERS are used.
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]


# ---------------------------
# Utility functions
# ---------------------------

def clear_screen():
    """
    Clear the terminal screen (Linux/Unix).
    """
    try:
        os.system('clear')
    except Exception:
        # Fallback to printing newlines if clearing fails
        print("\n" * 100)


def create_board(rows, cols):
    """
    Create a 2D Connect 4 board initialized with spaces.
    Board is represented as a list of rows, each row is a list of cells.
    """
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Print the board in the required ASCII format.
    Columns are labeled A, B, C, ...
    Rows are printed top to bottom with grid lines.
    """
    rows = len(board)
    cols = len(board[0])

    # Header with column letters
    header_letters = [string.ascii_uppercase[i] for i in range(cols)]
    header = "  " + "   ".join(header_letters)
    print(header)

    # Horizontal separator line
    sep = "+" + "+".join(["---"] * cols) + "+"

    # Print each row
    for r in range(rows):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c] if board[r][c] != "" else " ")
        print("| " + " | ".join(row_cells) + " |")
    print(sep)


def column_letter_to_index(letter):
    """
    Convert a column letter (A-Z) to a zero-based index.
    Returns None if not a valid uppercase letter A-Z.
    """
    if len(letter) != 1 or letter not in string.ascii_uppercase:
        return None
    return ord(letter) - ord('A')


def get_column_input(num_cols, current_player_symbol):
    """
    Prompt the user for a column letter. Validate input strictly:
    - Must be a single letter corresponding to a column within the board.
    - Accept lowercase by converting to uppercase.
    Keeps prompting until valid input is provided.
    Returns the zero-based column index.
    """
    while True:
        try:
            user_input = input(f"Player {current_player_symbol}, please enter a column: ").strip()
        except EOFError:
            # If input stream is closed, exit gracefully
            print("\nInput stream closed. Exiting game.")
            sys.exit(0)

        if not user_input:
            print("Invalid input. Please enter a column letter.")
            continue

        letter = user_input[0].upper()
        idx = column_letter_to_index(letter)
        if idx is None:
            print("Invalid input. Please enter a single letter (A-Z).")
            continue
        if idx < 0 or idx >= num_cols:
            print(f"Out of bounds. Please enter a letter between A and {string.ascii_uppercase[num_cols - 1]}.")
            continue

        return idx


def place_checker(board, col_index, symbol):
    """
    Place a checker with 'symbol' in the specified column (col_index).
    The checker falls to the lowest available row.
    Returns the row index where the checker was placed.
    If the column is full, returns None.
    """
    rows = len(board)
    # Start from bottom row and move upward
    for r in range(rows - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = symbol
            return r
    return None  # Column full


def check_direction(board, start_r, start_c, dr, dc, symbol):
    """
    Check a run of WIN_RUN cells in a specific direction (dr, dc)
    starting from (start_r, start_c) for the given symbol.
    Returns True if all cells match the symbol, else False.
    """
    rows = len(board)
    cols = len(board[0])
    for k in range(WIN_RUN):
        r = start_r + dr * k
        c = start_c + dc * k
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if board[r][c] != symbol:
            return False
    return True


def check_win(board, symbol):
    """
    Check if the given symbol has a winning sequence of WIN_RUN
    horizontally, vertically, or diagonally.
    """
    rows = len(board)
    cols = len(board[0])

    # Directions: right, down, down-right, down-left
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                if check_direction(board, r, c, dr, dc, symbol):
                    return True
    return False


def check_draw(board):
    """
    A draw occurs when the board is full (no spaces left) and no player has won.
    """
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def select_starting_player(num_players):
    """
    Randomly select the starting player's index [0..num_players-1].
    """
    return random.randint(0, num_players - 1)


def build_player_list(num_players):
    """
    Build the list of player symbols based on NUM_PLAYERS.
    """
    assert 2 <= num_players <= 5, "Number of players must be between 2 and 5."
    return PLAYER_SYMBOLS[:num_players]


# ---------------------------
# Main game loop
# ---------------------------

def main():
    # Validate configuration
    if COLS > 26:
        raise ValueError("Maximum number of columns is 26 (A-Z).")
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        raise ValueError("Number of players must be between 2 and 5.")

    # Initialize board and players
    board = create_board(ROWS, COLS)
    players = build_player_list(NUM_PLAYERS)

    # Random starting player
    current_idx = select_starting_player(NUM_PLAYERS)

    # Show initial empty board
    clear_screen()
    print_board(board)
    print(f"Player {players[current_idx]} starts.")

    # Game loop
    while True:
        # Prompt the current player for a move
        player_symbol = players[current_idx]

        # Get valid input (column in range)
        col_index = get_column_input(COLS, player_symbol)

        # Attempt to place the checker
        row_index = place_checker(board, col_index, player_symbol)

        # Clear screen and print the board after the move attempt
        clear_screen()

        # If column is full, the turn is invalid and the player loses the turn
        if row_index is None:
            print_board(board)
            col_letter = string.ascii_uppercase[col_index]
            print(f"Column {col_letter} is full. Player {player_symbol} loses the turn.")
            try:
                input("Press Enter to continue...")
            except EOFError:
                pass
            # Next player
            current_idx = (current_idx + 1) % NUM_PLAYERS
            continue

        # Valid placement: update and show board
        print_board(board)

        # Check for a win
        if check_win(board, player_symbol):
            print(f"Player {player_symbol} won!")
            break

        # Check for a draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
