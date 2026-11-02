import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_COLS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYERS_COUNT = 2  # Set number of players here (2 to 5)
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4

assert 2 <= PLAYERS_COUNT <= 5, "Number of players must be between 2 and 5"
assert COLS <= MAX_COLS, f"Number of columns must be less or equal to {MAX_COLS}"
assert ROWS > 0 and COLS > 0, "Board dimensions must be positive integers"

# We will represent the board as a list of rows, each row is a list of strings.
# Each element initially is " " (space)

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    rows = len(board)
    # Print column headers A B C ...
    header_letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(header_letters))
    
    # Print each row with separators
    for r in range(rows):
        print("+" + "---+" * cols)
        row_str = "|"
        for c in range(cols):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print("+" + "---+" * cols)

def get_column_index(input_str, cols):
    # Validate and convert the player's input letter to column index
    if len(input_str) != 1:
        return None
    ch = input_str.upper()
    if 'A' <= ch < chr(ord('A') + cols):
        return ord(ch) - ord('A')
    return None

def is_column_full(board, col):
    # If top cell in the column is occupied, column is full
    return board[0][col] != " "

def place_checker(board, col, checker):
    # Places checker in the lowest available row in the column.
    # Returns True if successful, False if the column is full.
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None  # Column full

def check_direction(board, start_row, start_col, d_row, d_col, checker):
    # Count consecutive checkers of the same type starting at (start_row, start_col)
    # moving in direction (d_row, d_col)
    count = 0
    row, col = start_row, start_col
    rows = len(board)
    cols = len(board[0])
    while 0 <= row < rows and 0 <= col < cols and board[row][col] == checker:
        count += 1
        row += d_row
        col += d_col
    return count

def check_win(board, row, col, checker):
    # Check horizontal, vertical and both diagonals for a win of length WIN_LENGTH
    # We count in both directions and subtract 1 (the starting point counted twice)
    directions = [
        (0, 1),  # Horizontal right
        (1, 0),  # Vertical down
        (1, 1),  # Diagonal down-right
        (1, -1), # Diagonal down-left
    ]
    for d_row, d_col in directions:
        count = (
            check_direction(board, row, col, d_row, d_col, checker) +
            check_direction(board, row, col, -d_row, -d_col, checker) - 1
        )
        if count >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    # Board is full if no spaces on top row
    return all(cell != " " for cell in board[0])

def get_valid_input(current_player, board):
    cols = len(board[0])
    while True:
        inp = input(f"Player {current_player}, please enter a column: ").strip()
        col_index = get_column_index(inp, cols)
        if col_index is None:
            continue
        if is_column_full(board, col_index):
            # Turn lost if column full
            return col_index, True
        return col_index, False

def main():
    random.seed()
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS_COUNT]
    current_player_idx = random.randint(0, PLAYERS_COUNT - 1)

    print_board(board)

    while True:
        current_checker = players[current_player_idx]

        col, lost_turn = get_valid_input(current_checker, board)
        if lost_turn:
            # Column full: turn lost
            current_player_idx = (current_player_idx + 1) % PLAYERS_COUNT
            print_board(board)
            continue

        position = place_checker(board, col, current_checker)
        print_board(board)

        if position is None:
            # Should not happen due to validation, but safe check
            current_player_idx = (current_player_idx + 1) % PLAYERS_COUNT
            continue

        row_placed, col_placed = position

        # Check for win
        if check_win(board, row_placed, col_placed, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if board_full(board):
            print("The game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % PLAYERS_COUNT

if __name__ == "__main__":
    main()
