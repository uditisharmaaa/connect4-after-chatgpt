import os
import random
import string
import sys
import time

# =========================
# Configuration (constants)
# =========================
ROWS = 6
COLS = 7           # Max 26 columns (A-Z)
NUM_PLAYERS = 2    # Between 2 and 5 players
WIN_LENGTH = 4     # Always 4, per assignment

PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# Validate configuration
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if not (1 <= COLS <= 26):
    print("COLS must be between 1 and 26.")
    sys.exit(1)
if ROWS < 1:
    print("ROWS must be at least 1.")
    sys.exit(1)

ACTIVE_PLAYERS = PLAYER_SYMBOLS[:NUM_PLAYERS]


# =========================
# Utility functions
# =========================
def clear_screen():
    # Clear the terminal screen (Unix/Linux)
    os.system('clear')


def create_board(rows, cols):
    # Create a ROWS x COLS board filled with spaces
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Column headers (A, B, C, ...)
    header_letters = list(string.ascii_uppercase[:cols])
    print("  " + "   ".join(header_letters))

    # Top border line
    horizontal_line = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(horizontal_line)
        # Row content
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
    # Bottom border line
    print(horizontal_line)


def is_valid_column_input(text, cols):
    # Valid input is a single letter within A.. up to number of columns
    if len(text) != 1:
        return False
    if text < "A" or text > chr(ord("A") + cols - 1):
        return False
    return True


def drop_checker(board, col_index, symbol):
    """
    Attempt to drop a checker with 'symbol' into column col_index.
    Returns the row index where it landed, or None if the column is full.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_index] == " ":
            board[r][col_index] = symbol
            return r
    return None  # Column is full


def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    n = WIN_LENGTH

    # Directions: (dr, dc)
    directions = [
        (0, 1),    # Horizontal right
        (1, 0),    # Vertical down
        (1, 1),    # Diagonal down-right
        (1, -1),   # Diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == symbol:
                    count += 1
                    if count == n:
                        return True
                    rr += dr
                    cc += dc
    return False


def check_draw(board):
    # Draw if no empty spaces remain anywhere
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


# =========================
# Main game loop
# =========================
def main():
    random.seed()

    board = create_board(ROWS, COLS)
    current_player_index = random.randrange(NUM_PLAYERS)

    # Initial display before the first move
    clear_screen()
    print_board(board)

    while True:
        current_symbol = ACTIVE_PLAYERS[current_player_index]
        cols_letters = string.ascii_uppercase[:COLS]

        # Prompt loop for valid input (column letter). Invalid input does not lose turn.
        while True:
            user_in = input(f"Player {current_symbol}, please enter a column: ").strip().upper()
            if is_valid_column_input(user_in, COLS):
                col_idx = ord(user_in) - ord('A')
                break
            else:
                print("Invalid input. Please enter a valid column letter.")
                # Reprint board context
                time.sleep(0.5)
                clear_screen()
                print_board(board)

        # Attempt to drop the checker. If column is full, the turn is lost.
        row_placed = drop_checker(board, col_idx, current_symbol)
        if row_placed is None:
            # Column full, lose turn
            clear_screen()
            print_board(board)
            print(f"Column {cols_letters[col_idx]} is full. Player {current_symbol} loses this turn.")
            time.sleep(1.0)
            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            clear_screen()
            print_board(board)
            continue

        # After a successful move, check for a win or draw
        if check_win(board, current_symbol):
            clear_screen()
            print_board(board)
            print(f"Player {current_symbol} won!")
            break

        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

        # Show updated board for next turn
        clear_screen()
        print_board(board)


if __name__ == "__main__":
    main()
