import os
import random
import string
import sys

# =========================
# Configuration (constants)
# =========================
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

# Safety checks for constraints
assert 2 <= NUM_PLAYERS <= 5, "Number of players must be between 2 and 5."
assert 1 <= COLS <= 26, "Number of columns must be between 1 and 26."
assert ROWS >= 4, "Number of rows must be at least 4."
PLAYER_SYMBOLS = CHECKERS[:NUM_PLAYERS]
COLUMN_LABELS = list(string.ascii_uppercase[:COLS])


def clear_screen():
    # Clear terminal screen
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board, current_symbol=None):
    # Header with column labels
    header = "  " + "   ".join(COLUMN_LABELS)
    sep = "+" + "+".join(["---"] * COLS) + "+"

    print(header)
    print(sep)
    for r in range(ROWS):
        row_cells = []
        for c in range(COLS):
            row_cells.append(board[r][c] if board[r][c] != " " else " ")
        print("| " + " | ".join(row_cells) + " |")
        print(sep)

    if current_symbol is not None:
        print(f"Player {current_symbol}, please enter a column:")


def get_column_input():
    # Keep asking until a valid column label (A.. up to COLS) is given.
    while True:
        try:
            user_input = input().strip().upper()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting game.")
            sys.exit(0)

        if len(user_input) != 1:
            print(f"Invalid input. Enter a single letter between A and {COLUMN_LABELS[-1]}:")
            continue

        if user_input not in COLUMN_LABELS:
            print(f"Invalid column. Enter a letter between A and {COLUMN_LABELS[-1]}:")
            continue

        # Valid column character
        return COLUMN_LABELS.index(user_input)


def place_checker(board, col, symbol):
    # Place at lowest available row in the given column.
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return r
    return None  # Column full


def count_in_direction(board, start_r, start_c, dr, dc, symbol):
    r, c = start_r + dr, start_c + dc
    count = 0
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    return count


def check_win(board, last_r, last_c, symbol):
    # Check all 4 directions (pairwise) that can make 4 in a row
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]
    for dr, dc in directions:
        total = 1  # count the last placed piece
        total += count_in_direction(board, last_r, last_c, dr, dc, symbol)
        total += count_in_direction(board, last_r, last_c, -dr, -dc, symbol)
        if total >= WIN_LENGTH:
            return True
    return False


def check_draw(board):
    # Draw if no spaces left anywhere on board
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True


def next_player_index(current, num_players):
    return (current + 1) % num_players


def main():
    board = create_board(ROWS, COLS)
    current_player = random.randrange(NUM_PLAYERS)

    # Initial display
    clear_screen()
    print_board(board, PLAYER_SYMBOLS[current_player])

    while True:
        col = get_column_input()

        # Try placing checker
        placed_row = place_checker(board, col, PLAYER_SYMBOLS[current_player])

        if placed_row is None:
            # Column full: turn is invalid and the player loses the turn
            clear_screen()
            print_board(board)  # Show unchanged board
            print(f"Column {COLUMN_LABELS[col]} is full. Player {PLAYER_SYMBOLS[current_player]} loses the turn.")
            current_player = next_player_index(current_player, NUM_PLAYERS)
            print(f"Player {PLAYER_SYMBOLS[current_player]}, please enter a column:")
            continue

        # Successful move: update board, check for win/draw
        clear_screen()
        print_board(board)

        if check_win(board, placed_row, col, PLAYER_SYMBOLS[current_player]):
            print(f"Player {PLAYER_SYMBOLS[current_player]} won!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player = next_player_index(current_player, NUM_PLAYERS)
        print(f"Player {PLAYER_SYMBOLS[current_player]}, please enter a column:")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nExiting game.")
        sys.exit(0)
