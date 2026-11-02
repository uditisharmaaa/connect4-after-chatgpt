import os
import random
import sys

# ----------------------------
# Configuration (adjustable)
# ----------------------------
ROWS = 6                # Number of rows (e.g., 6)
COLUMNS = 7             # Number of columns (e.g., 7), max 26
NUM_PLAYERS = 2         # From 2 to 5 players

# Predefined player checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]

# ----------------------------
# Validation of configuration
# ----------------------------
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if not (1 <= COLUMNS <= 26):
    print("COLUMNS must be between 1 and 26.")
    sys.exit(1)

if ROWS <= 0:
    print("ROWS must be positive.")
    sys.exit(1)

PLAYERS = CHECKERS[:NUM_PLAYERS]


# ----------------------------
# Utility Functions
# ----------------------------
def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('clear')


def create_board(rows: int, cols: int):
    """Create a board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_label(index: int) -> str:
    """Return the column label (A-Z) for a given index."""
    return chr(ord('A') + index)


def label_to_index(label: str) -> int:
    """Convert a column label (A-Z) to a zero-based column index."""
    return ord(label) - ord('A')


def print_board(board) -> None:
    """Print the board in the specified format."""
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header
    header_labels = [column_label(i) for i in range(cols)]
    print("  " + "   ".join(header_labels))

    # Horizontal border segment
    border = "+---" * cols + "+"

    for r in range(rows):
        print(border)
        row_cells = []
        for c in range(cols):
            cell = board[r][c]
            row_cells.append(f"| {cell} ")
        print("".join(row_cells) + "|")
    print(border)


def find_lowest_empty_row(board, col: int) -> int:
    """Return the lowest empty row index in the given column, or -1 if full."""
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return -1


def is_draw(board) -> bool:
    """Return True if the board is full (no empty spaces), else False."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def check_win(board, symbol: str) -> bool:
    """Check if the given symbol has 4 in a row horizontally, vertically, or diagonally."""
    rows = len(board)
    cols = len(board[0])

    # Directions: (dr, dc)
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
                count = 1
                rr, cc = r + dr, c + dc
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == symbol:
                    count += 1
                    if count == 4:
                        return True
                    rr += dr
                    cc += dc
    return False


def read_valid_column_input(cols: int) -> int:
    """
    Read and validate the user's column input.
    Keeps asking until a valid uppercase letter within [A, A+cols-1] is provided.
    Returns the zero-based column index.
    """
    last_label = column_label(cols - 1)
    while True:
        user_input = input().strip()
        if not user_input or len(user_input) != 1:
            print(f"Invalid input. Please enter a letter between A and {last_label}:")
            continue

        ch = user_input.upper()
        if not ('A' <= ch <= last_label):
            print(f"Invalid input. Please enter a letter between A and {last_label}:")
            continue

        return label_to_index(ch)


# ----------------------------
# Main Game Loop
# ----------------------------
def main():
    board = create_board(ROWS, COLUMNS)

    # Randomly select first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Initial board print
    clear_screen()
    print_board(board)

    # Gameplay loop
    while True:
        current_symbol = PLAYERS[current_player_idx]
        last_label = column_label(COLUMNS - 1)
        print(f"Player {current_symbol}, please enter a column:")

        # Read and validate input letter (reprompt on invalid input)
        col = read_valid_column_input(COLUMNS)

        # Check if column is full -> turn is lost
        if board[0][col] != " ":
            print(f"Column {column_label(col)} is full. Turn lost.")
            # Next player's turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            # Print updated (unchanged) board for next turn
            clear_screen()
            print_board(board)
            continue

        # Place the checker at the lowest available row in the selected column
        row_to_place = find_lowest_empty_row(board, col)
        if row_to_place == -1:
            # Should not happen since we checked top cell, but just in case
            print(f"Column {column_label(col)} is full. Turn lost.")
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            clear_screen()
            print_board(board)
            continue

        board[row_to_place][col] = current_symbol

        # After placing, check for win
        if check_win(board, current_symbol):
            clear_screen()
            print_board(board)
            print(f"Player {current_symbol} won!")
            break

        # Check for draw
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("Game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

        # Print updated board before next turn
        clear_screen()
        print_board(board)


if __name__ == "__main__":
    main()
