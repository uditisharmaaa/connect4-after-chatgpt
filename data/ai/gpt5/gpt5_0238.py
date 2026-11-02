import os
import random
import string

# Constants (you may change these for your own testing; submission requires these values)
ROWS = 6
COLUMNS = 7   # Max 26
NUM_PLAYERS = 2  # Between 2 and 5

# Player symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]


def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]


def clear_screen():
    os.system('clear')


def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0])

    # Header with column letters
    letters = list(string.ascii_uppercase[:cols])
    header = "  " + "   ".join(letters)
    print(header)
    # Top border
    print("+" + "---+" * cols)

    # Rows
    for r in range(rows):
        row_line = "|"
        for c in range(cols):
            row_line += f" {board[r][c]} |"
        print(row_line)
        print("+" + "---+" * cols)


def get_column_index_from_input(user_input, max_cols):
    """
    Returns a valid column index (0-based) if input is a single letter within range.
    Otherwise returns None.
    """
    if not user_input:
        return None
    s = user_input.strip().upper()
    if len(s) != 1:
        return None
    if s < 'A' or s > 'Z':
        return None
    idx = ord(s) - ord('A')
    if 0 <= idx < max_cols:
        return idx
    return None


def is_column_full(board, col):
    return board[0][col] != " "


def is_board_full(board):
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True


def drop_checker(board, col, symbol):
    """
    Drops the checker into the specified column.
    Returns the row index where the checker was placed, or None if column is full.
    """
    rows = len(board)
    # Start from bottom
    for r in range(rows - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = symbol
            return r
    return None


def count_in_direction(board, start_r, start_c, dr, dc, symbol):
    """
    Counts consecutive symbols including the starting cell in both positive and negative directions.
    Returns total count of consecutive symbols in this line.
    """
    rows = len(board)
    cols = len(board[0])
    count = 1  # start cell

    # Positive direction
    r, c = start_r + dr, start_c + dc
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc

    # Negative direction
    r, c = start_r - dr, start_c - dc
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == symbol:
        count += 1
        r -= dr
        c -= dc

    return count


def check_win(board, r, c, symbol):
    """
    Checks whether placing 'symbol' at (r, c) creates a 4-in-a-row in any direction.
    """
    # Directions: horizontal, vertical, diagonal (/), diagonal (\)
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal \
        (1, -1)   # diagonal /
    ]
    for dr, dc in directions:
        if count_in_direction(board, r, c, dr, dc, symbol) >= 4:
            return True
    return False


def main():
    # Basic validations for constants
    cols = max(1, min(COLUMNS, 26))
    rows = max(1, ROWS)
    num_players = max(2, min(NUM_PLAYERS, 5))

    symbols = PLAYER_SYMBOLS[:num_players]

    board = create_board(rows, cols)

    # Randomly select starting player
    current_player_index = random.randrange(num_players)

    # Show initial empty board
    print_board(board)

    while True:
        current_symbol = symbols[current_player_index]

        # Prompt until a valid column letter is entered
        col_index = None
        while col_index is None:
            user_input = input(f"Player {current_symbol}, please enter a column: ")
            col_index = get_column_index_from_input(user_input, cols)
            if col_index is None:
                # Reprint board to keep UI consistent after invalid input
                print_board(board)
                print("Invalid input. Please enter a valid column letter (e.g., A, B, C).")

        # If the chosen column is full, player loses the turn
        if is_column_full(board, col_index):
            print_board(board)
            print(f"Column {string.ascii_uppercase[col_index]} is full. Turn lost.")
            # After losing a turn, check for draw (board might be full)
            if is_board_full(board):
                print("It's a draw!")
                break
            # Next player's turn
            current_player_index = (current_player_index + 1) % num_players
            continue

        # Place the checker
        placed_row = drop_checker(board, col_index, current_symbol)

        # Update and display board
        print_board(board)

        # Check for win
        if placed_row is not None and check_win(board, placed_row, col_index, current_symbol):
            print(f"Player {current_symbol} won!")
            break

        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player_index = (current_player_index + 1) % num_players


if __name__ == "__main__":
    main()
