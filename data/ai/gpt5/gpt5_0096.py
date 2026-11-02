import os
import random
import string

# =======================
# Configuration constants
# =======================
ROWS = 6            # number of rows (default submission requirement: 6)
COLS = 7            # number of columns (default submission requirement: 7, max 26)
NUM_PLAYERS = 2     # number of players (2 to 5 inclusive; default submission requirement: 2)
WIN_LENGTH = 4      # number in a row needed to win (always 4 per assignment)

# Validate configuration
assert 2 <= NUM_PLAYERS <= 5, "NUM_PLAYERS must be between 2 and 5"
assert 1 <= ROWS, "ROWS must be >= 1"
assert 1 <= COLS <= 26, "COLS must be between 1 and 26"

PLAYER_MARKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]


def clear_screen():
    # Clear the terminal screen (Unix/Linux)
    os.system('clear')


def create_board(rows, cols):
    # Board is a list of lists (rows x cols) initialized with single whitespace
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    # Labels A, B, C, ... up to the number of columns
    return list(string.ascii_uppercase[:cols])


def print_board(board):
    labels = column_labels(len(board[0]))
    cols = len(labels)
    # Header
    header = "  " + "   ".join(labels)
    sep = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep)
    # Each row
    for r in range(len(board)):
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
        print(sep)


def lowest_empty_row(board, col_idx):
    # Returns the index of the lowest empty row in the given column, or None if full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_idx] == " ":
            return r
    return None


def drop_checker(board, col_idx, marker):
    # Places marker in the lowest available row in column. Returns row index or None if full.
    r = lowest_empty_row(board, col_idx)
    if r is None:
        return None
    board[r][col_idx] = marker
    return r


def in_bounds(board, r, c):
    return 0 <= r < len(board) and 0 <= c < len(board[0])


def check_winner(board):
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
            start = board[r][c]
            if start == " ":
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while count < WIN_LENGTH and in_bounds(board, rr, cc) and board[rr][cc] == start:
                    count += 1
                    rr += dr
                    cc += dc
                if count == WIN_LENGTH:
                    return start
    return None


def is_draw(board):
    # Draw if no spaces left on board
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def get_valid_column_input(valid_labels, player_marker):
    # Prompt until a valid column label is provided; invalid input does not cost a turn
    while True:
        try:
            user_in = input(f"Player {player_marker}, please enter a column: ").strip().upper()
        except EOFError:
            # Treat EOF as invalid input; continue prompting
            continue
        if len(user_in) != 1 or user_in not in valid_labels:
            print("Invalid input. Please enter a valid column letter.")
            continue
        return valid_labels.index(user_in)


def main():
    board = create_board(ROWS, COLS)
    labels = column_labels(COLS)

    # Randomly select the first player
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Show the initial empty board
    clear_screen()
    print_board(board)

    while True:
        current_marker = PLAYER_MARKERS[current_player_idx]

        # Prompt for valid column letter (does not lose turn for invalid input)
        col_idx = get_valid_column_input(labels, current_marker)

        # Attempt to drop the checker
        row_idx = drop_checker(board, col_idx, current_marker)

        # Clear and print updated board after the attempt
        clear_screen()
        print_board(board)

        if row_idx is None:
            # Column was full; the turn is invalid and the player loses the turn
            print(f"Column {labels[col_idx]} is full. Player {current_marker} loses the turn.")
            # After a lost turn (no placement), still check for draw (edge case)
            if is_draw(board):
                print("It's a draw!")
                break
            # Pass to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        # Check for a winner after a successful placement
        winner = check_winner(board)
        if winner is not None:
            print(f"Player {winner} won!")
            break

        # Check for a draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
