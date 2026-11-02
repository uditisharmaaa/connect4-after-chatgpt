import os
import random
import string

# Constants (adjustable, but keep COLS <= 26 and 2 <= NUM_PLAYERS <= 5)
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Checker symbols in the required order
CHECKERS = ["X", "O", "V", "H", "M"]

# Validate constant constraints
assert 2 <= NUM_PLAYERS <= 5, "Number of players must be between 2 and 5."
assert COLS <= 26, "Maximum number of columns is 26 (A-Z)."

# Select the checker symbols for the current game
PLAYER_SYMBOLS = CHECKERS[:NUM_PLAYERS]


def clear_screen():
    """Clear the terminal screen (Linux/Unix as per assignment)."""
    os.system('clear')


def create_board(rows, cols):
    """Create a rows x cols board initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Print the board with column headers and grid lines."""
    rows = len(board)
    cols = len(board[0])

    # Column headers (A, B, C, ...)
    header_letters = string.ascii_uppercase[:cols]
    header_line = "  " + "   ".join(header_letters)
    # Horizontal border
    border = "+" + "+".join(["---"] * cols) + "+"

    print(header_line)
    print(border)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(f" {board[r][c]} ")
        print("|" + "|".join(row_cells) + "|")
        print(border)


def find_next_open_row(board, col):
    """Return the bottom-most open row index in the given column, or None if full."""
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def is_board_full(board):
    """Return True if the board is full (no spaces in the top row)."""
    top_row = board[0]
    return all(cell != " " for cell in top_row)


def check_win_from(board, row, col, symbol):
    """
    Check if placing 'symbol' at (row, col) creates a 4-in-a-row
    horizontally, vertically, or diagonally.
    """
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1  # count current piece
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc

        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc

        if count >= 4:
            return True

    return False


def get_column_input(cols, current_symbol):
    """
    Prompt the user for a valid column letter input.
    Invalid inputs (non-letter, out of range) are rejected until valid.
    Returns the zero-based column index.
    """
    valid_letters = string.ascii_uppercase[:cols]
    prompt = f"Player {current_symbol}, please enter a column: "

    while True:
        user_input = input(prompt).strip().upper()
        if len(user_input) != 1 or user_input not in valid_letters:
            # Invalid input, ask again (turn is not lost)
            continue
        return valid_letters.index(user_input)


def game_loop():
    """Main game loop: initialize, play turns, check for win/draw, and end."""
    board = create_board(ROWS, COLS)

    # Randomly choose starting player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    # Initial display (show board before first move)
    clear_screen()
    print_board(board)

    while True:
        current_symbol = PLAYER_SYMBOLS[current_player_idx]

        # Get a valid column letter from the player
        col = get_column_input(COLS, current_symbol)

        # Attempt to place checker; if column is full, player loses the turn
        next_row = find_next_open_row(board, col)
        if next_row is None:
            # Column full -> invalid turn, player loses turn
            print(f"Column {string.ascii_uppercase[col]} is full. Player {current_symbol} loses the turn.")
            input("Press Enter to continue...")
            # Next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            clear_screen()
            print_board(board)
            continue

        # Place the checker
        board[next_row][col] = current_symbol

        # After placement, clear screen and print updated board
        clear_screen()
        print_board(board)

        # Check for win
        if check_win_from(board, next_row, col, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check for draw
        if is_board_full(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    game_loop()
