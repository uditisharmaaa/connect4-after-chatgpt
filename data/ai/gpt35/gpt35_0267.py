import os
import random
import string

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_COUNT = 4

# Players' checkers in order
CHECKERS = ["X", "O", "V", "H", "M"]

# Configuration for this submission
NUM_PLAYERS = 2


def clear_screen():
    os.system('clear')


def create_board(rows, columns):
    """Create a board filled with spaces."""
    return [[" " for _ in range(columns)] for _ in range(rows)]


def print_board(board):
    columns = len(board[0])
    rows = len(board)

    col_labels = [string.ascii_uppercase[i] for i in range(columns)]

    # Print column headers
    print("  " + "   ".join(col_labels))
    sep_line = "+" + ("---+" * columns)
    for r in range(rows):
        print(sep_line)
        row_str = "|"
        for c in range(columns):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(sep_line)


def input_column(player_checker, columns, board):
    """
    Ask the player to input column letter until valid input is provided.
    Return the column index, or None if the column is full (loses turn).
    """
    col_labels = [string.ascii_uppercase[i] for i in range(columns)]

    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(inp) != 1 or inp not in col_labels:
            # Invalid input - not a single valid letter
            continue

        col = col_labels.index(inp)
        # Check if column is full
        if board[0][col] != " ":
            # Column full, player loses turn
            return None
        return col


def place_checker(board, col, checker):
    """
    Place the checker in the chosen column.
    The checker falls to the lowest available space in that column.
    """
    rows = len(board)
    for r in reversed(range(rows)):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col  # Return the position where checker was placed
    return None  # If full, should not happen because we check before


def check_win(board, last_row, last_col, checker):
    """
    Check if placing checker at (last_row, last_col) created a 4-in-a-row.
    Check horizontal, vertical, and both diagonals.
    """
    rows = len(board)
    cols = len(board[0])

    def count_direction(dr, dc):
        count = 0
        r, c = last_row + dr, last_col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        return count

    # Directions: horizontal (0,1), vertical (1,0),
    # diag_down (1,1), diag_up (-1,1)
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]

    for dr, dc in directions:
        # Count checkers in positive and negative directions
        count_pos = count_direction(dr, dc)
        count_neg = count_direction(-dr, -dc)
        total = count_pos + count_neg + 1  # include current checker
        if total >= WIN_COUNT:
            return True
    return False


def board_full(board):
    """Check if the board is full (no spaces left in top row)."""
    return all(cell != " " for cell in board[0])


def main():
    # Validate configuration
    if not (MIN_PLAYERS <= NUM_PLAYERS <= MAX_PLAYERS):
        print(f"Invalid number of players: {NUM_PLAYERS}. Must be between {MIN_PLAYERS} and {MAX_PLAYERS}.")
        return
    if not (1 <= COLUMNS <= MAX_COLUMNS):
        print(f"Invalid number of columns: {COLUMNS}. Must be between 1 and {MAX_COLUMNS}.")
        return

    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]

    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)

        checker = players[current_player_idx]

        col = input_column(checker, COLUMNS, board)
        if col is None:
            # Column full, lose turn
            # Switch to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        last_pos = place_checker(board, col, checker)

        clear_screen()
        print_board(board)

        if check_win(board, last_pos[0], last_pos[1], checker):
            print(f"Player {checker} won!")
            break

        if board_full(board):
            print("The game is a draw!")
            break

        # Next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
