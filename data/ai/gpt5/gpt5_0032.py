import os
import random
import string
import sys

# =========================
# Configurable constants
# =========================
ROWS = 6           # number of rows (height)
COLS = 7           # number of columns (width), max 26
NUM_PLAYERS = 2    # number of players (2 to 5)

# Player tokens in order
TOKENS = ["X", "O", "V", "H", "M"]

# =========================
# Utility and game logic
# =========================

def clear_screen():
    # Clear using Unix/Linux clear
    os.system('clear')


def create_board(rows, cols):
    # Create a board filled with spaces
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    # Labels A, B, C, ...
    return [string.ascii_uppercase[i] for i in range(cols)]


def print_board(board):
    # Prints the board in the required ASCII-art style
    rows = len(board)
    cols = len(board[0])

    labels = column_labels(cols)
    # Header labels
    header = "  " + "   ".join(labels)
    sep = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print(sep)


def get_valid_players(num_players):
    # Validate number of players and return their tokens
    if num_players < 2 or num_players > 5:
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")
    return TOKENS[:num_players]


def get_input_column(cols):
    # Get and validate user input for a column.
    # Invalid input (non-letter, out of range) -> reprompt.
    # Returns a valid column index (0-based).
    labels = column_labels(cols)
    valid_set = set(labels)
    while True:
        user_in = input("Please enter a column: ").strip()
        if not user_in:
            print("Invalid input. Please enter a column letter.")
            continue
        # Accept either case, but convert to uppercase
        ch = user_in[0].upper()
        if ch in valid_set:
            return labels.index(ch)
        else:
            print(f"Invalid column. Valid columns are: {', '.join(labels)}")


def first_empty_row(board, col):
    # Return the row index to place a token in the given column,
    # scanning from bottom up. Return None if column is full.
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def place_checker(board, col, token):
    # Place token in the given column if possible.
    # Returns (row, col) if placed, or None if column full.
    r = first_empty_row(board, col)
    if r is None:
        return None
    board[r][col] = token
    return (r, col)


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def count_in_direction(board, start_r, start_c, dr, dc, token):
    # Count consecutive tokens in one direction (excluding the start)
    rows, cols = len(board), len(board[0])
    r, c = start_r + dr, start_c + dc
    count = 0
    while in_bounds(r, c, rows, cols) and board[r][c] == token:
        count += 1
        r += dr
        c += dc
    return count


def check_win(board, last_r, last_c):
    # Check if placing at (last_r, last_c) created a 4-in-a-row
    token = board[last_r][last_c]
    if token == " ":
        return False

    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]
    for dr, dc in directions:
        total = 1  # include the last placed token
        total += count_in_direction(board, last_r, last_c, dr, dc, token)
        total += count_in_direction(board, last_r, last_c, -dr, -dc, token)
        if total >= 4:
            return True
    return False


def is_draw(board):
    # A draw occurs if there are no spaces left on the board
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def game_loop(rows, cols, num_players):
    # Initialize
    if cols > 26:
        raise ValueError("Maximum supported number of columns is 26.")
    players = get_valid_players(num_players)
    board = create_board(rows, cols)

    # Randomly select starting player
    current_idx = random.randrange(len(players))

    # Initial print
    clear_screen()
    print_board(board)
    print(f"Player {players[current_idx]}, it's your turn.")

    # Main loop
    while True:
        # Ask for input (reprompt on invalid input)
        col = get_input_column(cols)

        # Try to place checker
        placed = place_checker(board, col, players[current_idx])

        # Clear and print board after the attempt (as per requirement)
        clear_screen()
        print_board(board)

        if placed is None:
            # Column full: turn is invalid and the player loses the turn
            print(f"Column {column_labels(cols)[col]} is full. Player {players[current_idx]} loses the turn.")
            # Switch player
            current_idx = (current_idx + 1) % len(players)
            # Show prompt for next player
            print(f"Player {players[current_idx]}, it's your turn.")
            continue

        # Check for win
        r, c = placed
        if check_win(board, r, c):
            print(f"Player {players[current_idx]} won!")
            return

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            return

        # Next player's turn
        current_idx = (current_idx + 1) % len(players)
        print(f"Player {players[current_idx]}, it's your turn.")


def main():
    try:
        game_loop(ROWS, COLS, NUM_PLAYERS)
    except KeyboardInterrupt:
        print("\nGame interrupted.")
        sys.exit(0)


if __name__ == "__main__":
    main()
