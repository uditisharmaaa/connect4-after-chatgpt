import os
import random
import string

# Constants (can be adjusted; submission requires ROWS=6, COLS=7, NUM_PLAYERS=2)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]

# Safety checks for constraints
if COLS > 26:
    COLS = 26
if NUM_PLAYERS < 2:
    NUM_PLAYERS = 2
if NUM_PLAYERS > 5:
    NUM_PLAYERS = 5

PLAYERS = CHECKERS[:NUM_PLAYERS]
COLUMN_LABELS = list(string.ascii_uppercase[:COLS])


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    # Header with column labels
    header = "  " + "   ".join(COLUMN_LABELS)
    sep = "+" + "+".join(["---"] * COLS) + "+"
    print(header)
    print(sep)
    for r in range(ROWS):
        row_cells = []
        for c in range(COLS):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print(sep)


def find_drop_row(board, col_index):
    # Return the row index where the checker will land, or None if column is full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col_index] == " ":
            return r
    return None


def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS


def check_direction(board, start_r, start_c, dr, dc, symbol):
    count = 0
    r, c = start_r, start_c
    while in_bounds(r, c) and board[r][c] == symbol:
        count += 1
        if count == 4:
            return True
        r += dr
        c += dc
    return False


def check_win(board, symbol):
    # Check all cells as potential starts
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != symbol:
                continue
            # Right (horizontal)
            if check_direction(board, r, c, 0, 1, symbol):
                return True
            # Down (vertical)
            if check_direction(board, r, c, 1, 0, symbol):
                return True
            # Down-right (diagonal)
            if check_direction(board, r, c, 1, 1, symbol):
                return True
            # Down-left (diagonal)
            if check_direction(board, r, c, 1, -1, symbol):
                return True
    return False


def is_draw(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True


def get_valid_column_input():
    while True:
        user_in = input("Please enter a column: ").strip()
        if len(user_in) != 1:
            print("Invalid input. Enter a single letter for the column.")
            continue
        ch = user_in.upper()
        if ch not in COLUMN_LABELS:
            print("Invalid column. Choose from: " + ", ".join(COLUMN_LABELS))
            continue
        return ch


def main():
    board = create_board(ROWS, COLS)
    current_player_index = random.randrange(NUM_PLAYERS)

    # Initial print
    clear_screen()
    print_board(board)
    print(f"Player {PLAYERS[current_player_index]}, please enter a column:")

    while True:
        # Get valid column letter (re-prompt on invalid entry; do not lose turn)
        col_letter = get_valid_column_input()
        col_index = COLUMN_LABELS.index(col_letter)

        # Try to place the checker
        drop_row = find_drop_row(board, col_index)
        if drop_row is None:
            # Column full: lose turn
            print(f"Column {col_letter} is full. You lose your turn.")
            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
        else:
            # Place the checker
            symbol = PLAYERS[current_player_index]
            board[drop_row][col_index] = symbol

            # Check for win
            if check_win(board, symbol):
                clear_screen()
                print_board(board)
                print(f"Player {symbol} won!")
                break

            # Check for draw
            if is_draw(board):
                clear_screen()
                print_board(board)
                print("It's a draw!")
                break

            # Next player's turn
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

        # Print updated board and prompt next player
        clear_screen()
        print_board(board)
        print(f"Player {PLAYERS[current_player_index]}, please enter a column:")


if __name__ == "__main__":
    main()
