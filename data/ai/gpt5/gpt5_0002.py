import os
import random
import sys

# Constants (configure here)
ROWS = 6                # number of rows (default 6)
COLS = 7                # number of columns (default 7, max 26)
NUM_PLAYERS = 2         # number of players (2..5)
CHECKERS = ["X", "O", "V", "H", "M"]  # in order of assignment to players

# Validations for constants
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if COLS > 26:
    print("COLS cannot be greater than 26.")
    sys.exit(1)
if ROWS <= 0 or COLS <= 0:
    print("ROWS and COLS must be positive.")
    sys.exit(1)
if NUM_PLAYERS > len(CHECKERS):
    print("Not enough checker symbols for the number of players.")
    sys.exit(1)

PLAYER_SYMBOLS = CHECKERS[:NUM_PLAYERS]


def clear_screen():
    """Clear the terminal screen (Linux/Unix)."""
    os.system('clear')


def create_board(rows, cols):
    """Create a 2D board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Print the board formatted as specified."""
    rows = len(board)
    cols = len(board[0])

    # Header with column letters
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(header)

    # Top border
    border = "+" + "+".join("---" for _ in range(cols)) + "+"
    for r in range(rows):
        print(border)
        # Row content
        row_str = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row_str)
    print(border)


def next_open_row(board, col):
    """Return the index of the lowest open row in the given column, or None if full."""
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def drop_checker(board, col, symbol):
    """Place the checker in the lowest available row of the given column. Return row or None if full."""
    r = next_open_row(board, col)
    if r is None:
        return None
    board[r][col] = symbol
    return r


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win(board, symbol):
    """Check all directions for a 4-in-a-row for the given symbol."""
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while count < 4 and in_bounds(nr, nc, rows, cols) and board[nr][nc] == symbol:
                    count += 1
                    nr += dr
                    nc += dc
                if count >= 4:
                    return True
    return False


def board_full(board):
    """Return True if the board is full (no spaces in the top row)."""
    return all(cell != " " for cell in board[0])


def get_valid_column_input(cols):
    """
    Prompt user until a valid column letter (within range A..A+cols-1) is entered.
    Returns zero-based column index.
    """
    while True:
        user_in = input().strip().upper()
        if len(user_in) != 1 or not ('A' <= user_in <= 'Z'):
            print("Invalid input. Please enter a valid column letter.")
            continue
        col = ord(user_in) - ord('A')
        if not (0 <= col < cols):
            print("Input out of board range. Please enter a valid column letter.")
            continue
        return col


def main():
    random.seed()

    board = create_board(ROWS, COLS)

    # Randomly choose starting player index
    current_player_idx = random.randrange(NUM_PLAYERS)

    # Initial screen
    clear_screen()
    print_board(board)
    # Main game loop
    while True:
        current_symbol = PLAYER_SYMBOLS[current_player_idx]
        print(f"Player {current_symbol}, please enter a column:")
        col = get_valid_column_input(COLS)

        # Try to place the checker
        placed_row = drop_checker(board, col, current_symbol)
        if placed_row is None:
            # Column full -> invalid turn, player loses the turn
            clear_screen()
            print_board(board)
            # Advance to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            # Check for draw (not strictly necessary here but safe)
            if board_full(board):
                print("It's a draw!")
                break
            continue

        # After a successful move, clear screen and print updated board
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check for draw
        if board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
