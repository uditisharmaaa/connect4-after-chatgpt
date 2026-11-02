import os
import random
import string
import sys

# -----------------------------
# Configuration (change if desired; for submission keep as specified)
# -----------------------------
ROWS = 6                 # number of rows (e.g., 6)
COLS = 7                 # number of columns (e.g., 7), must be <= 26
NUM_PLAYERS = 2          # between 2 and 5 players
TOKENS = ["X", "O", "V", "H", "M"]  # tokens in order for up to 5 players
WIN_LENGTH = 4           # number in a row to win (fixed at 4 per assignment)

# -----------------------------
# Validation of configuration
# -----------------------------
if not (2 <= NUM_PLAYERS <= 5):
    print("ERROR: NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

if COLS < 1 or COLS > 26:
    print("ERROR: COLS must be between 1 and 26.")
    sys.exit(1)

if ROWS < 1:
    print("ERROR: ROWS must be at least 1.")
    sys.exit(1)

PLAYER_TOKENS = TOKENS[:NUM_PLAYERS]


# -----------------------------
# Game utilities
# -----------------------------
def clear_screen():
    # Per assignment: clear screen using Linux/Unix clear
    os.system('clear')


def create_board(rows, cols):
    # Board is a list of lists: rows x cols initialized with spaces
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    # Labels are uppercase letters starting from 'A'
    return list(string.ascii_uppercase[:cols])


def print_board(board):
    labels = column_labels(len(board[0]))
    # Header
    header = "  " + "   ".join(labels)
    line = "+" + "+".join(["---"] * len(labels)) + "+"
    print(header)
    print(line)
    # Rows
    for r in range(len(board)):
        row_cells = "|" + "|".join(f" {board[r][c]} " for c in range(len(board[0]))) + "|"
        print(row_cells)
        print(line)


def is_valid_column_input(inp, cols):
    if len(inp) != 1:
        return False
    if inp < 'A' or inp >= chr(ord('A') + cols):
        return False
    return True


def find_drop_row(board, col):
    # Return the row index where the checker will land, or None if column full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def count_in_direction(board, start_r, start_c, dr, dc, token):
    # Count consecutive tokens starting just beyond (start_r, start_c) in (dr, dc)
    r, c = start_r + dr, start_c + dc
    cnt = 0
    rows, cols = len(board), len(board[0])
    while in_bounds(r, c, rows, cols) and board[r][c] == token:
        cnt += 1
        r += dr
        c += dc
    return cnt


def check_win(board, last_r, last_c, token):
    # Check all 4 principal directions using last placed position
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # H, V, Diag down-right, Diag down-left
    for dr, dc in directions:
        total = 1  # include last placed
        total += count_in_direction(board, last_r, last_c, dr, dc, token)
        total += count_in_direction(board, last_r, last_c, -dr, -dc, token)
        if total >= WIN_LENGTH:
            return True
    return False


def is_draw(board):
    # Draw if no empty cells in top row (or entire board)
    return all(cell != " " for cell in board[0])


# -----------------------------
# Main game loop
# -----------------------------
def main():
    board = create_board(ROWS, COLS)

    # Randomly choose starting player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        current_token = PLAYER_TOKENS[current_player_idx]

        # Input loop for a valid column label; invalid inputs re-prompt
        while True:
            prompt = f"Player {current_token}, please enter a column: "
            user_inp = input(prompt).strip().upper()

            if not is_valid_column_input(user_inp, COLS):
                valid_range = f"A-{column_labels(COLS)[-1]}"
                print(f"Invalid input. Please enter a single letter between {valid_range}.")
                continue

            col = ord(user_inp) - ord('A')
            break  # valid column letter provided

        # Attempt to place checker
        row_to_place = find_drop_row(board, col)
        if row_to_place is None:
            # Column full: turn is invalid and player loses the turn
            print(f"Column {user_inp} is full. Turn lost.")
            # Advance to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            # Small pause for readability (optional); not required by assignment.
            # input("Press Enter to continue...")
            continue

        # Place the checker
        board[row_to_place][col] = current_token

        # Check for a win
        if check_win(board, row_to_place, col, current_token):
            clear_screen()
            print_board(board)
            print(f"Player {current_token} won!")
            break

        # Check for a draw
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("Game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
