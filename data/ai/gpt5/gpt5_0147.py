import os
import random
import string
import sys

# =========================
# Configuration (constants)
# =========================
ROWS = 6
COLS = 7  # Max 26 columns supported
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
EMPTY = " "
WIN_LENGTH = 4  # Always 4 per assignment
MAX_COLS = 26

# Validate configuration
assert 2 <= NUM_PLAYERS <= 5, "NUM_PLAYERS must be between 2 and 5."
assert 1 <= COLS <= MAX_COLS, f"COLS must be between 1 and {MAX_COLS}."
assert len(CHECKERS) >= NUM_PLAYERS, "Not enough checker symbols provided for players."


def clear_screen():
    # Assignment requests using 'clear'
    os.system('clear')


def create_board(rows, cols):
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    # Labels start from 'A'
    return list(string.ascii_uppercase[:cols])


def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    labels = column_labels(cols)

    # Header labels
    print("  " + "   ".join(labels))

    # Horizontal border
    hline = "+" + "+".join(["---"] * cols) + "+"

    for r in range(rows):
        print(hline)
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(hline)


def get_valid_column_input(player_checker, cols):
    labels = column_labels(cols)
    prompt = f"Player {player_checker}, please enter a column: "
    while True:
        try:
            user_in = input(prompt)
        except (EOFError, KeyboardInterrupt):
            print("\nInput interrupted. Exiting game.")
            sys.exit(0)

        user_in = user_in.strip()
        if len(user_in) == 0:
            print("Invalid input: empty. Please enter a column letter.")
            continue

        letter = user_in.upper()
        if len(letter) != 1 or letter not in labels:
            print(f"Invalid input: please enter a single letter between {labels[0]} and {labels[-1]}.")
            continue

        col_index = labels.index(letter)
        return col_index, letter  # Return both index and label for messages


def drop_checker(board, col, checker):
    # Place checker in the lowest available row in the column.
    # Returns the row index where the checker was placed, or None if the column is full.
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == EMPTY:
            board[r][col] = checker
            return r
    return None


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win(board, row, col, checker):
    # Check if placing 'checker' at (row, col) creates a win of length WIN_LENGTH
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1  # Count the placed checker itself

        # Forward direction
        r, c = row + dr, col + dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc

        # Backward direction
        r, c = row - dr, col - dc
        while in_bounds(r, c, rows, cols) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_LENGTH:
            return True

    return False


def check_draw(board):
    # Draw if no EMPTY cells remain in top row or any row
    for row in board:
        if EMPTY in row:
            return False
    return True


def main():
    rows = ROWS
    cols = COLS
    players = CHECKERS[:NUM_PLAYERS]

    board = create_board(rows, cols)

    # Randomly select starting player
    current_player_index = random.randrange(len(players))

    # Show initial empty board before the game starts
    print_board(board)

    # Game loop
    while True:
        current_checker = players[current_player_index]

        # Ask for input and validate column letter; retry on invalid input
        col_index, col_label = get_valid_column_input(current_checker, cols)

        # Try to drop checker; if column full, turn is invalid and player loses the turn
        row_index = drop_checker(board, col_index, current_checker)
        if row_index is None:
            # Column full: lose the turn
            print_board(board)
            print(f"Column {col_label} is full. Player {current_checker} loses the turn.")
            # Move to next player
            current_player_index = (current_player_index + 1) % len(players)
            continue

        # Valid placement: print updated board
        print_board(board)

        # Check for win
        if check_win(board, row_index, col_index, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % len(players)


if __name__ == "__main__":
    main()
