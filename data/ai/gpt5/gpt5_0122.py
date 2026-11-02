import os
import random
import string

# Constants (adjustable for testing, but submission requires 6 rows x 7 cols and 2 players)
ROWS = 6
COLS = 7  # max 26 (A-Z)
NUM_PLAYERS = 2  # valid range: 2..5

# Allowed checker symbols in order (use first NUM_PLAYERS)
CHECKERS = ["X", "O", "V", "H", "M"]


def clear_screen():
    # Clear terminal (Linux/Unix per assignment)
    os.system('clear')


def create_board(rows, cols):
    # Create a rows x cols board filled with spaces
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    rows = len(board)
    cols = len(board[0])

    # Header with column letters A.. up to cols
    letters = string.ascii_uppercase[:cols]
    header = "  " + "   ".join(letters)
    sep = "+" + "+".join(["---"] * cols) + "+"

    print(header)
    print(sep)
    for r in range(rows):
        row_str = "|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|"
        print(row_str)
        print(sep)


def column_from_input(col_input, cols):
    # Convert single letter (A..Z) to column index, return None if invalid
    if not col_input or len(col_input) != 1:
        return None
    ch = col_input.upper()
    letters = string.ascii_uppercase[:cols]
    if ch in letters:
        return letters.index(ch)
    return None


def get_valid_column_input(cols, current_checker):
    # Ask until a syntactically valid column letter (within board) is provided
    # Does not check if the column is full (that's handled by drop attempt)
    while True:
        user_in = input(f"Player {current_checker}, please enter a column: ").strip()
        col_idx = column_from_input(user_in, cols)
        if col_idx is not None:
            return col_idx
        print("Invalid input. Please enter a valid column letter (e.g., A, B, C).")


def find_drop_row(board, col):
    # Return the row index where a checker would land in the given column,
    # or None if the column is full.
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def place_checker(board, col, checker):
    # Attempt to place checker; return True if placed, False if column full
    row = find_drop_row(board, col)
    if row is None:
        return False
    board[row][col] = checker
    return True


def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])
    target = checker

    # Directions: (dr, dc): right, down, diag down-right, diag up-right
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != target:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == target:
                    count += 1
                    if count == 4:
                        return True
                    rr += dr
                    cc += dc
    return False


def is_draw(board):
    # Draw if no empty cells remain
    for row in board:
        if " " in row:
            return False
    return True


def next_player_index(current_idx, total_players):
    return (current_idx + 1) % total_players


def main():
    # Validate constants
    cols = max(1, min(COLS, 26))  # enforce max 26 columns
    rows = max(1, ROWS)
    num_players = max(2, min(NUM_PLAYERS, 5))
    symbols = CHECKERS[:num_players]

    # Initialize game
    board = create_board(rows, cols)
    current = random.randrange(num_players)

    # Initial display
    clear_screen()
    print_board(board)

    while True:
        current_checker = symbols[current]

        # Display prompt after printing the board (as in example)
        col = get_valid_column_input(cols, current_checker)

        # Try to place checker
        if not place_checker(board, col, current_checker):
            # Column full: invalid turn; player loses turn
            clear_screen()
            print_board(board)
            print(f"Column {string.ascii_uppercase[col]} is full. Player {current_checker} loses the turn.")
            # Next player's turn
            current = next_player_index(current, num_players)
            continue

        # After a valid placement, update screen and check for win/draw
        clear_screen()
        print_board(board)

        if check_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        if is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current = next_player_index(current, num_players)


if __name__ == "__main__":
    main()
