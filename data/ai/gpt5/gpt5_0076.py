import os
import random
import sys

# ------------ Configuration (submission should use 6 rows x 7 columns, 2 players) ------------
ROWS = 6
COLS = 7  # Max 26 (A-Z)
NUM_PLAYERS = 2  # Between 2 and 5

# Player checker symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# ------------- Validation of configuration -------------
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if not (1 <= COLS <= 26):
    print("COLS must be between 1 and 26.")
    sys.exit(1)
if ROWS < 1:
    print("ROWS must be at least 1.")
    sys.exit(1)

SYMBOLS_IN_PLAY = PLAYER_SYMBOLS[:NUM_PLAYERS]


# ------------- Game Functions -------------

def clear_screen():
    # Requirement: use os.system('clear') to clear the game screen before printing the board
    os.system('clear')


def create_board(rows, cols):
    # Create a board initialized with spaces
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header with column letters
    header_letters = [chr(ord('A') + i) for i in range(cols)]
    header_line = "  " + "   ".join(header_letters)
    print(header_line)

    # Horizontal separator
    sep = "+" + "+".join(["---"] * cols) + "+"

    # Rows
    for r in range(rows):
        print(sep)
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
    print(sep)


def next_player_index(current_index, total_players):
    return (current_index + 1) % total_players


def column_from_input(user_input, cols):
    """
    Convert a single-letter input to a column index (0-based).
    Returns an integer column index if valid, otherwise None.
    """
    s = user_input.strip().upper()
    if len(s) != 1:
        return None
    ch = s[0]
    if 'A' <= ch <= chr(ord('A') + cols - 1):
        return ord(ch) - ord('A')
    return None


def prompt_for_column(player_symbol, cols):
    """
    Prompt the player until a syntactically valid column letter (within the board) is entered.
    Does not check for full column (turn is lost in that case by separate rule).
    """
    while True:
        try:
            user_input = input(f"Player {player_symbol}, please enter a column: ")
        except EOFError:
            # If input stream ends unexpectedly, exit gracefully
            print()
            sys.exit(0)
        col = column_from_input(user_input, cols)
        if col is not None:
            return col
        print("Invalid input. Please enter a single letter within the board (e.g., A, B, C...).")


def find_drop_row(board, col):
    """
    Given a column, find the lowest available row to drop the checker.
    Returns the row index, or None if the column is full.
    """
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def place_checker(board, col, symbol):
    """
    Attempts to place a checker in the specified column.
    Returns (row, col) if successful, or None if the column is full.
    """
    row = find_drop_row(board, col)
    if row is None:
        return None
    board[row][col] = symbol
    return (row, col)


def in_bounds(board, r, c):
    return 0 <= r < len(board) and 0 <= c < len(board[0])


def check_direction(board, start_r, start_c, dr, dc, target, needed=4):
    """
    Count consecutive target symbols starting from (start_r, start_c) in both directions (dr, dc) and (-dr, -dc).
    Returns True if count >= needed, else False.
    """
    count = 1  # include the starting position

    # Forward direction
    r, c = start_r + dr, start_c + dc
    while in_bounds(board, r, c) and board[r][c] == target:
        count += 1
        r += dr
        c += dc

    # Backward direction
    r, c = start_r - dr, start_c - dc
    while in_bounds(board, r, c) and board[r][c] == target:
        count += 1
        r -= dr
        c -= dc

    return count >= needed


def check_win(board, last_move, needed=4):
    """
    Check if the last move resulted in a win.
    last_move is a tuple (row, col). If last_move is None, no win.
    """
    if last_move is None:
        return False
    r, c = last_move
    target = board[r][c]
    if target == " ":
        return False

    # Directions: horizontal, vertical, diag down-right, diag up-right
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for dr, dc in directions:
        if check_direction(board, r, c, dr, dc, target, needed):
            return True
    return False


def board_full(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def run_game(rows, cols, symbols):
    board = create_board(rows, cols)

    # Randomly select first player
    current_player_idx = random.randint(0, len(symbols) - 1)

    # Initial board print
    print_board(board)

    winner = None

    while True:
        player_symbol = symbols[current_player_idx]

        # Prompt for input (validated to be within A..)
        col = prompt_for_column(player_symbol, cols)

        # Try to place checker
        move = place_checker(board, col, player_symbol)
        if move is None:
            # Column full: invalid turn, player loses the turn
            print(f"Column {chr(ord('A') + col)} is full. Player {player_symbol} loses the turn.")
            # Pause briefly for user to read message
            try:
                input("Press Enter to continue...")
            except EOFError:
                pass
            # Print board again (unchanged)
            print_board(board)
            # Next player
            current_player_idx = next_player_index(current_player_idx, len(symbols))
            continue

        # After successful placement, print updated board
        print_board(board)

        # Check for win
        if check_win(board, move, needed=4):
            winner = player_symbol
            print(f"Player {winner} won!")
            break

        # Check for draw
        if board_full(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = next_player_index(current_player_idx, len(symbols))


def main():
    run_game(ROWS, COLS, SYMBOLS_IN_PLAY)


if __name__ == "__main__":
    main()
