import os
import random
import string
import sys

# --- Constants (Change these if needed for testing, but submission must use these values) ---
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2  # Changeable from 2 to 5. For submission must be 2.
CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]
EMPTY_CELL = " "

# --- Helper functions ---

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def create_board(rows, cols):
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Column headers: A, B, ...
    header = "  " + "   ".join(string.ascii_uppercase[:cols])
    separator = "+" + "---+" * cols
    print(header)
    print(separator)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print(separator)

def get_valid_columns(board):
    cols = len(board[0])
    valid = []
    for col in range(cols):
        if board[0][col] == EMPTY_CELL:
            valid.append(string.ascii_uppercase[col])
    return valid

def get_column_index(column_letter, cols):
    if len(column_letter) != 1:
        return -1
    column_letter = column_letter.upper()
    if column_letter in string.ascii_uppercase[:cols]:
        return string.ascii_uppercase.index(column_letter)
    return -1

def drop_checker(board, col, checker):
    """
    Drop a checker into the column.
    Returns the row index where checker landed, or -1 if column is full.
    """
    rows = len(board)
    for row in reversed(range(rows)):
        if board[row][col] == EMPTY_CELL:
            board[row][col] = checker
            return row
    return -1

def is_board_full(board):
    return all(cell != EMPTY_CELL for cell in board[0])

def check_for_win(board, row, col, checker):
    return (
        check_direction(board, row, col, checker, 0, 1) +   # Horizontal
        check_direction(board, row, col, checker, 1, 0) +   # Vertical
        check_direction(board, row, col, checker, 1, 1) +   # Diagonal /
        check_direction(board, row, col, checker, 1, -1)    # Diagonal \
        > 0)

def check_direction(board, row, col, checker, delta_row, delta_col):
    """
    Check a direction for 4-in-a-row for the current checker.
    Returns 1 if found, else 0.
    """
    rows = len(board)
    cols = len(board[0])
    count = 1

    # Check in the positive direction
    r, c = row + delta_row, col + delta_col
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += delta_row
        c += delta_col

    # Check in the negative direction
    r, c = row - delta_row, col - delta_col
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r -= delta_row
        c -= delta_col

    return 1 if count >= 4 else 0

def prompt_for_column(valid_columns, current_player_checker):
    while True:
        col_input = input(f"Player {current_player_checker}, please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in string.ascii_uppercase[:COLUMNS]:
            print(f"Invalid input. Please enter one of {', '.join(string.ascii_uppercase[:COLUMNS])}.")
            continue
        if col_input not in valid_columns:
            print("This column is full. Please choose another column.")
            continue
        return col_input

def pick_starting_player(num_players):
    return random.randint(0, num_players - 1)

# --- Main game loop ---

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS
    current_player = pick_starting_player(NUM_PLAYERS)
    game_over = False

    while not game_over:
        clear_screen()
        print_board(board)
        valid_columns = get_valid_columns(board)

        # Draw check
        if len(valid_columns) == 0:
            print("The board is full. It's a draw!")
            break

        current_checker = players[current_player]
        col_letter = prompt_for_column(valid_columns, current_checker)
        col_index = get_column_index(col_letter, COLUMNS)
        dropped_row = drop_checker(board, col_index, current_checker)

        # Should never be -1 because of input validation, but just in case
        if dropped_row == -1:
            print("Unexpected error: tried to drop in a full column. Losing turn.")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        # Check for win
        if check_for_win(board, dropped_row, col_index, current_checker):
            clear_screen()
            print_board(board)
            print(f"Player {current_checker} won!")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
