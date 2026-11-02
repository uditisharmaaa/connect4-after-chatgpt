import os
import random
import string
import sys

# =========================
# Configuration constants
# =========================
ROWS = 6                  # Default per submission requirement
COLS = 7                  # Default per submission requirement (max 26)
NUM_PLAYERS = 2           # Between 2 and 5 inclusive

# Player symbols in order; use first NUM_PLAYERS entries
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# Number of checkers in a row to win (always 4 per spec)
WIN_LENGTH = 4


# =========================
# Utility & Game Functions
# =========================
def clear_screen():
    # Clear terminal screen (Linux/Unix target per assignment)
    os.system('clear')


def create_board(rows, cols):
    # 2D board initialized with spaces
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Column labels: A, B, C, ...
    header = "  " + "   ".join(string.ascii_uppercase[:cols])

    # Horizontal separator line
    sep = "+" + "+".join(["---"] * cols) + "+"

    # Build output lines
    lines = [header, sep]
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        lines.append("|" + "|".join(row_cells) + "|")
        lines.append(sep)

    # Print
    clear_screen()
    print("\n".join(lines))


def get_lowest_empty_row(board, col):
    # Return the row index of the lowest empty cell in a given column, or None if full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def is_valid_column_input(inp, cols):
    # Valid if single alphabetic character mapping to a column within bounds
    if not inp or len(inp) != 1:
        return False
    if not inp.isalpha():
        return False
    ch = inp.upper()
    idx = ord(ch) - ord('A')
    return 0 <= idx < cols


def check_direction(board, start_r, start_c, dr, dc, symbol):
    # Count contiguous symbols including starting cell along (dr, dc) and opposite
    rows = len(board)
    cols = len(board[0])

    count = 1  # include the starting cell

    # Forward direction
    r, c = start_r + dr, start_c + dc
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc

    # Backward direction
    r, c = start_r - dr, start_c - dc
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
        count += 1
        r -= dr
        c -= dc

    return count >= WIN_LENGTH


def check_win(board, last_r, last_c, symbol):
    # Check 4-in-a-row in all directions from the last placed checker
    return (
        check_direction(board, last_r, last_c, 0, 1, symbol) or   # Horizontal
        check_direction(board, last_r, last_c, 1, 0, symbol) or   # Vertical
        check_direction(board, last_r, last_c, 1, 1, symbol) or   # Diagonal down-right
        check_direction(board, last_r, last_c, 1, -1, symbol)     # Diagonal down-left
    )


def board_full(board):
    # True if no spaces left anywhere
    return all(cell != " " for row in board for cell in row)


def prompt_player(symbol, cols):
    # Prompt until valid column input (column letter within bounds)
    while True:
        try:
            user_in = input(f"Player {symbol}, please enter a column: ").strip()
        except EOFError:
            # In case of non-interactive env: exit gracefully
            print()
            sys.exit(0)

        if is_valid_column_input(user_in, cols):
            return ord(user_in.upper()) - ord('A')
        # Invalid input: keep asking (turn is not lost)
        print("Invalid input. Please enter a valid column letter (e.g., A, B, C).")


def run_game(rows, cols, num_players):
    # Basic validations
    if not (2 <= num_players <= 5):
        raise ValueError("Number of players must be between 2 and 5.")
    if cols > 26:
        raise ValueError("Maximum supported columns is 26.")

    # Setup players and board
    symbols = PLAYER_SYMBOLS[:num_players]
    board = create_board(rows, cols)

    # Randomly select starting player index
    current_idx = random.randrange(num_players)

    # Show initial empty board and who starts
    print_board(board)

    last_move = None  # Track last move position for win checking

    while True:
        symbol = symbols[current_idx]

        # Display prompt for current player
        col = prompt_player(symbol, cols)

        # Attempt to place checker
        row = get_lowest_empty_row(board, col)
        if row is None:
            # Column full: turn is invalid and player loses the turn
            print(f"Column {chr(ord('A') + col)} is full. Player {symbol} loses the turn.")
            # Reprint the unchanged board after message
            # Pause briefly waiting for Enter so message is visible
            try:
                input("Press Enter to continue...")
            except EOFError:
                pass
            print_board(board)
            # Next player's turn
            current_idx = (current_idx + 1) % num_players
            # Check for draw even if no move was placed
            if board_full(board):
                print("It's a draw!")
                break
            continue

        # Place the checker
        board[row][col] = symbol
        last_move = (row, col, symbol)

        # Print updated board
        print_board(board)

        # Check for a win from the last move
        if check_win(board, row, col, symbol):
            print(f"Player {symbol} won!")
            break

        # Check for a draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % num_players


def main():
    run_game(ROWS, COLS, NUM_PLAYERS)


if __name__ == "__main__":
    main()
