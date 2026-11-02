import os
import random

# Constants for the board dimensions
ROWS = 6   # Number of rows
COLS = 7   # Number of columns (max 26)

# Number of players and their checker symbols
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

# Number of checkers in a row needed to win
WIN_COUNT = 4

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board(rows, cols):
    """Creates a board with given rows and columns initialized with spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the board with column headers labeled as letters."""
    cols = len(board[0])
    rows = len(board)
    # Print column headers A, B, C, ...
    headers = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(headers)
    # Print horizontal separator line
    sep = "+" + "---+" * cols
    for r in range(rows):
        print(sep)
        row_str = "|"
        for c in range(cols):
            row_str += " {} |".format(board[r][c])
        print(row_str)
    print(sep)

def is_valid_column(input_str, cols):
    """
    Check if the input is a single uppercase letter
    representing a valid column between A and ...
    """
    if len(input_str) != 1:
        return False
    if not input_str.isalpha() or not input_str.isupper():
        return False
    col_index = ord(input_str) - ord('A')
    if 0 <= col_index < cols:
        return True
    return False

def place_checker(board, col_index, checker):
    """
    Place the checker in the lowest available row in the given column.
    Returns True and the row index if placed successfully,
    Returns False and None if the column is full.
    """
    # Bottom row is last index ROWS-1
    for row in reversed(range(len(board))):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True, row
    return False, None

def check_direction(board, start_row, start_col, delta_row, delta_col, checker):
    """
    Checks number of continuous checkers in a direction starting from
    (start_row, start_col) moving by delta_row, delta_col.
    """
    count = 0
    row, col = start_row, start_col
    rows = len(board)
    cols = len(board[0])

    while 0 <= row < rows and 0 <= col < cols:
        if board[row][col] == checker:
            count += 1
            row += delta_row
            col += delta_col
        else:
            break
    return count

def check_win(board, row, col, checker):
    """
    Check all directions from the last placed checker for a win:
    - Horizontal
    - Vertical
    - Diagonal (2 directions)
    """
    directions = [
        ((0, -1), (0, 1)),     # Horizontal (left, right)
        ((-1, 0), (1, 0)),     # Vertical (up, down)
        ((-1, -1), (1, 1)),    # Diagonal (\) (up-left, down-right)
        ((-1, 1), (1, -1)),    # Diagonal (/) (up-right, down-left)
    ]

    for dir1, dir2 in directions:
        count = 1  # count the placed checker itself
        count += check_direction(board, row + dir1[0], col + dir1[1], dir1[0], dir1[1], checker)
        count += check_direction(board, row + dir2[0], col + dir2[1], dir2[0], dir2[1], checker)
        if count >= WIN_COUNT:
            return True
    return False

def check_draw(board):
    """Check if the board is full (no empty spaces in the top row)."""
    # If any space in the top row is empty, it's not a draw
    top_row = board[0]
    for cell in top_row:
        if cell == " ":
            return False
    return True

def next_player_index(current_index):
    """Get the next player's index, cycling back to zero."""
    return (current_index + 1) % NUM_PLAYERS

def main():
    # Create initial board
    board = create_board(ROWS, COLS)

    # List of active player checkers (slice first NUM_PLAYERS)
    players = CHECKERS[:NUM_PLAYERS]

    # Randomly select which player starts
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    while True:
        clear_screen()
        print_board(board)
        current_checker = players[current_player_idx]
        # Prompt input
        input_valid = False
        while not input_valid:
            column_input = input(f"Player {current_checker}, please enter a column: ")
            if not is_valid_column(column_input, COLS):
                print(f"Invalid input '{column_input}'. Please enter a valid column letter A-{chr(ord('A') + COLS - 1)}.")
                continue
            col_index = ord(column_input) - ord('A')
            # Check if the column is full
            placed, row_placed = place_checker(board, col_index, current_checker)
            if placed:
                input_valid = True
            else:
                # Column is full -> turn is lost
                print(f"Column {column_input} is full. {current_checker} loses the turn.")
                input_valid = True
                row_placed = None

        # Check for win only if checker was placed
        if row_placed is not None:
            if check_win(board, row_placed, col_index, current_checker):
                clear_screen()
                print_board(board)
                print(f"Player {current_checker} won!")
                break
        # Check for draw
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("Game is a draw!")
            break

        # Next player's turn
        current_player_idx = next_player_index(current_player_idx)

if __name__ == "__main__":
    main()
