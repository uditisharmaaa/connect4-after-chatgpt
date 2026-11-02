import os
import random
import string

# ==== CONSTANTS ====
ROWS = 6                # Number of rows on the board (default 6)
COLUMNS = 7             # Number of columns on the board (default 7, max 26)
PLAYERS = 2             # Number of players (default 2, up to 5)
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Player symbols
EMPTY_CELL = " "        # Representation of an empty board cell

# ==== FUNCTIONS ====

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board(rows, cols):
    """Creates a new game board."""
    return [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the Connect 4 board."""
    col_labels = "  " + "   ".join(string.ascii_uppercase[:COLUMNS])
    print(col_labels)
    print("+" + "---+" * COLUMNS)
    for row in board:
        row_str = "|" + "|".join(f" {cell} " for cell in row) + "|"
        print(row_str)
        print("+" + "---+" * COLUMNS)

def choose_first_player():
    """Randomly selects the first player's index."""
    return random.randint(0, PLAYERS - 1)

def is_valid_column(input_str):
    """Checks if input_str is a valid column label (single capital character between A and ...)."""
    if len(input_str) != 1:
        return False
    letter = input_str.upper()
    if letter < 'A' or letter >= chr(ord('A') + COLUMNS):
        return False
    return True

def is_column_full(board, col):
    """Returns True if specified column (index) is full, else False."""
    return board[0][col] != EMPTY_CELL

def get_next_open_row(board, col):
    """Returns the row index of the next available (bottommost) position in column col, or None if full."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY_CELL:
            return row
    return None

def drop_checker(board, col, player_symbol):
    """Places the player's checker in the requested column. Assumes the column is not full."""
    row = get_next_open_row(board, col)
    if row is not None:
        board[row][col] = player_symbol
        return row
    return None

def win_check(board, row, col, symbol):
    """Checks if placing a checker at (row, col) with 'symbol' creates a win."""
    # Directions: (delta_row, delta_col)
    directions = [
        (0, 1),    # horizontal right
        (1, 0),    # vertical down
        (1, 1),    # diagonal down-right
        (1, -1),   # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # one direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        # opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_board_full(board):
    """Returns True if the board is full, False otherwise."""
    for c in range(COLUMNS):
        if not is_column_full(board, c):
            return False
    return True

def get_player_input(board, player_symbol):
    """Reads user input for the column to play, validates it, and returns the column index. If column is full, turn is lost."""
    while True:
        col_input = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
        if not is_valid_column(col_input):
            print("Invalid input! Please enter a valid column letter.")
            continue
        col = ord(col_input) - ord('A')
        if is_column_full(board, col):
            print("That column is full. You lose your turn!")
            return None                        # Lose the turn
        return col

# ==== MAIN GAME ====

def main():
    # Setup
    board = create_board(ROWS, COLUMNS)
    player_symbols = PLAYER_SYMBOLS[:PLAYERS]
    current_player_idx = choose_first_player()

    clear_screen()
    print_board(board)
    print(f"Player {player_symbols[current_player_idx]} starts!\n")

    while True:
        player_symbol = player_symbols[current_player_idx]
        col = get_player_input(board, player_symbol)
        if col is not None:
            row = drop_checker(board, col, player_symbol)
            clear_screen()
            print_board(board)
            if win_check(board, row, col, player_symbol):
                print(f"Player {player_symbol} won!")
                break
            if is_board_full(board):
                print("It's a draw!")
                break
        else:
            clear_screen()
            print_board(board)
            print("Turn lost due to full column.")

        # Alternate to the next player
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
