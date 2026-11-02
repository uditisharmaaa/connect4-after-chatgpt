import os
import random
import string
import sys

# ====== Configuration (you may change these for testing; submission requires 6x7 and 2 players) ======
ROWS = 6
COLS = 7     # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]  # In order; only first NUM_PLAYERS used
CONNECT_N = 4  # Always 4 per assignment
# =====================================================================================================

# Safety checks for configuration
if COLS < 1 or COLS > 26:
    print("Error: COLS must be between 1 and 26.")
    sys.exit(1)
if ROWS < 1:
    print("Error: ROWS must be at least 1.")
    sys.exit(1)
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    print("Error: NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)

PLAYERS = CHECKERS[:NUM_PLAYERS]


def clear_screen():
    # Clear the screen as required by the assignment
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def column_labels(cols):
    # Labels are A, B, C, ...
    return list(string.ascii_uppercase[:cols])


def print_board(board):
    rows = len(board)
    cols = len(board[0])
    labels = column_labels(cols)

    # Header with column labels
    header = "  " + "   ".join(labels)
    sep = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep)
    for r in range(rows):
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
        print(sep)


def get_valid_column_input(cols, current_player):
    labels = column_labels(cols)
    valid_set = set(labels)

    while True:
        try:
            user_in = input(f"Player {current_player}, please enter a column: ").strip().upper()
        except EOFError:
            # End of input stream -> exit gracefully
            print()
            sys.exit(0)

        if len(user_in) != 1 or user_in not in valid_set:
            print("Invalid input. Please enter a single uppercase letter within the board range.")
            continue
        return labels.index(user_in)


def place_checker(board, col, checker):
    # Place checker in the lowest empty spot in the given column
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r
    return None  # Column full


def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols


def check_win(board, checker, connect_n=4):
    rows = len(board)
    cols = len(board[0])

    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                nr, nc = r + dr, c + dc
                while count < connect_n and in_bounds(nr, nc, rows, cols) and board[nr][nc] == checker:
                    count += 1
                    nr += dr
                    nc += dc
                if count >= connect_n:
                    return True
    return False


def is_draw(board):
    # Draw if no empty spaces in top row (or anywhere)
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def game():
    board = create_board(ROWS, COLS)
    start_index = random.randrange(NUM_PLAYERS)
    current_index = start_index

    # Initial screen
    clear_screen()
    print_board(board)

    while True:
        current_player = PLAYERS[current_index]
        # Prompt and validate input
        col = get_valid_column_input(COLS, current_player)

        # Attempt to place checker
        row_placed = place_checker(board, col, current_player)

        # Clear and print after the attempted move (as per requirement)
        clear_screen()

        if row_placed is None:
            # Column full, turn is invalid and player loses the turn
            print_board(board)
            print(f"Column {column_labels(COLS)[col]} is full. Player {current_player} loses the turn.")
            # Advance to next player
            current_index = (current_index + 1) % NUM_PLAYERS
            continue

        # Successfully placed
        print_board(board)

        # Check win
        if check_win(board, current_player, CONNECT_N):
            print(f"Player {current_player} won!")
            break

        # Check draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_index = (current_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    game()
