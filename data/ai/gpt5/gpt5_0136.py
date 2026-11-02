import os
import random
import string
import sys

# Constants (adjustable within constraints; submission requires ROWS=6, COLS=7, NUM_PLAYERS=2)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # used in order

# Validate constants
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
COLUMN_LABELS = list(string.ascii_uppercase[:COLS])

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Header
    header = "  " + "   ".join(COLUMN_LABELS)
    print(header)
    # Grid
    sep = "+" + "+".join(["---"] * COLS) + "+"
    for r in range(ROWS):
        print(sep)
        row_cells = "|".join(f" {board[r][c]} " for c in range(COLS))
        print(f"|{row_cells}|")
    print(sep)

def col_from_input(s):
    s = s.strip().upper()
    if len(s) != 1 or s < 'A' or s > chr(ord('A') + COLS - 1):
        return None
    return ord(s) - ord('A')

def find_row_for_col(board, col):
    # Return the lowest available row index in the column; None if full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            return r
    return None

def check_win(board, last_r, last_c, symbol):
    # Check 4 in a row including the last placed piece
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for dr, dc in directions:
        count = 1
        # forward
        r, c = last_r + dr, last_c + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        # backward
        r, c = last_r - dr, last_c - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == ' ':
                return False
    return True

def main():
    board = create_board(ROWS, COLS)
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    winner = None

    while True:
        player_symbol = PLAYERS[current_player_idx]
        print(f"Player {player_symbol}, please enter a column:")
        user_in = input("> ")

        # Validate input (format and bounds). Re-prompt on invalid input.
        col = col_from_input(user_in)
        while col is None:
            print(f"Invalid input. Please enter a column between {COLUMN_LABELS[0]} and {COLUMN_LABELS[-1]}.")
            print(f"Player {player_symbol}, please enter a column:")
            user_in = input("> ")
            col = col_from_input(user_in)

        # Determine placement
        row = find_row_for_col(board, col)
        if row is None:
            # Column full -> turn is invalid and player loses the turn
            print(f"Column {COLUMN_LABELS[col]} is full. Turn lost.")
            # Next player's turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue

        # Place checker
        board[row][col] = player_symbol
        print_board(board)

        # Check for win
        if check_win(board, row, col, player_symbol):
            print(f"Player {player_symbol} won!")
            winner = player_symbol
            break

        # Check for draw
        if is_draw(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

    # Game over
    # Nothing else to print per assignment requirements

if __name__ == "__main__":
    try:
        # Show initial board and randomly selected starting player happens in main
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted.")
        sys.exit(0)
