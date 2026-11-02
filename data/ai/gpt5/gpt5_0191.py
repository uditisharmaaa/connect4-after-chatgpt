import os
import random
import string
import sys

# ====== Configuration (submission: 6 rows x 7 cols, 2 players) ======
ROWS = 6
COLS = 7  # Must be <= 26
NUM_PLAYERS = 2  # Supported: 2..5
TOKENS = ["X", "O", "V", "H", "M"]  # Used in order

WIN_LENGTH = 4  # Always 4 in a row to win


# ====== Utility Functions ======
def clear_screen():
    # Clear terminal screen as required
    os.system('clear')


def make_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    # Returns list of 'A', 'B', ... sized to COLS (max 26)
    return list(string.ascii_uppercase[:cols])


def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    labels = column_labels(cols)
    # Header line of letters
    print("  " + "   ".join(labels))
    # Horizontal separator
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(sep)
        # Print row from top to bottom; board[0] is top row
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    print(sep)


def is_board_full(board):
    # Board is full if there is no space in any cell
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def lowest_empty_row(board, col):
    # Returns the index of the lowest empty row in a column, or None if full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win_from(board, start_r, start_c, dr, dc, token):
    # Count consecutive tokens in one direction, including starting cell
    rows = len(board)
    cols = len(board[0])
    count = 0
    r, c = start_r, start_c
    while in_bounds(r, c, rows, cols) and board[r][c] == token:
        count += 1
        r += dr
        c += dc
    return count


def check_win(board, last_r, last_c, token):
    # Check all 4 directions (horizontal, vertical, and two diagonals) centered on last move
    # For each direction, count both forward and backward, subtract 1 to avoid double counting center
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        total = 1  # include the last placed piece
        # Forward
        total += count_direction(board, last_r, last_c, dr, dc, token)
        # Backward
        total += count_direction(board, last_r, last_c, -dr, -dc, token)
        if total >= WIN_LENGTH:
            return True
    return False


def count_direction(board, r, c, dr, dc, token):
    rows = len(board)
    cols = len(board[0])
    cnt = 0
    nr, nc = r + dr, c + dc
    while in_bounds(nr, nc, rows, cols) and board[nr][nc] == token:
        cnt += 1
        nr += dr
        nc += dc
    return cnt


def get_valid_input(cols):
    labels = column_labels(cols)
    label_set = set(labels)
    while True:
        try:
            user_in = input("Please enter a column: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting game.")
            sys.exit(0)
        # Accept lowercase but convert to uppercase; still validate
        if len(user_in) == 1 and user_in.upper() in label_set:
            return labels.index(user_in.upper())
        else:
            print("Invalid input. Enter a single letter for a valid column (e.g., A, B, C...).")


def game_loop(rows, cols, num_players):
    if not (2 <= num_players <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        return
    if not (1 <= cols <= 26):
        print("COLS must be between 1 and 26.")
        return

    board = make_board(rows, cols)
    players = TOKENS[:num_players]

    # Randomly select first player
    current_idx = random.randrange(num_players)

    # Show initial board and first player
    print_board(board)
    print(f"Player {players[current_idx]}, please enter a column:")

    while True:
        token = players[current_idx]

        # Prompt for input and validate format/range (does not lose turn on invalid format)
        col = get_valid_input(cols)

        # Attempt to place token
        row_to_place = lowest_empty_row(board, col)
        if row_to_place is None:
            # Column full: lose the turn
            print(f"Column {column_labels(cols)[col]} is full. Player {token} loses the turn.")
            # Move to next player
            current_idx = (current_idx + 1) % num_players
            # Reprint board for next player's turn
            print_board(board)
            print(f"Player {players[current_idx]}, please enter a column:")
            continue

        # Place the token
        board[row_to_place][col] = token

        # Print updated board
        print_board(board)

        # Check for win
        if check_win(board, row_to_place, col, token):
            print(f"Player {token} won!")
            return

        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            return

        # Next player's turn
        current_idx = (current_idx + 1) % num_players
        print(f"Player {players[current_idx]}, please enter a column:")


def main():
    game_loop(ROWS, COLS, NUM_PLAYERS)


if __name__ == "__main__":
    main()
