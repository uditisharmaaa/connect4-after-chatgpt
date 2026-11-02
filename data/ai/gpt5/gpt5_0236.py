import os
import random
import string
import sys

# -----------------------------
# Configuration (Change allowed for testing; submission requires these values)
ROWS = 6
COLUMNS = 7           # Max 26
NUM_PLAYERS = 2       # Between 2 and 5
WIN_LENGTH = 4        # Always 4 as per assignment
CHECKER_SYMBOLS = ["X", "O", "V", "H", "M"]
# -----------------------------

def clear_screen():
    # Clear terminal screen (Linux/Unix)
    os.system('clear')

def validate_config(rows, cols, num_players):
    if cols < 1 or cols > 26:
        raise ValueError("COLUMNS must be between 1 and 26.")
    if rows < 1:
        raise ValueError("ROWS must be at least 1.")
    if num_players < 2 or num_players > 5:
        raise ValueError("NUM_PLAYERS must be between 2 and 5.")

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def get_col_labels(cols):
    # Labels A, B, C, ... up to cols
    return list(string.ascii_uppercase[:cols])

def print_board(board, col_labels):
    # Column header
    header = "  " + "   ".join(col_labels)
    sep = "+" + "+".join(["---"] * len(col_labels)) + "+"

    print(header)
    print(sep)
    for r in range(len(board)):
        row_str = "|"
        for c in range(len(board[0])):
            row_str += " " + board[r][c] + " |"
        print(row_str)
        print(sep)

def first_empty_row_in_col(board, col_idx):
    # Returns the bottom-most empty row index in the given column, or None if full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_idx] == " ":
            return r
    return None

def drop_checker(board, col_idx, symbol):
    # Place the symbol in the lowest available cell in the column
    r = first_empty_row_in_col(board, col_idx)
    if r is None:
        return None
    board[r][col_idx] = symbol
    return r

def check_direction(board, start_r, start_c, dr, dc, symbol, win_len):
    rows = len(board)
    cols = len(board[0])
    r, c = start_r, start_c
    for k in range(win_len):
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if board[r][c] != symbol:
            return False
        r += dr
        c += dc
    return True

def check_win(board, symbol, win_len=WIN_LENGTH):
    rows = len(board)
    cols = len(board[0])
    # Check all cells as potential start for 4-in-a-row in any of 4 directions
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
                if check_direction(board, r, c, dr, dc, symbol, win_len):
                    return True
    return False

def board_full(board):
    # If any top row cell is empty, board is not full (or more generally, any empty anywhere)
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True

def prompt_for_column(col_labels, player_symbol):
    # Keep asking until input format is valid and within board range.
    # If format invalid, reprompt; if column is valid but full, the turn is lost elsewhere.
    while True:
        inp = input(f"Player {player_symbol}, please enter a column: ").strip()
        if len(inp) != 1:
            print("Invalid input. Please enter a single uppercase letter corresponding to a column.")
            continue
        ch = inp.upper()
        if ch not in col_labels:
            print(f"Invalid column. Please choose from {col_labels[0]} to {col_labels[-1]}.")
            continue
        return col_labels.index(ch)

def game_loop(rows, cols, num_players):
    symbols = CHECKER_SYMBOLS[:num_players]
    col_labels = get_col_labels(cols)
    board = create_board(rows, cols)

    # Randomly select starting player
    current_idx = random.randrange(num_players)

    # Initial display
    clear_screen()
    print_board(board, col_labels)

    while True:
        player_symbol = symbols[current_idx]
        # Prompt for column (validate input format and range)
        col_idx = prompt_for_column(col_labels, player_symbol)

        # Attempt to place checker
        placed_row = drop_checker(board, col_idx, player_symbol)
        if placed_row is None:
            # Column full: invalid turn, player loses turn
            clear_screen()
            print_board(board, col_labels)
            print(f"Column {col_labels[col_idx]} is full. Player {player_symbol} loses the turn.")
            # Next player's turn
            current_idx = (current_idx + 1) % num_players
            # Continue without win/draw check since no move placed
            continue

        # Successful placement: update display
        clear_screen()
        print_board(board, col_labels)

        # Check for win
        if check_win(board, player_symbol, WIN_LENGTH):
            print(f"Player {player_symbol} won!")
            return

        # Check for draw
        if board_full(board):
            print("It's a draw!")
            return

        # Next player's turn
        current_idx = (current_idx + 1) % num_players

def main():
    try:
        validate_config(ROWS, COLUMNS, NUM_PLAYERS)
    except ValueError as e:
        print("Configuration error:", e, file=sys.stderr)
        sys.exit(1)

    # Start game
    # Before the game starts, board is shown via initial rendering in game_loop
    game_loop(ROWS, COLUMNS, NUM_PLAYERS)

if __name__ == "__main__":
    main()
