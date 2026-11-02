import os
import random
import string

# Constants (you may change these for testing; submission requires ROWS=6, COLS=7, NUM_PLAYERS=2)
ROWS = 6
COLS = 7  # Max 26
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]

# Validate constants
if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
    raise ValueError("NUM_PLAYERS must be between 2 and 5.")
if COLS < 1 or COLS > 26:
    raise ValueError("COLS must be between 1 and 26.")
if ROWS < 1:
    raise ValueError("ROWS must be at least 1.")

ACTIVE_CHECKERS = CHECKERS[:NUM_PLAYERS]
COLUMN_LABELS = list(string.ascii_uppercase[:COLS])  # ['A', 'B', ..., up to COLS]


def clear_screen():
    # Clear the terminal screen (Linux/Unix)
    os.system('clear')


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    # Column labels
    header = "  " + "   ".join(COLUMN_LABELS)
    print(header)
    # Top border before any row content
    border = "+" + "+".join(["---"] * COLS) + "+"
    for r in range(ROWS):
        print(border)
        row_cells = []
        for c in range(COLS):
            row_cells.append(board[r][c])
        print("| " + " | ".join(row_cells) + " |")
    # Bottom border
    print(border)


def is_valid_column_input(s):
    if len(s) != 1:
        return False
    if s not in COLUMN_LABELS:
        return False
    return True


def get_lowest_empty_row(board, col):
    # Returns the row index of the lowest empty cell in the given column, or None if full
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None


def drop_checker(board, col, checker):
    # Attempt to drop a checker into column col. Returns (row, col) if placed, or None if column is full.
    row = get_lowest_empty_row(board, col)
    if row is None:
        return None
    board[row][col] = checker
    return (row, col)


def check_win(board, checker):
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == checker and board[r][c + 1] == checker and
                board[r][c + 2] == checker and board[r][c + 3] == checker):
                return True

    # Check vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if (board[r][c] == checker and board[r + 1][c] == checker and
                board[r + 2][c] == checker and board[r + 3][c] == checker):
                return True

    # Check diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if (board[r][c] == checker and board[r + 1][c + 1] == checker and
                board[r + 2][c + 2] == checker and board[r + 3][c + 3] == checker):
                return True

    # Check diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if (board[r][c] == checker and board[r - 1][c + 1] == checker and
                board[r - 2][c + 2] == checker and board[r - 3][c + 3] == checker):
                return True

    return False


def check_draw(board):
    # Draw if no empty spaces left
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True


def main():
    board = create_board(ROWS, COLS)
    current_player_index = random.randrange(NUM_PLAYERS)

    # Initial display
    clear_screen()
    print_board(board)

    while True:
        current_checker = ACTIVE_CHECKERS[current_player_index]
        # Prompt user input until valid column letter
        while True:
            try:
                user_input = input(f"Player {current_checker}, please enter a column: ").strip().upper()
            except EOFError:
                # If input stream ends, just exit gracefully
                return
            if is_valid_column_input(user_input):
                break
            else:
                # Invalid input, ask again without losing the turn
                clear_screen()
                print_board(board)
                print("Invalid input. Please enter a valid column letter.")

        col = COLUMN_LABELS.index(user_input)

        # Try to drop checker
        move = drop_checker(board, col, current_checker)

        if move is None:
            # Column full: lose the turn
            clear_screen()
            print_board(board)
            print(f"Column {user_input} is full. Player {current_checker} loses the turn.")
            # Check for draw even if move not made (in case the board is full)
            if check_draw(board):
                print("The game is a draw!")
                break
            # Switch player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        # Move was made
        clear_screen()
        print_board(board)

        # Check win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
