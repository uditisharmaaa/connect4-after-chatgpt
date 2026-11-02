import os
import random
import sys

# Constants (submission requirement: 6 rows x 7 columns, 2 players)
ROWS = 6
COLS = 7  # Max 26 (A-Z)
N_PLAYERS = 2  # Supports 2 to 5 players

# Player markers in order
MARKERS = ["X", "O", "V", "H", "M"]


def clear_screen():
    # Clear screen for Unix/Linux/macOS. Fall back to printing lines if not available.
    try:
        os.system('clear')
    except Exception:
        print("\n" * 100)


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])
    # Header with column labels A..:
    labels = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(labels)
    # Separator line builder
    sep = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(sep)
        row_cells = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row_cells)
    print(sep)


def validate_settings():
    if not (2 <= N_PLAYERS <= 5):
        print("Error: N_PLAYERS must be between 2 and 5.")
        sys.exit(1)
    if COLS > 26 or COLS < 1:
        print("Error: COLS must be between 1 and 26.")
        sys.exit(1)
    if ROWS < 1:
        print("Error: ROWS must be at least 1.")
        sys.exit(1)


def get_active_markers(n_players):
    return MARKERS[:n_players]


def prompt_for_column(active_marker, cols):
    # Keep asking until input is a valid uppercase letter for an in-range column
    while True:
        user_input = input(f"Player {active_marker}, please enter a column: ").strip()
        if not user_input:
            continue
        # Accept a single letter; ignore longer strings
        ch = user_input.upper()[0]
        if 'A' <= ch <= chr(ord('A') + cols - 1):
            return ord(ch) - ord('A')
        # Invalid input -> re-prompt without losing the turn
        # (Do not print extra messages to match assignment simplicity)


def place_checker(board, col, marker):
    """
    Attempt to place a checker in the given column.
    Returns (placed: bool, row_index_if_placed or None)
    If the column is full, returns (False, None).
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = marker
            return True, r
    return False, None


def is_draw(board):
    # Draw if no spaces remain on the board
    return all(cell != " " for row in board for cell in row)


def check_win(board):
    """
    Check if there is a 4-in-a-row on the board.
    Returns (won: bool, marker_or_None)
    """
    rows = len(board)
    cols = len(board[0])

    def in_bounds(r, c):
        return 0 <= r < rows and 0 <= c < cols

    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            m = board[r][c]
            if m == " ":
                continue
            for dr, dc in directions:
                cnt = 1
                rr, cc = r + dr, c + dc
                while cnt < 4 and in_bounds(rr, cc) and board[rr][cc] == m:
                    cnt += 1
                    rr += dr
                    cc += dc
                if cnt >= 4:
                    return True, m
    return False, None


def main():
    validate_settings()

    board = create_board(ROWS, COLS)
    players = get_active_markers(N_PLAYERS)

    # Randomly choose the first player
    current_idx = random.randint(0, N_PLAYERS - 1)

    # Initial display
    clear_screen()
    print_board(board)

    while True:
        # Prompt current player
        current_marker = players[current_idx]
        col = prompt_for_column(current_marker, COLS)

        placed, placed_row = place_checker(board, col, current_marker)
        # After attempting to place, update the display
        clear_screen()
        print_board(board)

        if not placed:
            # Column full: invalid turn and player loses the turn
            # Move to next player
            current_idx = (current_idx + 1) % N_PLAYERS
            # Continue to next turn (no win/draw possible since nothing changed)
            continue

        # Check for win
        won, winner = check_win(board)
        if won and winner is not None:
            print(f"Player {winner} won!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % N_PLAYERS


if __name__ == "__main__":
    main()
