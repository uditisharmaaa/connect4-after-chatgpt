import os
import random
import sys

# =========================
# Configuration (Constants)
# =========================
ROWS = 6                 # Number of rows (default for submission: 6)
COLS = 7                 # Number of columns (default for submission: 7, max 26)
NUM_PLAYERS = 2          # Number of players (2 to 5 for full support; submission requires 2)
CHECKERS = ["X", "O", "V", "H", "M"]  # Order of checkers for players

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

PLAYERS = CHECKERS[:NUM_PLAYERS]


# =========================
# Utility / Display
# =========================
def clear_screen():
    # Linux/Unix terminal clear (as required)
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Column header
    header_letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(header_letters))

    # Top border
    print("+" + "+".join(["---"] * cols) + "+")

    # Rows
    for r in range(rows):
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
        print("+" + "+".join(["---"] * cols) + "+")


# =========================
# Game Mechanics
# =========================
def get_valid_column_input(cols):
    """
    Prompt until the user enters a valid column letter (A.. up to COLS).
    The function returns the 0-based column index.
    Invalid characters (numbers, symbols, out-of-range letters) are rejected,
    but the turn is not lost; the user is re-prompted.
    """
    while True:
        user_input = input("Please enter a column: ").strip()
        if not user_input:
            print("Invalid input. Please enter a column letter.")
            continue

        # Accept both lowercase and uppercase, normalize to uppercase
        ch = user_input.upper()

        if len(ch) != 1 or not ch.isalpha():
            print("Invalid input. Enter a single letter (e.g., A, B, C).")
            continue

        col_index = ord(ch) - ord('A')
        if not (0 <= col_index < cols):
            max_letter = chr(ord('A') + cols - 1)
            print(f"Out of range. Enter a letter between A and {max_letter}.")
            continue

        return col_index


def drop_checker(board, col, checker):
    """
    Drop the checker into the given column.
    Returns the row index where it lands, or None if the column is full.
    """
    rows = len(board)
    # Start from bottom row, find first empty space
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return None  # Column full


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win(board, checker):
    """
    Check for a win (4 in a row) for the given checker across
    horizontal, vertical, and both diagonal directions.
    """
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (1, 1),   # down-right
        (1, -1),  # down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while count < 4 and in_bounds(nr, nc, rows, cols) and board[nr][nc] == checker:
                    count += 1
                    nr += dr
                    nc += dc
                if count == 4:
                    return True
    return False


def check_draw(board):
    """
    The game is a draw if no empty spaces remain.
    """
    for row in board:
        if " " in row:
            return False
    return True


# =========================
# Main Game Loop
# =========================
def main():
    board = create_board(ROWS, COLS)

    # Randomly select starting player index
    current_idx = random.randint(0, NUM_PLAYERS - 1)

    # Initial display
    clear_screen()
    print_board(board)
    print(f"Player {PLAYERS[current_idx]}, you start!")

    while True:
        current_checker = PLAYERS[current_idx]
        print(f"Player {current_checker}, please enter a column:")
        col = get_valid_column_input(COLS)

        # Attempt to drop the checker
        row_landed = drop_checker(board, col, current_checker)
        if row_landed is None:
            # Column full -> turn lost
            clear_screen()
            print_board(board)
            col_letter = chr(ord('A') + col)
            print(f"Column {col_letter} is full. Player {current_checker} loses the turn.")
            # Next player's turn
            current_idx = (current_idx + 1) % NUM_PLAYERS
            continue

        # After a valid move, check for win or draw
        if check_win(board, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        if check_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw.")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % NUM_PLAYERS

        # Clear and print updated board for the next turn
        clear_screen()
        print_board(board)

if __name__ == "__main__":
    main()
