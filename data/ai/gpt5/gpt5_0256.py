import os
import random
import string
import sys

# === Configuration constants ===
ROWS = 6
COLS = 7  # Max 26 (A-Z)
NUM_PLAYERS = 2  # Supported range: 2..5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4  # Always 4 per assignment

# === Validation of constants ===
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if not (1 <= COLS <= 26):
    print("COLS must be between 1 and 26.")
    sys.exit(1)
if ROWS <= 0:
    print("ROWS must be a positive integer.")
    sys.exit(1)

ACTIVE_PLAYERS = PLAYER_SYMBOLS[:NUM_PLAYERS]


def clear_screen():
    # Clear terminal screen (Linux/Unix)
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header with column letters
    letters = string.ascii_uppercase[:cols]
    print("  " + "   ".join(letters))

    # Horizontal line segment
    horiz = "+---" * cols + "+"

    for r in range(rows):
        print(horiz)
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
    print(horiz)


def is_valid_column_letter(inp, cols):
    if len(inp) != 1:
        return False
    if inp < 'A' or inp > chr(ord('A') + cols - 1):
        return False
    return True


def find_drop_row(board, col):
    # Return the row index where a checker will land in given column, or None if column is full
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def place_checker(board, col, symbol):
    # Place checker and return row index, or None if column full
    r = find_drop_row(board, col)
    if r is None:
        return None
    board[r][col] = symbol
    return r


def check_win_from(board, start_r, start_c, symbol, win_len=WIN_LENGTH):
    rows = len(board)
    cols = len(board[0])

    # Directions: (dr, dc)
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diag down-right
        (-1, 1),  # diag up-right
    ]

    for dr, dc in directions:
        count = 1

        # forward
        r, c = start_r + dr, start_c + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc

        # backward
        r, c = start_r - dr, start_c - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc

        if count >= win_len:
            return True

    return False


def is_draw(board):
    # Draw if no empty spaces remain
    for row in board:
        if " " in row:
            return False
    return True


def game_loop():
    board = create_board(ROWS, COLS)
    current_player_idx = random.randrange(len(ACTIVE_PLAYERS))

    while True:
        print_board(board)
        current_symbol = ACTIVE_PLAYERS[current_player_idx]
        try:
            # Input validation: repeat until a valid column letter (existing column)
            while True:
                user_inp = input(f"Player {current_symbol}, please enter a column: ").strip().upper()
                if is_valid_column_letter(user_inp, COLS):
                    break
                else:
                    print(f"Invalid input. Please enter a letter between A and {chr(ord('A') + COLS - 1)}.")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting game.")
            return

        col = ord(user_inp) - ord('A')

        # If column full, turn is invalid and player loses the turn
        if board[0][col] != " ":
            print(f"Column {user_inp} is full. Turn lost.")
            input("Press Enter to continue...")
            current_player_idx = (current_player_idx + 1) % len(ACTIVE_PLAYERS)
            continue

        # Place checker
        placed_row = place_checker(board, col, current_symbol)

        # Safety check (should not happen because top checked above)
        if placed_row is None:
            print(f"Column {user_inp} is full. Turn lost.")
            input("Press Enter to continue...")
            current_player_idx = (current_player_idx + 1) % len(ACTIVE_PLAYERS)
            continue

        # Check for win
        if check_win_from(board, placed_row, col, current_symbol):
            print_board(board)
            print(f"Player {current_symbol} won!")
            return

        # Check for draw
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            return

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % len(ACTIVE_PLAYERS)


if __name__ == "__main__":
    # Start the game
    game_loop()
