import os
import random
import sys

# =========================
# Configuration constants
# =========================
ROWS = 6                  # number of rows (default for submission)
COLS = 7                  # number of columns (default for submission, max 26)
NUM_PLAYERS = 2           # number of players (2 to 5)
TOKENS = ["X", "O", "V", "H", "M"]  # tokens in order, first NUM_PLAYERS are used

# Guard constraints
assert 2 <= NUM_PLAYERS <= 5, "NUM_PLAYERS must be between 2 and 5"
assert 1 <= ROWS, "ROWS must be positive"
assert 1 <= COLS <= 26, "COLS must be between 1 and 26"


def clear_screen():
    """Clear the terminal screen (Linux/Unix)."""
    os.system('clear')


def create_board(rows, cols):
    """Create a 2D board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Print the board with column letter headers and ASCII grid."""
    rows = len(board)
    cols = len(board[0])

    # Header letters
    header_letters = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(header_letters)

    # Horizontal line
    hline = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(hline)
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
    print(hline)


def first_empty_row(board, col):
    """Return the lowest empty row index in column col, or None if full."""
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def drop_checker(board, col, token):
    """
    Place token into column col at the lowest empty position.
    Returns the (row, col) where placed, or None if the column is full.
    """
    r = first_empty_row(board, col)
    if r is None:
        return None
    board[r][col] = token
    return (r, col)


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win(board, token):
    """Check for a win (4 in a row) for token in any direction."""
    rows = len(board)
    cols = len(board[0])
    needed = 4

    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while count < needed and in_bounds(rr, cc, rows, cols) and board[rr][cc] == token:
                    count += 1
                    rr += dr
                    cc += dc
                if count == needed:
                    return True
    return False


def check_draw(board):
    """Return True if no empty spaces remain on the board."""
    for row in board:
        if " " in row:
            return False
    return True


def letter_to_col(letter):
    """Convert column letter (A-Z) to index. Returns index or None."""
    letter = letter.strip().upper()
    if len(letter) != 1 or not letter.isalpha():
        return None
    idx = ord(letter) - ord('A')
    if 0 <= idx < COLS:
        return idx
    return None


def prompt_for_column(current_token):
    """
    Prompt user for a valid column letter in range.
    Invalid inputs (non-letter or out of range) cause a re-prompt (turn not lost).
    Returns the valid column index (int).
    """
    while True:
        try:
            user_input = input(f"Player {current_token}, please enter a column: ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting game.")
            sys.exit(0)

        if len(user_input) != 1:
            print("Invalid input. Please enter a single uppercase letter corresponding to a column.")
            continue

        if not user_input.isalpha():
            print("Invalid input. Please enter a letter (A-Z).")
            continue

        idx = letter_to_col(user_input)
        if idx is None:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + COLS - 1)}.")
            continue

        return idx


def game_loop():
    board = create_board(ROWS, COLS)
    players = TOKENS[:NUM_PLAYERS]

    # Randomly select first player index
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial display
    clear_screen()
    print_board(board)

    while True:
        current_token = players[current_player_idx]

        # Ask for a column letter until it's a valid, in-range letter
        col = prompt_for_column(current_token)

        # Try to drop the checker
        placed = drop_checker(board, col, current_token)

        if placed is None:
            # Column full: player loses the turn
            print(f"Column {chr(ord('A') + col)} is full. Player {current_token} loses the turn.")
            # Next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            # Update display for next turn
            clear_screen()
            print_board(board)
            continue

        # Successful placement: check for win/draw
        r, c = placed

        # Update display
        clear_screen()
        print_board(board)

        if check_win(board, current_token):
            print(f"Player {current_token} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


def main():
    game_loop()


if __name__ == "__main__":
    main()
