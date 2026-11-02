import os
import random
import sys

# Constants (adjustable, but submission should use 6x7 and 2 players)
ROWS = 6
COLS = 7      # Maximum 26 (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5

# Player checkers in order
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# Safety checks for constraints
assert 2 <= NUM_PLAYERS <= 5, "NUM_PLAYERS must be between 2 and 5"
assert 1 <= ROWS, "ROWS must be at least 1"
assert 1 <= COLS <= 26, "COLS must be between 1 and 26"

# Derived values
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLS)]
ACTIVE_CHECKERS = PLAYER_CHECKERS[:NUM_PLAYERS]


def clear_screen():
    """Clear the terminal screen (Linux/Unix)."""
    os.system('clear')


def create_board(rows, cols):
    """Create a rows x cols board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Print the board with column labels as specified."""
    rows = len(board)
    cols = len(board[0])

    # Header with column letters
    header = "  " + "   ".join(COLUMN_LABELS[:cols])
    sep = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print(sep)


def find_lowest_empty_row(board, col):
    """Return the lowest available row index in the given column, or None if full."""
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def drop_checker(board, col, checker):
    """
    Place a checker in the given column.
    Returns row index if placed, or None if the column is full.
    """
    r = find_lowest_empty_row(board, col)
    if r is None:
        return None
    board[r][col] = checker
    return r


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win_from_cell(board, r, c, dr, dc, checker):
    """
    Check 4 in a row starting at (r, c) moving by (dr, dc) direction.
    Returns True if exactly 4 consecutive checkers found.
    """
    rows = len(board)
    cols = len(board[0])
    for i in range(4):
        rr = r + dr * i
        cc = c + dc * i
        if not in_bounds(rr, cc, rows, cols) or board[rr][cc] != checker:
            return False
    return True


def check_win(board, checker):
    """Check for any 4-in-a-row for the given checker on the board."""
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                if check_win_from_cell(board, r, c, dr, dc, checker):
                    return True
    return False


def check_draw(board):
    """Return True if the board has no empty spaces."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def prompt_for_column(current_checker):
    """
    Prompt the current player for a column letter.
    Validate input format (must be uppercase letter within board columns).
    Returns the zero-based column index.
    """
    while True:
        try:
            user_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
        except EOFError:
            # Treat EOF as quit
            print("\nInput closed. Exiting game.")
            sys.exit(0)
        except KeyboardInterrupt:
            print("\nGame interrupted.")
            sys.exit(0)

        # Validate single-letter A.. up to number of columns
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Enter a single uppercase letter corresponding to a column.")
            continue

        col_letter = user_input
        if col_letter not in COLUMN_LABELS[:COLS]:
            print(f"Invalid column. Please choose a letter from A to {COLUMN_LABELS[COLS - 1]}.")
            continue

        return COLUMN_LABELS.index(col_letter)


def next_player_index(current_index, total_players):
    """Get the next player's index in round-robin fashion."""
    return (current_index + 1) % total_players


def main():
    board = create_board(ROWS, COLS)

    # Randomly select the first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Print initial empty board
    clear_screen()
    print_board(board)

    # Main game loop
    while True:
        current_checker = ACTIVE_CHECKERS[current_player_idx]
        # Prompt until a valid column letter is given (format/bounds). Full column loses the turn.
        col = prompt_for_column(current_checker)

        # Attempt to drop checker
        placed_row = drop_checker(board, col, current_checker)
        if placed_row is None:
            # Column is full: invalid move, lose the turn
            clear_screen()
            print_board(board)
            print(f"Column {COLUMN_LABELS[col]} is full. Player {current_checker} loses this turn.")
            # Advance to next player
            current_player_idx = next_player_index(current_player_idx, NUM_PLAYERS)
            continue

        # After a successful move, check for win/draw
        if check_win(board, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw.")
            break

        # Continue to next player
        clear_screen()
        print_board(board)
        current_player_idx = next_player_index(current_player_idx, NUM_PLAYERS)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted.")
        sys.exit(0)
