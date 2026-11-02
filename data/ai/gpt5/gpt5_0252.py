import os
import random
import string
import sys

# ----- Configuration (you may change these for testing; submission should be 6x7 and 2 players) -----
ROWS = 6            # number of rows (height)
COLS = 7            # number of columns (width), max 26
NUM_PLAYERS = 2     # number of players supported: between 2 and 5
WIN_LENGTH = 4      # number in a row needed to win (fixed at 4 per assignment)
CHECKERS = ["X", "O", "V", "H", "M"]

# Safety checks for configuration
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if COLS < 1 or COLS > 26:
    print("COLS must be between 1 and 26.")
    sys.exit(1)
if ROWS < 1:
    print("ROWS must be at least 1.")
    sys.exit(1)

PLAYERS = CHECKERS[:NUM_PLAYERS]
COLUMN_LABELS = list(string.ascii_uppercase[:COLS])


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def draw_board(board):
    clear_screen()
    # Header with column letters
    header = "  " + "   ".join(COLUMN_LABELS)
    print(header)
    # Top border
    print("+" + ("---+" * len(board[0])))
    # Rows
    for r in range(len(board)):
        row_cells = []
        for c in range(len(board[0])):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print("+" + ("---+" * len(board[0])))


def get_valid_column_input():
    while True:
        user_input = input("Please enter a column: ").strip()
        if len(user_input) != 1:
            print("Invalid input. Enter exactly one letter corresponding to a column.")
            continue
        ch = user_input.upper()
        if ch not in COLUMN_LABELS:
            print(f"Invalid column. Enter a letter between {COLUMN_LABELS[0]} and {COLUMN_LABELS[-1]}.")
            continue
        return COLUMN_LABELS.index(ch), ch


def get_lowest_empty_row(board, col):
    # Start from bottom row upwards
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def count_in_direction(board, start_r, start_c, dr, dc, symbol):
    r, c = start_r + dr, start_c + dc
    count = 0
    rows, cols = len(board), len(board[0])
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    return count


def check_for_win(board, r, c, symbol):
    # Only check if a symbol was placed (r and c not None)
    if r is None or c is None:
        return False

    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        # Count both directions from the placed piece
        total = 1
        total += count_in_direction(board, r, c, dr, dc, symbol)
        total += count_in_direction(board, r, c, -dr, -dc, symbol)
        if total >= WIN_LENGTH:
            return True
    return False


def is_draw(board):
    # Draw if no empty spaces remain
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def choose_start_player(num_players):
    return random.randrange(num_players)


def main():
    random.seed()
    board = create_board(ROWS, COLS)
    current_player_idx = choose_start_player(NUM_PLAYERS)

    # Initial board print and prompt
    draw_board(board)
    print(f"Player {PLAYERS[current_player_idx]}, please enter a column:")

    while True:
        # Get column input (re-prompt until the input is valid)
        col, label = get_valid_column_input()

        # Try to place checker
        row_to_place = get_lowest_empty_row(board, col)
        placed = False
        winner = None

        if row_to_place is not None:
            board[row_to_place][col] = PLAYERS[current_player_idx]
            placed = True
            # Check win after placement
            if check_for_win(board, row_to_place, col, PLAYERS[current_player_idx]):
                draw_board(board)
                print(f"Player {PLAYERS[current_player_idx]} won!")
                break
            # Check draw
            if is_draw(board):
                draw_board(board)
                print("The game is a draw.")
                break
        else:
            # Column full, turn is lost
            pass

        # After turn resolution, switch player (even if turn was lost due to full column)
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

        # Redraw board and prompt next player
        draw_board(board)
        if not placed:
            print(f"Column {label} is full. Turn lost.")
        print(f"Player {PLAYERS[current_player_idx]}, please enter a column:")


if __name__ == "__main__":
    main()
