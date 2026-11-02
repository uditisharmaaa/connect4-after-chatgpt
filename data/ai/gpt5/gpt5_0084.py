import os
import random
import string
import sys

# ========= Configuration (you can change these constants for testing) =========
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4
# ============================================================================

def clear_screen():
    # Clear terminal screen (Linux/Unix)
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def get_player_symbols(num_players):
    if not (2 <= num_players <= 5):
        raise ValueError("Number of players must be between 2 and 5.")
    return CHECKERS[:num_players]

def choose_start_player(num_players):
    return random.randrange(num_players)

def column_labels(cols):
    # Labels A.. up to 26 columns
    if cols > 26:
        raise ValueError("Maximum supported columns is 26.")
    return list(string.ascii_uppercase[:cols])

def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    labels = column_labels(cols)

    # Header
    header = "  " + "   ".join(labels)
    sep = "+" + "+".join(["---"] * cols) + "+"

    clear_screen()
    print(header)
    print(sep)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print(sep)

def validate_input(inp, cols):
    if not inp:
        return None
    ch = inp.strip().upper()
    if len(ch) != 1:
        return None
    labels = column_labels(cols)
    if ch not in labels:
        return None
    return labels.index(ch)

def drop_checker(board, col, symbol):
    # Place symbol in the lowest available slot in the given column.
    # Returns the row index where it was placed, or None if column full.
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return r
    return None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, symbol):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    w = WIN_LENGTH

    # Directions: (dr, dc)
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diag down-right
        (1, -1),  # diag down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != symbol:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r, c
                for _ in range(w - 1):
                    rr += dr
                    cc += dc
                    if in_bounds(rr, cc, rows, cols) and board[rr][cc] == symbol:
                        count += 1
                    else:
                        break
                if count >= w:
                    return True
    return False

def check_draw(board):
    # Draw if no empty spaces remain
    for row in board:
        if " " in row:
            return False
    return True

def prompt_for_column(current_symbol, cols):
    while True:
        try:
            user_inp = input(f"Player {current_symbol}, please enter a column: ").strip()
        except EOFError:
            # Gracefully handle EOF (treat as invalid input, reprompt)
            user_inp = ""
        idx = validate_input(user_inp, cols)
        if idx is not None:
            return idx
        # invalid input, reprompt without losing turn
        print("Invalid input. Enter a single uppercase letter for a valid column (e.g., A, B, ...).")

def main():
    # Validate configuration
    if COLS > 26:
        print("Error: COLS cannot exceed 26.", file=sys.stderr)
        sys.exit(1)
    if not (2 <= NUM_PLAYERS <= 5):
        print("Error: NUM_PLAYERS must be between 2 and 5.", file=sys.stderr)
        sys.exit(1)

    board = create_board(ROWS, COLS)
    symbols = get_player_symbols(NUM_PLAYERS)
    current = choose_start_player(NUM_PLAYERS)

    # Initial board print
    print_board(board)
    print(f"Player {symbols[current]} will start.")

    while True:
        # Show current board before move
        print_board(board)
        current_symbol = symbols[current]

        col_index = prompt_for_column(current_symbol, COLS)
        placed_row = drop_checker(board, col_index, current_symbol)

        # After attempting to place, print updated board
        print_board(board)

        if placed_row is None:
            # Column full: turn is invalid and player loses the turn
            print(f"Column {column_labels(COLS)[col_index]} is full. Player {current_symbol} loses the turn.")
        else:
            # Check for win
            if check_win(board, current_symbol):
                print(f"Player {current_symbol} won!")
                break
            # Check for draw
            if check_draw(board):
                print("The game is a draw!")
                break

        # Next player's turn
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
