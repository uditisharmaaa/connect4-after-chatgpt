import os
import random
import sys

# =========================
# Configuration constants
# =========================
ROWS = 6
COLS = 7            # Max 26
NUM_PLAYERS = 2     # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4       # Always 4 per assignment

# Validate configuration
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if COLS > 26:
    print("Maximum supported columns is 26 (A-Z).")
    sys.exit(1)
if ROWS <= 0 or COLS <= 0:
    print("ROWS and COLS must be positive.")
    sys.exit(1)

PLAYER_TOKENS = CHECKERS[:NUM_PLAYERS]

def clear_screen():
    try:
        os.system('clear')
    except Exception:
        pass

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def column_letters(cols):
    return [chr(ord('A') + i) for i in range(cols)]

def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    letters = column_letters(cols)

    # Header with column labels
    print("  " + "   ".join(letters))

    # Horizontal separator line
    sep = "+" + "+".join(["---"] * cols) + "+"

    # Rows
    for r in range(rows):
        print(sep)
        row_cells = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row_cells)
    print(sep)

def is_valid_column_input(s, cols):
    if len(s) != 1 or not s.isalpha():
        return False
    ch = s.upper()
    letters = column_letters(cols)
    return ch in letters

def col_index_from_letter(ch):
    return ord(ch.upper()) - ord('A')

def find_drop_row(board, col):
    # Return the row index where a checker will land, or None if column full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def drop_checker(board, col, token):
    row = find_drop_row(board, col)
    if row is None:
        return None
    board[row][col] = token
    return row

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, last_row, last_col, token):
    # Check 4 in a row including last placed token
    rows = len(board)
    cols = len(board[0])

    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for dr, dc in directions:
        count = 1  # include last placed
        # forward
        r, c = last_row + dr, last_col + dc
        while in_bounds(r, c, rows, cols) and board[r][c] == token:
            count += 1
            r += dr
            c += dc
        # backward
        r, c = last_row - dr, last_col - dc
        while in_bounds(r, c, rows, cols) and board[r][c] == token:
            count += 1
            r -= dr
            c -= dc

        if count >= WIN_COUNT:
            return True
    return False

def check_draw(board):
    # Draw if no spaces left
    for row in board:
        if " " in row:
            return False
    return True

def prompt_for_column(current_token, cols):
    while True:
        user_input = input(f"Player {current_token}, please enter a column: ").strip()
        if not is_valid_column_input(user_input, cols):
            print("Invalid input. Please enter a single letter within the board (e.g., A-G).")
            continue
        return col_index_from_letter(user_input)

def main():
    board = create_board(ROWS, COLS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)

    # Initial board print
    print_board(board)

    while True:
        current_token = PLAYER_TOKENS[current_player_index]

        # Show prompt with current board
        # Note: Board is already printed at loop start or after last action
        col = prompt_for_column(current_token, COLS)

        drop_row = find_drop_row(board, col)
        if drop_row is None:
            print(f"Column {chr(ord('A') + col)} is full. Player {current_token} loses the turn.")
            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            # Print board again for next turn
            print_board(board)
            continue

        # Place checker
        placed_row = drop_checker(board, col, current_token)

        # Print updated board
        print_board(board)

        # Check for win
        if check_win(board, placed_row, col, current_token):
            print(f"Player {current_token} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

    # End
    return

if __name__ == "__main__":
    main()
