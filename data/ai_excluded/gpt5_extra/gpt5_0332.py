import os
import random
import string
import sys

# ---------- Configuration (submission must be 6 rows x 7 columns and 2 players) ----------
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5 inclusive
WIN_LEN = 4

PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]


# ---------- Utility functions ----------
def clear_screen():
    # Clear terminal screen on Unix/Linux/macOS
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Column headers (A..)
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    sep = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep)
    for r in range(rows):
        line = "|"
        for c in range(cols):
            line += f" {board[r][c]} |"
        print(line)
        print(sep)


def is_board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def get_valid_column_input(current_symbol, cols):
    valid_letters = set(string.ascii_uppercase[:cols])

    while True:
        user_in = input(f"Player {current_symbol}, please enter a column: ").strip()
        if len(user_in) != 1:
            print("Invalid input. Enter a single uppercase letter corresponding to a column.")
            continue
        letter = user_in.upper()
        if letter not in valid_letters:
            print("Invalid column. Please enter a valid column letter within the board.")
            continue
        return ord(letter) - ord('A')


def drop_checker(board, col, symbol):
    """
    Drops the checker into the given column.
    Returns the row index where the checker lands, or None if the column is full.
    """
    rows = len(board)
    # Start from bottom row upward
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return r
    return None  # Column full


def check_win_from_cell(board, row, col, symbol):
    """
    Check if placing symbol at (row, col) creates a win of length WIN_LEN.
    We only need to examine lines going through (row, col).
    """
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1  # count the placed checker itself

        # extend in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc

        # extend in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_LEN:
            return True

    return False


def validate_configuration():
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.", file=sys.stderr)
        sys.exit(1)
    if COLS < 1 or COLS > 26:
        print("COLS must be between 1 and 26.", file=sys.stderr)
        sys.exit(1)
    if ROWS < 1:
        print("ROWS must be at least 1.", file=sys.stderr)
        sys.exit(1)


# ---------- Main game ----------
def main():
    validate_configuration()

    board = create_board(ROWS, COLS)
    symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]

    # Randomly choose starting player
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial board display
    clear_screen()
    print_board(board)

    winner = None

    while True:
        current_symbol = symbols[current_player_idx]

        # Ask for a valid column letter (invalid inputs do not lose turn)
        col = get_valid_column_input(current_symbol, COLS)

        # Try to drop checker (if full, turn is invalid and lost)
        row = drop_checker(board, col, current_symbol)
        if row is None:
            print(f"Column {chr(ord('A') + col)} is full. Player {current_symbol} loses the turn.")
            # Move to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            # Show unchanged board for next player
            input("Press Enter to continue...")
            clear_screen()
            print_board(board)
            continue

        # Successful move: update screen
        clear_screen()
        print_board(board)

        # Check for win
        if check_win_from_cell(board, row, col, current_symbol):
            winner = current_symbol
            print(f"Player {winner} won!")
            break

        # Check for draw
        if is_board_full(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

    # Game over
    # No further action required


if __name__ == "__main__":
    main()
