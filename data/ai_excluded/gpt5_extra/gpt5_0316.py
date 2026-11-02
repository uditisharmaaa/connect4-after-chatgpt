import os
import random
import string
import sys

# ======== Configurable constants (adjustable but constrained) ========
ROWS = 6
COLS = 7          # Max 26 (A-Z)
NUM_PLAYERS = 2   # Between 2 and 5
WIN_LENGTH = 4

# Ensure constraints
COLS = max(1, min(26, COLS))
NUM_PLAYERS = max(2, min(5, NUM_PLAYERS))

PLAYER_MARKS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]


def clear_screen():
    # Per assignment requirement (Unix-like terminals)
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Column headers
    labels = [string.ascii_uppercase[i] for i in range(cols)]
    header = "  " + "   ".join(labels)
    sep_line = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep_line)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
        print(sep_line)


def is_valid_column_input(inp, cols):
    if len(inp) != 1:
        return False
    if not inp.isalpha():
        return False
    idx = ord(inp.upper()) - ord('A')
    return 0 <= idx < cols


def get_column_from_input(inp):
    return ord(inp.upper()) - ord('A')


def get_player_input(current_player_mark, cols):
    while True:
        try:
            user_inp = input(f"Player {current_player_mark}, please enter a column: ").strip()
        except EOFError:
            # Treat EOF as invalid; continue prompting
            continue

        if is_valid_column_input(user_inp, cols):
            return get_column_from_input(user_inp)
        else:
            print("Invalid input. Please enter a valid column letter within the board (e.g., A, B, C...).")


def drop_checker(board, col, mark):
    """
    Attempts to drop a checker into column 'col'.
    Returns the (row, col) where the checker lands, or None if the column is full.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):  # start from bottom
        if board[r][col] == " ":
            board[r][col] = mark
            return (r, col)
    return None


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win_from(board, start_r, start_c, dr, dc, mark):
    """
    Count consecutive marks starting from (start_r, start_c) in direction (dr, dc).
    Includes the starting cell if it matches 'mark'.
    """
    rows, cols = len(board), len(board[0])
    count = 0
    r, c = start_r, start_c
    while in_bounds(r, c, rows, cols) and board[r][c] == mark:
        count += 1
        r += dr
        c += dc
    return count


def check_win(board, last_move, mark):
    """
    Check win based on the last move coordinates and player's mark.
    We examine 4 directions: horizontal, vertical, and 2 diagonals.
    For each line, count both forward and backward directions.
    """
    if last_move is None:
        return False
    r, c = last_move
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        # Count including both directions but avoid double counting the center
        count = 1
        count += check_win_from(board, r + dr, c + dc, dr, dc, mark)
        count += check_win_from(board, r - dr, c - dc, -dr, -dc, mark)
        if count >= WIN_LENGTH:
            return True
    return False


def is_draw(board):
    # A draw occurs when there is no empty cell left
    for row in board:
        if " " in row:
            return False
    return True


def game_loop():
    rows, cols = ROWS, COLS
    board = create_board(rows, cols)

    # Randomly select starting player index
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial screen
    clear_screen()
    print_board(board)

    # Inform who starts (optional, not specified but helpful)
    print(f"Player {PLAYER_MARKS[current_player_idx]} starts.\n")

    while True:
        current_mark = PLAYER_MARKS[current_player_idx]
        # Prompt for input
        col = get_player_input(current_mark, cols)

        # Try to drop the checker
        landing = drop_checker(board, col, current_mark)
        clear_screen()
        print_board(board)

        if landing is None:
            # Column is full: turn is invalid and player loses the turn
            print(f"Column {string.ascii_uppercase[col]} is full. Player {current_mark} loses the turn.\n")
        else:
            # Check for win
            if check_win(board, landing, current_mark):
                print(f"Player {current_mark} won!")
                break

            # Check for draw
            if is_draw(board):
                print("The game is a draw!")
                break

        # Next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


def main():
    try:
        game_loop()
    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C
        sys.exit(0)


if __name__ == "__main__":
    main()
