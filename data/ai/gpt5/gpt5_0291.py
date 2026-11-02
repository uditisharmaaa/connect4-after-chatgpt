import os
import random
import string
import sys

# ========= Configuration (you may change these for testing) =========
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
WIN_LENGTH = 4
PLAYER_TOKENS = ["X", "O", "V", "H", "M"]
# ====================================================================

if not (2 <= NUM_PLAYERS <= 5):
    raise ValueError("NUM_PLAYERS must be between 2 and 5.")
if not (1 <= COLS <= 26):
    raise ValueError("COLS must be between 1 and 26.")
if len(PLAYER_TOKENS) < NUM_PLAYERS:
    raise ValueError("Not enough player tokens provided.")


def clear_screen():
    # Clear the terminal screen
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    # Labels A, B, C, ...
    return list(string.ascii_uppercase[:cols])


def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows else 0
    labels = column_labels(cols)

    # Top labels
    label_line = "  " + "   ".join(labels)
    sep_line = "+" + "+".join(["---"] * cols) + "+"

    print(label_line)
    print(sep_line)
    for r in range(rows):
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
        print(sep_line)


def board_full(board):
    # If top row contains no spaces, board is full
    return all(cell != " " for cell in board[0])


def drop_checker(board, col_index, token):
    """
    Attempts to drop a checker with 'token' into column 'col_index'.
    Returns the (row_index) where the checker lands, or None if the column is full.
    """
    rows = len(board)
    # Start from bottom row upwards
    for r in range(rows - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = token
            return r
    return None


def in_bounds(board, r, c):
    return 0 <= r < len(board) and 0 <= c < len(board[0])


def count_in_direction(board, start_r, start_c, dr, dc, token):
    """
    Count consecutive tokens starting at (start_r, start_c) and moving (dr, dc).
    Includes the starting position.
    """
    r, c = start_r, start_c
    count = 0
    while in_bounds(board, r, c) and board[r][c] == token:
        count += 1
        r += dr
        c += dc
    return count


def is_winning_move(board, r, c, token):
    """
    Check if placing token at (r, c) results in a win of WIN_LENGTH in any direction.
    """
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]
    for dr, dc in directions:
        # Count tokens in positive and negative directions, subtract 1 to avoid double-counting (r,c)
        total = (
            count_in_direction(board, r, c, dr, dc, token) +
            count_in_direction(board, r, c, -dr, -dc, token) - 1
        )
        if total >= WIN_LENGTH:
            return True
    return False


def parse_input(user_input, cols):
    """
    Validates user input: must be a single uppercase letter within available columns.
    Returns the column index (0-based) if valid, otherwise None.
    """
    if len(user_input) != 1:
        return None
    if user_input < 'A' or user_input > 'Z':
        return None
    idx = ord(user_input) - ord('A')
    if 0 <= idx < cols:
        return idx
    return None


def game_loop():
    tokens = PLAYER_TOKENS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    # Randomly select starting player
    current_player = random.randrange(NUM_PLAYERS)

    # Initial display
    clear_screen()
    print_board(board)

    while True:
        # For draw check in case of no available moves at all
        if board_full(board):
            print("It's a draw!")
            break

        token = tokens[current_player]
        labels = column_labels(COLS)

        # Prompt until valid input (letters only and within board).
        # Note: If chosen valid column is full, player loses the turn (no re-prompt).
        while True:
            try:
                user_in = input(f"Player {token}, please enter a column: ").strip().upper()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting game.")
                sys.exit(0)

            col_idx = parse_input(user_in, COLS)
            if col_idx is None:
                print(f"Invalid input. Please enter one of: {', '.join(labels)}")
                continue
            else:
                break

        # Attempt to drop checker
        row_landed = drop_checker(board, col_idx, token)
        if row_landed is None:
            # Column full: turn is invalid and player loses the turn
            clear_screen()
            print_board(board)
            print(f"Column {labels[col_idx]} is full. Player {token} loses the turn.")
            # Next player's turn
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        # Successful move: update screen
        clear_screen()
        print_board(board)

        # Check for win
        if is_winning_move(board, row_landed, col_idx, token):
            print(f"Player {token} won!")
            break

        # Check for draw after a valid move
        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS


def main():
    game_loop()


if __name__ == "__main__":
    main()
