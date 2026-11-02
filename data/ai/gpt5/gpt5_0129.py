import os
import random
import sys

# Constants (you may change ROWS, COLS, NUM_PLAYERS for testing; final submission requires 6x7 and 2 players)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5
WIN_LENGTH = 4

CHECKERS_ORDER = ["X", "O", "V", "H", "M"]  # in order

# Safety checks for constraints
if COLS > 26:
    print("Maximum supported columns is 26.")
    sys.exit(1)
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    print("Number of players must be between 2 and 5.")
    sys.exit(1)

PLAYERS = CHECKERS_ORDER[:NUM_PLAYERS]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Header letters
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(header)

    # Top border
    border = "+" + "+".join(["---"] * cols) + "+"
    for r in range(rows):
        print(border)
        row_cells = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row_cells)
    print(border)


def col_letter_to_index(s):
    # Returns index or None if invalid
    if len(s) != 1:
        return None
    ch = s.upper()
    if not ('A' <= ch <= 'Z'):
        return None
    idx = ord(ch) - ord('A')
    return idx


def get_valid_column_input(cols):
    while True:
        user_input = input("Please enter a column: ").strip()
        idx = col_letter_to_index(user_input)
        if idx is None:
            print("Invalid input. Enter a single letter for the column (e.g., A, B, C).")
            continue
        if idx < 0 or idx >= cols:
            print("Column out of range. Please enter a valid column letter on the board.")
            continue
        return idx


def drop_checker(board, col, checker):
    # Place checker in the lowest empty spot in the column.
    # Returns the row index where placed, or None if column full.
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return None


def count_in_direction(board, start_r, start_c, dr, dc, checker):
    rows = len(board)
    cols = len(board[0])
    r = start_r + dr
    c = start_c + dc
    count = 0
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += dr
        c += dc
    return count


def check_win(board, r, c, checker):
    # Check all 4 directions using the last placed position (r, c)
    # Directions: horizontal (0,1), vertical (1,0), diag1 (1,1), diag2 (1,-1)
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        total = 1  # include the placed checker
        total += count_in_direction(board, r, c, dr, dc, checker)
        total += count_in_direction(board, r, c, -dr, -dc, checker)
        if total >= WIN_LENGTH:
            return True
    return False


def is_draw(board):
    # Draw if no spaces in top row (or whole board)
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True


def game_loop():
    board = create_board(ROWS, COLS)
    current_player_index = random.randrange(NUM_PLAYERS)

    # Initial display
    clear_screen()
    print_board(board)
    print(f"Player {PLAYERS[current_player_index]}, you start!")

    while True:
        checker = PLAYERS[current_player_index]

        # Show board before asking for input
        print(f"Player {checker}, please enter a column:")
        col = get_valid_column_input(COLS)

        row_placed = drop_checker(board, col, checker)

        if row_placed is None:
            # Column full: lose the turn
            clear_screen()
            print_board(board)
            print(f"Column {chr(ord('A') + col)} is full. Player {checker} loses the turn.")
            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        # After a successful placement, clear and show updated board
        clear_screen()
        print_board(board)

        # Check for win
        if check_win(board, row_placed, col, checker):
            print(f"Player {checker} won!")
            break

        # Check for draw
        if is_draw(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    game_loop()
