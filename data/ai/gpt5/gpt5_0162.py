import os
import random
import string
import sys

# -------------------- Constants (adjustable) --------------------
# Submission requires 6 rows x 7 columns and 2 players
ROWS = 6
COLS = 7  # Max 26 (A-Z)
NUM_PLAYERS = 2  # Supported: 2..5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4  # Always 4 per assignment
# ---------------------------------------------------------------


def clear_screen():
    # Clear the terminal screen on Unix/Linux/macOS
    os.system('clear')


def create_board(rows, cols):
    # Create a rows x cols board filled with spaces
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])

    letters = string.ascii_uppercase[:cols]

    # Header: column letters
    header = "  " + "   ".join(letters)
    sep_line = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep_line)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print(sep_line)


def get_valid_column_input(num_cols):
    # Prompt until user enters a valid column letter in range A.. (num_cols)
    letters = string.ascii_uppercase[:num_cols]
    while True:
        try:
            user_input = input().strip()
        except EOFError:
            # If input stream ends unexpectedly, exit gracefully
            sys.exit(0)
        except KeyboardInterrupt:
            sys.exit(0)

        if len(user_input) != 1:
            print(f"Invalid input. Please enter a single letter between A and {letters[-1]}:")
            continue

        ch = user_input.upper()
        if ch not in letters:
            print(f"Invalid input. Column must be between A and {letters[-1]}:")
            continue

        return letters.index(ch)


def drop_checker(board, col, symbol):
    # Place checker in the lowest available row in the given column
    # Returns the row index where the checker landed, or None if column is full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return r
    return None  # Column full


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def count_in_direction(board, start_r, start_c, dr, dc, symbol):
    # Count consecutive symbols including (start_r, start_c) in both ±(dr, dc) directions
    rows = len(board)
    cols = len(board[0])

    count = 1  # include starting cell

    # Forward direction
    r, c = start_r + dr, start_c + dc
    while in_bounds(r, c, rows, cols) and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc

    # Backward direction
    r, c = start_r - dr, start_c - dc
    while in_bounds(r, c, rows, cols) and board[r][c] == symbol:
        count += 1
        r -= dr
        c -= dc

    return count


def check_win(board, last_r, last_c, symbol):
    # Check if placing symbol at (last_r, last_c) created a connect-4
    # Directions: horizontal, vertical, diag down-right, diag up-right
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for dr, dc in directions:
        if count_in_direction(board, last_r, last_c, dr, dc, symbol) >= WIN_LENGTH:
            return True
    return False


def check_draw(board):
    # Draw if no spaces left
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def main():
    # Validate constants
    if not (2 <= NUM_PLAYERS <= 5):
        print("NUM_PLAYERS must be between 2 and 5.")
        return
    if COLS > 26 or COLS <= 0:
        print("COLS must be between 1 and 26.")
        return
    if ROWS <= 0:
        print("ROWS must be positive.")
        return

    symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    board = create_board(ROWS, COLS)

    # Randomly select first player index
    current_idx = random.randrange(NUM_PLAYERS)

    # Initial print
    clear_screen()
    print_board(board)
    print(f"Player {symbols[current_idx]}, please enter a column:")

    while True:
        # Read and validate column input (re-prompts until a valid column letter)
        col = get_valid_column_input(COLS)

        # Attempt to drop the checker
        row_placed = drop_checker(board, col, symbols[current_idx])

        # Clear and print board after the attempt (as per requirements)
        clear_screen()
        print_board(board)

        if row_placed is None:
            # Column full: the turn is invalid and the player loses the turn
            print(f"Column {string.ascii_uppercase[col]} is full. Player {symbols[current_idx]} loses the turn.")
            # Advance to next player
            current_idx = (current_idx + 1) through NUM_PLAYERS if False else (current_idx + 1) % NUM_PLAYERS
        else:
            # Check for a win
            if check_win(board, row_placed, col, symbols[current_idx]):
                print(f"Player {symbols[current_idx]} won!")
                break

            # Check for draw
            if check_draw(board):
                print("The game is a draw!")
                break

            # Advance to next player
            current_idx = (current_idx + 1) % NUM_PLAYERS

        # Prompt next player
        print(f"Player {symbols[current_idx]}, please enter a column:")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C
        print()
        sys.exit(0)
