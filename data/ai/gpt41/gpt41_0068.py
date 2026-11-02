import os
import random
import sys

# --- CONSTANTS ---
ROWS = 6  # default 6 rows
COLS = 7  # default 7 columns (max 26)
MAX_COL_LETTERS = 26
PLAYERS = 2  # default 2 (should support up to 5: X, O, V, H, M)
CHECKERS = ["X", "O", "V", "H", "M"]

# --- FUNCTIONS ---

def clear_screen():
    """Clears the command line screen."""
    os.system('clear')

def create_board(rows, cols):
    """Creates a board with given dimensions, filled with whitespaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the board with column labels."""
    clear_screen()
    cols = len(board[0])
    # column labels
    col_labels = [chr(ord('A') + i) for i in range(cols)]
    print("  ", end="")
    for label in col_labels:
        print(f" {label}  ", end="")
    print()
    print("+---" * cols + "+")
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+---" * cols + "+")

def get_valid_players():
    """Determine which checker symbols to use based on PLAYERS."""
    if PLAYERS < 2 or PLAYERS > 5:
        print("Number of players must be between 2 and 5.")
        sys.exit(1)
    return CHECKERS[:PLAYERS]

def get_column_input(board):
    """Prompts the user for a column input and validates it."""
    cols = len(board[0])
    while True:
        col_input = input("Please enter a column: ").strip().upper()
        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input. Please enter a single letter corresponding to a column.")
            continue
        col_num = ord(col_input) - ord('A')
        if col_num < 0 or col_num >= cols:
            print("Invalid column letter. Try again.")
            continue
        if board[0][col_num] != " ":
            print("Column is full. You lose your turn.")
            return None  # Indicate full column, lose turn
        return col_num

def drop_checker(board, col, checker):
    """Drops the checker in the chosen column."""
    rows = len(board)
    # Start from the bottom and find first empty space
    for row in range(rows-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None  # Should not reach here if validated beforehand

def is_board_full(board):
    """Checks if the board is completely filled."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def check_for_win(board, last_row, last_col, checker):
    """Checks horizontally, vertically, and diagonally for 4 in a row."""
    return (check_direction(board, last_row, last_col, checker, 0, 1) or  # Horizontal
            check_direction(board, last_row, last_col, checker, 1, 0) or  # Vertical
            check_direction(board, last_row, last_col, checker, 1, 1) or  # Diagonal \
            check_direction(board, last_row, last_col, checker, 1, -1))   # Diagonal /

def check_direction(board, row, col, checker, d_row, d_col):
    """Check (row, col) in direction (d_row, d_col) for 4 in a row."""
    rows = len(board)
    cols = len(board[0])
    count = 1  # include the last placed checker

    # Check one direction
    r, c = row + d_row, col + d_col
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r += d_row
        c += d_col

    # Check opposite direction
    r, c = row - d_row, col - d_col
    while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
        count += 1
        r -= d_row
        c -= d_col

    return count >= 4

def choose_first_player():
    """Randomly selects who starts first and returns the player index."""
    return random.randint(0, PLAYERS - 1)

def main():
    board = create_board(ROWS, COLS)
    player_symbols = get_valid_players()
    first_player = choose_first_player()
    current_player = first_player
    print_board(board)
    print(f"Player {player_symbols[current_player]}'s turn to start!")

    while True:
        player_checker = player_symbols[current_player]
        print_board(board)
        print(f"Player {player_checker}, ", end="")
        col = get_column_input(board)
        if col is None:
            # Full column, lose turn.
            current_player = (current_player + 1) % PLAYERS
            continue
        row, col_placed = drop_checker(board, col, player_checker)
        if check_for_win(board, row, col_placed, player_checker):
            print_board(board)
            print(f"Player {player_checker} won!")
            break
        if is_board_full(board):
            print_board(board)
            print("It's a draw! No more legal moves.")
            break
        current_player = (current_player + 1) % PLAYERS  # Next player

if __name__ == "__main__":
    main()
