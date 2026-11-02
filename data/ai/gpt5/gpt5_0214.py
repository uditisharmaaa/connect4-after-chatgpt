import os
import random
import sys

# Constants (change these for different configurations; submission requires 6x7 and 2 players)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
WIN_LENGTH = 4

CHECKERS = ["X", "O", "V", "H", "M"]  # In order

# Basic validations for constants
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if COLS > 26 or COLS < 1:
    print("COLS must be between 1 and 26.")
    sys.exit(1)
if ROWS < 1:
    print("ROWS must be at least 1.")
    sys.exit(1)

PLAYERS = CHECKERS[:NUM_PLAYERS]


def clear_screen():
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    # Labels A, B, C, ...
    return [chr(ord('A') + i) for i in range(cols)]


def print_board(board):
    labels = column_labels(len(board[0]))
    # Header with column labels
    print("  " + "   ".join(labels))
    # Rows
    sep = "+" + ("---+" * len(board[0]))
    for r in range(len(board)):
        print(sep)
        line = ""
        for c in range(len(board[0])):
            line += f"| {board[r][c]} "
        line += "|"
        print(line)
    print(sep)


def input_column(current_player, cols):
    labels = column_labels(cols)
    valid_set = set(labels)
    while True:
        try:
            user_in = input(f"Player {current_player}, please enter a column: ").strip()
        except EOFError:
            # Graceful exit on EOF
            print()
            sys.exit(0)
        if len(user_in) != 1:
            print("Invalid input. Please enter a single uppercase letter corresponding to a column.")
            continue
        c = user_in.upper()
        if c not in valid_set:
            print(f"Invalid column. Please enter one of: {', '.join(labels)}")
            continue
        return ord(c) - ord('A')


def find_row_for_col(board, col):
    # Place from bottom (last row) upwards
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None  # Column full


def place_checker(board, row, col, checker):
    board[row][col] = checker


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win(board):
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    for r in range(rows):
        for c in range(cols):
            ch = board[r][c]
            if ch == " ":
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r, c
                for _ in range(WIN_LENGTH - 1):
                    nr += dr
                    nc += dc
                    if not in_bounds(nr, nc, rows, cols):
                        break
                    if board[nr][nc] != ch:
                        break
                    count += 1
                if count >= WIN_LENGTH:
                    return ch  # Return the winning checker
    return None


def check_draw(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def main():
    board = create_board(ROWS, COLS)
    current_index = random.randint(0, NUM_PLAYERS - 1)
    clear_screen()
    print_board(board)

    while True:
        current_player = PLAYERS[current_index]
        # Prompt and get a valid column letter
        col = input_column(current_player, COLS)
        row = find_row_for_col(board, col)

        if row is None:
            # Column full - lose turn
            clear_screen()
            print_board(board)
            print(f"Column {chr(ord('A') + col)} is full. Player {current_player} loses the turn.")
            # Next player
            current_index = (current_index + 1) % NUM_PLAYERS
            continue

        # Place checker
        place_checker(board, row, col, current_player)

        # Clear and print updated board
        clear_screen()
        print_board(board)

        # Check for win
        winner = check_win(board)
        if winner is not None:
            print(f"Player {winner} won!")
            break

        # Check for draw
        if check_draw(board):
            print("It's a draw!")
            break

        # Next player
        current_index = (current_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
