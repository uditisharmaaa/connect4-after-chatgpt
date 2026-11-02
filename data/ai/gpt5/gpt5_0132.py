import os
import random
import string

# -------------------------------
# Configuration (change if needed)
# -------------------------------
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

# -------------------------------
# Helpers and Game Logic
# -------------------------------

def create_board(rows, cols):
    """Create a rows x cols board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    """Return a list of uppercase column labels (A..Z)."""
    if cols > 26:
        raise ValueError("Maximum supported columns is 26.")
    return list(string.ascii_uppercase[:cols])


def print_board(board, labels):
    """Clear the screen and print the board with headers."""
    os.system('clear')
    # Header with column labels
    print("  " + "   ".join(labels))
    horiz = "+" + "+".join(["---"] * len(labels)) + "+"
    for r in range(len(board)):
        print(horiz)
        row_str = "|" + "|".join(f" {board[r][c]} " for c in range(len(labels))) + "|"
        print(row_str)
    print(horiz)


def get_column_index(user_input, labels):
    """Convert user input into a column index if valid, else return None."""
    if not user_input or len(user_input) != 1:
        return None
    ch = user_input.upper()
    if ch not in labels:
        return None
    return labels.index(ch)


def drop_checker(board, col_index, checker):
    """
    Drop a checker into the specified column.
    Return the row index where it lands, or None if the column is full.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = checker
            return r
    return None


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win(board, checker):
    """Check if the given checker has a winning line of WIN_LENGTH."""
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
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while count < WIN_LENGTH and in_bounds(rr, cc, rows, cols) and board[rr][cc] == checker:
                    count += 1
                    rr += dr
                    cc += dc
                if count == WIN_LENGTH:
                    return True
    return False


def check_draw(board):
    """Return True if the board is full (no spaces)."""
    for row in board:
        if " " in row:
            return False
    return True


def next_player_index(current, total):
    return (current + 1) % total


def prompt_for_column(current_checker, labels):
    """Prompt the current player for a valid column letter; keep asking until valid."""
    while True:
        user_input = input(f"Player {current_checker}, please enter a column: ").strip()
        col_idx = get_column_index(user_input, labels)
        if col_idx is not None:
            return col_idx
        # invalid input: ask again (turn is not lost)
        print("Invalid input. Please enter a valid column letter (e.g., A, B, C).")


# -------------------------------
# Main Game Loop
# -------------------------------

def main():
    # Basic validations
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    if COLS > 26:
        raise ValueError("COLS must be at most 26.")

    players = CHECKERS[:NUM_PLAYERS]
    labels = column_labels(COLS)
    board = create_board(ROWS, COLS)

    # Randomly choose the first player
    current = random.randrange(NUM_PLAYERS)

    while True:
        # Show current board before the move
        print_board(board, labels)

        current_checker = players[current]
        col_idx = prompt_for_column(current_checker, labels)

        row_idx = drop_checker(board, col_idx, current_checker)
        if row_idx is None:
            # Column full: turn is invalid and the player loses the turn
            print(f"Column {labels[col_idx]} is full. Player {current_checker} loses the turn.")
            current = next_player_index(current, NUM_PLAYERS)
            continue

        # After a valid placement, check for win/draw
        if check_win(board, current_checker):
            print_board(board, labels)
            print(f"Player {current_checker} won!")
            break

        if check_draw(board):
            print_board(board, labels)
            print("The game is a draw.")
            break

        # Next player's turn
        current = next_player_index(current, NUM_PLAYERS)


if __name__ == "__main__":
    main()
