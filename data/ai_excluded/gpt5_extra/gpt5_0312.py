import os
import random
import string
import sys

# Constants (submission requires 6 rows x 7 cols and 2 players enabled)
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Supports 2 to 5

# Validate constraints
if not (2 <= NUM_PLAYERS <= 5):
    print("NUM_PLAYERS must be between 2 and 5.")
    sys.exit(1)
if not (1 <= COLS <= 26):
    print("COLS must be between 1 and 26.")
    sys.exit(1)
if ROWS < 1:
    print("ROWS must be at least 1.")
    sys.exit(1)

CHECKERS_ALL = ["X", "O", "V", "H", "M"]
CHECKERS = CHECKERS_ALL[:NUM_PLAYERS]


def clear_screen():
    # Clear terminal screen
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Header with column letters
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    sep = "+" + "+".join(["---"] * cols) + "+"
    print(header)
    print(sep)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
        print(sep)


def is_valid_column_input(inp, cols):
    if not inp or len(inp) != 1:
        return False
    ch = inp.upper()
    if ch < 'A' or ch >= chr(ord('A') + cols):
        return False
    return True


def get_column_index_from_input(inp):
    return ord(inp.upper()) - ord('A')


def place_checker(board, col_idx, checker):
    """
    Place checker in the lowest available row in the given column.
    Returns the row index where placed, or None if the column is full.
    """
    for r in range(len(board) - 1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return r
    return None


def check_win(board, checker):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Directions: right, down, down-right, down-left
    directions = [
        (0, 1),
        (1, 0),
        (1, 1),
        (1, -1),
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker:
                    count += 1
                    if count == 4:
                        return True
                    rr += dr
                    cc += dc
    return False


def check_draw(board):
    # Draw if no empty spaces remain in top row (or anywhere)
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == " ":
                return False
    return True


def main():
    board = create_board(ROWS, COLS)

    # Randomly choose the starting player index
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        current_checker = CHECKERS[current_player_idx]
        prompt = f"Player {current_checker}, please enter a column: "
        # Get valid input (invalid characters cause re-prompt; full column loses the turn)
        while True:
            user_input = input(prompt).strip()
            if not is_valid_column_input(user_input, COLS):
                print("Invalid input. Please enter a valid column letter (e.g., A, B, ...).")
                continue
            col = get_column_index_from_input(user_input)
            placed_row = place_checker(board, col, current_checker)
            if placed_row is None:
                # Column is full: lose the turn
                clear_screen()
                print_board(board)
                print(f"Column {user_input.upper()} is full. Player {current_checker} loses the turn.")
                # Switch to next player
                current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
                break
            else:
                # Successful move
                clear_screen()
                print_board(board)
                # Check for win
                if check_win(board, current_checker):
                    print(f"Player {current_checker} won!")
                    return
                # Check for draw
                if check_draw(board):
                    print("The game is a draw.")
                    return
                # Next player's turn
                current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
                break


if __name__ == "__main__":
    main()
