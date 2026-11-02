import os
import random
import string
import sys

# =========================
# Configuration (constants)
# =========================
ROWS = 6            # Number of rows (e.g., 6)
COLS = 7            # Number of columns (e.g., 7). Must be <= 26 for letter labels.
NUM_PLAYERS = 2     # Number of players (between 2 and 5 inclusive)

PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # In order, as specified (max 5 players)
WIN_LENGTH = 4      # Number of checkers in a row needed to win (always 4 per spec)
MAX_COLS = 26       # Maximum columns supported due to letter labels (A-Z)


# =========================
# Utility and game helpers
# =========================
def clear_screen():
    """
    Clear the terminal screen (Linux/Unix).
    """
    os.system('clear')


def create_board(rows, cols):
    """
    Create a 2D game board initialized with spaces.
    Returns: list of lists (rows x cols) filled with ' '.
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Print the board to match the specified format:
      - Column headers are letters starting at 'A'
      - Grid lines with +---+ and cells with | X |
    """
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Print column headers
    headers = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(headers))

    # Print top border and each row
    horizontal = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(horizontal)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(horizontal)


def col_letter_to_index(letter):
    """
    Convert a column letter ('A'..'Z') to a 0-based index.
    """
    return ord(letter) - ord('A')


def is_valid_column_letter(letter, cols):
    """
    Validate that the input is a single letter within the current board column range.
    """
    if len(letter) != 1:
        return False
    if letter < 'A' or letter > chr(ord('A') + cols - 1):
        return False
    return True


def get_valid_input(cols, current_symbol):
    """
    Prompt the user for a valid column letter input.
    Keeps asking until a valid input is provided (does not lose turn on invalid input).
    Returns the 0-based column index.
    """
    while True:
        user_input = input(f"Player {current_symbol}, please enter a column: ").strip().upper()
        if not user_input:
            print("Invalid input: empty. Please enter a letter corresponding to a column.")
            continue
        if not user_input.isalpha() or len(user_input) != 1:
            print("Invalid input: please enter a single letter (e.g., A, B, C...).")
            continue
        if not is_valid_column_letter(user_input, cols):
            valid_range = f"A to {chr(ord('A') + cols - 1)}"
            print(f"Invalid column: please enter a letter from {valid_range}.")
            continue
        return col_letter_to_index(user_input)


def column_is_full(board, col):
    """
    Check if a given column is completely full.
    """
    return board[0][col] != ' '


def drop_checker(board, col, symbol):
    """
    Drop a checker with 'symbol' into column 'col', occupying the lowest available cell.
    Assumes the column is not full.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = symbol
            return r, col  # Return the position where the checker was placed
    # Should not reach here if called only when column is not full.
    return None


def check_win(board, symbol):
    """
    Check whether the given 'symbol' has achieved WIN_LENGTH in a row in any direction.
    Directions: horizontal, vertical, diagonal down-right, diagonal up-right.
    """
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
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
                    if count >= WIN_LENGTH:
                        return True
                    rr += dr
                    cc += dc
    return False


def check_draw(board):
    """
    A draw occurs when the board is completely filled with no spaces remaining.
    """
    for row in board:
        if ' ' in row:
            return False
    return True


def assert_configuration():
    """
    Ensure that the configured constants are valid for the game constraints.
    """
    if COLS < 1 or COLS > MAX_COLS:
        print(f"Error: COLS must be between 1 and {MAX_COLS}. Current: {COLS}")
        sys.exit(1)
    if ROWS < 1:
        print("Error: ROWS must be at least 1.")
        sys.exit(1)
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Error: NUM_PLAYERS must be between 2 and 5 (inclusive).")
        sys.exit(1)
    if NUM_PLAYERS > len(PLAYER_SYMBOLS):
        print("Error: Not enough player symbols configured.")
        sys.exit(1)


def main():
    # Validate configuration
    assert_configuration()

    # Prepare game
    symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    # Randomly select the starting player
    current_player_index = random.randrange(NUM_PLAYERS)

    # Initial render before the game starts
    clear_screen()
    print_board(board)

    # Main game loop
    while True:
        current_symbol = symbols[current_player_index]

        # Get a valid column letter from the player
        col = get_valid_input(COLS, current_symbol)

        # If column is full, player loses the turn
        if column_is_full(board, col):
            # Render unchanged board and switch player
            clear_screen()
            print_board(board)
            # Player loses turn; move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        # Place the checker
        drop_checker(board, col, current_symbol)

        # After placing, clear and print updated board
        clear_screen()
        print_board(board)

        # Check for a win
        if check_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check for a draw
        if check_draw(board):
            print("Game is a draw.")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
