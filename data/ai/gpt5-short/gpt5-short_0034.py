import os
import random

# -----------------------------
# Configuration constants
# -----------------------------
ROWS = 6
COLS = 7
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]  # ['A','B','C','D','E','F','G']

# Player symbols in turn order. Use the first NUM_PLAYERS of these.
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

# Set how many players will play (must be between 2 and 5 inclusive).
NUM_PLAYERS = 2  # Change to 3, 4, or 5 as desired

# Command to clear the screen (as requested)
CLEAR_CMD = 'clear'


# -----------------------------
# Helper functions
# -----------------------------
def clear_screen():
    """Clear the console screen."""
    os.system(CLEAR_CMD)


def make_board():
    """Create an empty ROWS x COLS board filled with spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board, current_player_symbol=None):
    """
    Print the board to the console with column labels.
    Optionally show whose turn it is.
    """
    if current_player_symbol is not None:
        print(f"Connect 4 - {ROWS}x{COLS}    Players: {', '.join(PLAYER_SYMBOLS[:NUM_PLAYERS])}")
        print(f"Current turn: {current_player_symbol}")
    else:
        print(f"Connect 4 - {ROWS}x{COLS}")

    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    print("+" + "---+" * COLS)

    # Print each row
    for r in range(ROWS):
        row_cells = []
        for c in range(COLS):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + "---+" * COLS)


def letter_to_col(letter):
    """
    Convert a column letter (A-G) to a column index (0-6).
    Return None if invalid.
    """
    letter = letter.upper()
    if letter in COLUMN_LABELS:
        return ord(letter) - ord('A')
    return None


def is_column_full(board, col):
    """Return True if the given column is full (no spaces)."""
    return board[0][col] != ' '  # Top cell occupied means column is full


def drop_piece(board, col, symbol):
    """
    Drop the symbol into the given column.
    Returns the (row, col) where the piece lands, or None if the column is full.
    """
    if is_column_full(board, col):
        return None

    # Start from bottom row and find the first empty cell going upward
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = symbol
            return (r, col)
    return None  # Shouldn't reach here because we already checked full


def in_bounds(r, c):
    """Check if a (row, col) is within the board."""
    return 0 <= r < ROWS and 0 <= c < COLS


def check_win(board, r, c, symbol):
    """
    Check if placing 'symbol' at (r, c) wins the game.
    We check 4 directions: horizontal, vertical, and two diagonals.
    """
    # Directions to check: (dr, dc)
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # Count the placed piece itself

        # Extend in the positive direction
        rr, cc = r + dr, c + dc
        while in_bounds(rr, cc) and board[rr][cc] == symbol:
            count += 1
            rr += dr
            cc += dc

        # Extend in the negative direction
        rr, cc = r - dr, c - dc
        while in_bounds(rr, cc) and board[rr][cc] == symbol:
            count += 1
            rr -= dr
            cc -= dc

        if count >= 4:
            return True

    return False


def is_draw(board):
    """Return True if the board is full (no moves left)."""
    # If the top row has any spaces, the game is not a draw yet
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True


def get_valid_move(board, symbol):
    """
    Prompt the current player for a valid column letter.
    Validate input and ensure the column is not full.
    Returns the column index (0-6).
    """
    while True:
        move = input(f"Player {symbol}, choose a column (A-{COLUMN_LABELS[-1]}): ").strip().upper()

        # Basic validation: must be a single letter in A-G
        if len(move) != 1:
            print("Please enter exactly one letter.")
            continue

        col = letter_to_col(move)
        if col is None:
            print(f"Invalid column. Please enter a letter from A to {COLUMN_LABELS[-1]}.")
            continue

        if is_column_full(board, col):
            print("That column is full. Choose a different column.")
            continue

        return col


def validate_player_count():
    """
    Ensure NUM_PLAYERS is between 2 and 5 and not more than available symbols.
    Raises ValueError if configuration is invalid.
    """
    if not (2 <= NUM_PLAYERS <= 5):
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    if NUM_PLAYERS > len(PLAYER_SYMBOLS):
        raise ValueError("Not enough player symbols provided for NUM_PLAYERS.")


# -----------------------------
# Main game loop
# -----------------------------
def main():
    # Validate configuration
    validate_player_count()

    # Prepare players and board
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    board = make_board()

    # Pick a random starting player index
    current_index = random.randrange(len(players))

    # Game loop
    while True:
        clear_screen()
        print_board(board, current_player_symbol=players[current_index])

        # Get a valid move from the current player
        col = get_valid_move(board, players[current_index])

        # Drop the piece into the chosen column
        pos = drop_piece(board, col, players[current_index])
        if pos is None:
            # This should not happen because we validated the column,
            # but handle it defensively.
            print("Unexpected error: column is full. Try again.")
            input("Press Enter to continue...")
            continue

        r, c = pos

        # Check for win
        if check_win(board, r, c, players[current_index]):
            clear_screen()
            print_board(board)
            print(f"Player {players[current_index]} wins! Congratulations!")
            break

        # Check for draw
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! No more moves available.")
            break

        # Next player's turn
        current_index = (current_index + 1) % len(players)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C
        print("\nGame aborted.")
