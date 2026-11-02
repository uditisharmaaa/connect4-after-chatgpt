import os
import random
import string
import sys

# ========= Configuration (you may change these for testing) =========
ROWS = 6
COLS = 7  # Max 26 columns (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5
TOKENS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4  # Always 4 per assignment
# ====================================================================

assert 2 <= NUM_PLAYERS <= 5, "Number of players must be between 2 and 5."
assert 1 <= COLS <= 26, "Number of columns must be between 1 and 26."
assert ROWS >= 1, "Number of rows must be at least 1."

PLAYERS = TOKENS[:NUM_PLAYERS]


def clear_screen():
    # Clear screen for Unix/Linux/macOS as required
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Column header
    letters = string.ascii_uppercase[:cols]
    header = "  " + "   ".join(letters)
    sep = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep)
    for r in range(rows):
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
        print(sep)


def col_letter_to_index(ch):
    ch = ch.upper()
    if ch in string.ascii_uppercase:
        return ord(ch) - ord('A')
    return None


def get_valid_column_input(cols):
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        if len(user_input) != 1:
            print("Invalid input. Enter a single uppercase letter (e.g., A).")
            continue
        if user_input not in string.ascii_uppercase:
            print("Invalid input. Enter a letter A-Z.")
            continue
        idx = col_letter_to_index(user_input)
        if idx is None or not (0 <= idx < cols):
            print("Invalid input. Column is out of range.")
            continue
        return idx, user_input


def drop_checker(board, col, token):
    # Place token in the lowest available row in the given column.
    # Return row index if placed, or None if column is full.
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r
    return None


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_winner(board, token):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != token:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while count < WIN_LENGTH and in_bounds(nr, nc, rows, cols) and board[nr][nc] == token:
                    count += 1
                    nr += dr
                    nc += dc
                if count >= WIN_LENGTH:
                    return True
    return False


def check_draw(board):
    # Draw if no spaces left in top row or anywhere
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def print_state(board, current_player_token, prompt=True):
    clear_screen()
    print_board(board)
    if prompt:
        print(f"Player {current_player_token}, please enter a column:")


def main():
    board = create_board(ROWS, COLS)

    # Randomly select starting player
    current_player_index = random.randrange(NUM_PLAYERS)

    # Initial board print
    print_state(board, PLAYERS[current_player_index])

    while True:
        current_token = PLAYERS[current_player_index]

        # Get a syntactically valid column input (letter within range)
        col_idx, col_letter = get_valid_column_input(COLS)

        # Try to place checker
        placed_row = drop_checker(board, col_idx, current_token)

        if placed_row is None:
            # Column full: turn is invalid and lost
            print_state(board, current_token, prompt=False)
            print(f"Column {col_letter} is full. Player {current_token} loses the turn.")
            # Switch player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            # Show next prompt
            print_state(board, PLAYERS[current_player_index])
            continue

        # After a successful move, update display
        print_state(board, current_token, prompt=False)

        # Check for win
        if check_winner(board, current_token):
            print(f"Player {current_token} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw.")
            break

        # Switch player and continue
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        print_state(board, PLAYERS[current_player_index])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted.")
        sys.exit(0)
