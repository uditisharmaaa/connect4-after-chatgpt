import os
import random
import string

# =========================
# Configuration (Constants)
# =========================
# Submission must be 6 rows x 7 columns and 2 players by default.
ROWS = 6
COLS = 7            # Max 26 (columns labeled A-Z)
NUM_PLAYERS = 2     # Supported: 2 to 5 players inclusive
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LEN = 4         # Number of checkers in a row required to win (fixed at 4)

# =========================
# Validations for constants
# =========================
assert 2 <= NUM_PLAYERS <= 5, "NUM_PLAYERS must be between 2 and 5."
assert 1 <= ROWS, "ROWS must be at least 1."
assert 1 <= COLS <= 26, "COLS must be between 1 and 26."
PLAYER_SYMBOLS = CHECKERS[:NUM_PLAYERS]


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')


def create_board(rows, cols):
    """Create a board with the given dimensions filled with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """
    Print the board in the required format:
      A   B   C ...
    +---+---+---+
    |   |   |   |
    +---+---+---+
    ...
    """
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header with column letters
    letters = list(string.ascii_uppercase[:cols])
    print("  " + "   ".join(letters))

    # Horizontal border line
    hline = "+" + ("---+" * cols)

    for r in range(rows):
        print(hline)
        # Row content
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("|" + "|".join(f" {cell} " for cell in row_cells) + "|")
    print(hline)


def col_from_input(s):
    """
    Convert a single uppercase letter (A..Z) to a 0-based column index.
    Return None if invalid or out of range for current board.
    """
    if len(s) != 1 or not s.isalpha() or not s.isupper():
        return None
    idx = ord(s) - ord('A')
    if 0 <= idx < COLS:
        return idx
    return None


def drop_checker(board, col, checker):
    """
    Drop a checker into the given column.
    The checker occupies the lowest available space in the column.
    Returns the row index where the checker lands, or None if the column is full.
    """
    # Start from bottom row going upwards
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return None  # Column full


def in_bounds(r, c):
    """Check if (r, c) is within the board."""
    return 0 <= r < ROWS and 0 <= c < COLS


def count_direction(board, start_r, start_c, dr, dc, checker):
    """
    Count consecutive checkers equal to 'checker' starting from (start_r, start_c),
    moving in direction (dr, dc), including the starting cell.
    """
    r, c = start_r, start_c
    count = 0
    while in_bounds(r, c) and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count


def check_win(board, last_r, last_c, checker):
    """
    Check if placing a checker at (last_r, last_c) results in a win for 'checker'.
    A win is 4 in a row horizontally, vertically, or diagonally.
    """
    directions = [
        (0, 1),   # Horizontal (right)
        (1, 0),   # Vertical (down)
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]

    for dr, dc in directions:
        # Count both directions from the last placed checker
        total = (
            count_direction(board, last_r, last_c, dr, dc, checker) +
            count_direction(board, last_r, last_c, -dr, -dc, checker) - 1
        )
        if total >= WIN_LEN:
            return True
    return False


def is_draw(board):
    """Check if the board is full (no spaces left)."""
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True


def main():
    # Initialize board
    board = create_board(ROWS, COLS)

    # Randomly select the starting player index
    current_player = random.randrange(NUM_PLAYERS)

    # Show initial board
    clear_screen()
    print_board(board)

    # Game loop
    while True:
        checker = PLAYER_SYMBOLS[current_player]
        # Prompt until valid input (except full column causes turn loss)
        while True:
            try:
                user_input = input(f"Player {checker}, please enter a column: ").strip()
            except EOFError:
                # If input stream ends unexpectedly, exit gracefully
                print()
                return

            # Convert to uppercase and validate
            user_input = user_input.upper()
            col = col_from_input(user_input)
            if col is None:
                print("Invalid input. Enter a single uppercase letter within the board (e.g., A, B, C).")
                continue

            # Valid column letter provided; attempt to drop checker
            drop_row = drop_checker(board, col, checker)
            if drop_row is None:
                # Column full: turn is invalid and player loses the turn
                print(f"Column {user_input} is full. Turn lost.")
                # Before switching turns, show the board unchanged as "updated" state
                clear_screen()
                print_board(board)
                # Switch to next player
                current_player = (current_player + 1) % NUM_PLAYERS
            else:
                # Successful move: clear screen and print updated board
                clear_screen()
                print_board(board)

                # Check for a win
                if check_win(board, drop_row, col, checker):
                    print(f"Player {checker} won!")
                    return

                # Check for draw
                if is_draw(board):
                    print("Game is a draw!")
                    return

                # Switch to next player
                current_player = (current_player + 1) % NUM_PLAYERS

            # Break the input loop after either losing the turn (full column) or successful move.
            break


if __name__ == "__main__":
    main()
