import os
import random
import string

# -------------------------------
# Configuration (change if needed)
# -------------------------------
ROWS = 6            # number of rows (default: 6)
COLS = 7            # number of columns (default: 7, max: 26)
NUM_PLAYERS = 2     # number of players (2 to 5)

# The checkers used for players, in order
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]

# -------------------------------
# Validations for configuration
# -------------------------------
assert 2 <= NUM_PLAYERS <= 5, "NUM_PLAYERS must be between 2 and 5."
assert COLS <= 26, "COLS must be at most 26 (A-Z)."
assert ROWS >= 4 and COLS >= 4, "Board must be at least 4x4 to allow a win."
assert NUM_PLAYERS <= len(PLAYER_CHECKERS), "Not enough checker symbols defined."

# Truncate to the number of players
PLAYER_CHECKERS = PLAYER_CHECKERS[:NUM_PLAYERS]

# -------------------------------
# Game functions
# -------------------------------

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')


def create_board(rows, cols):
    """Create a board filled with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Print the board with column labels and grid lines."""
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Column headers
    header_letters = [string.ascii_uppercase[i] for i in range(cols)]
    print("  " + "   ".join(header_letters))

    # Horizontal line for the grid
    hline = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(hline)
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
    print(hline)


def get_column_index_from_input(user_input, max_cols):
    """
    Convert a single-letter column input to a zero-based index.
    Returns None if invalid.
    """
    if not user_input or len(user_input) != 1:
        return None
    ch = user_input.upper()
    if ch < "A" or ch > chr(ord("A") + max_cols - 1):
        return None
    return ord(ch) - ord("A")


def prompt_for_column(current_checker, cols):
    """
    Prompt the user until a valid column letter within range is entered.
    Returns the zero-based column index.
    """
    prompt = f"Player {current_checker}, please enter a column: "
    while True:
        raw = input(prompt).strip()
        col_idx = get_column_index_from_input(raw, cols)
        if col_idx is None:
            print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + cols - 1)}.")
            continue
        return col_idx


def find_available_row(board, col):
    """
    Given a column, find the lowest available row (from bottom up) for placement.
    Returns row index or None if the column is full.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win(board, checker):
    """
    Check if the given checker has four in a row horizontally, vertically, or diagonally.
    """
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
                count = 1
                rr, cc = r + dr, c + dc
                while count < 4 and in_bounds(rr, cc, rows, cols) and board[rr][cc] == checker:
                    count += 1
                    rr += dr
                    cc += dc
                if count == 4:
                    return True
    return False


def is_draw(board):
    """Return True if the board is full (no spaces)."""
    for row in board:
        if " " in row:
            return False
    return True


# -------------------------------
# Main game loop
# -------------------------------

def main():
    board = create_board(ROWS, COLS)

    # Randomly choose first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)

        current_checker = PLAYER_CHECKERS[current_player_index]

        # Prompt for a valid column letter input (does not lose turn on invalid input)
        col = prompt_for_column(current_checker, COLS)

        # Attempt to place the checker (lose turn if column is full)
        row = find_available_row(board, col)
        if row is None:
            # Column full -> turn is invalid and player loses the turn
            col_letter = chr(ord("A") + col)
            print(f"Column {col_letter} is full. Player {current_checker} loses the turn.")
            input("Press Enter to continue...")
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        # Place checker
        board[row][col] = current_checker

        # Check for win
        if check_win(board, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
