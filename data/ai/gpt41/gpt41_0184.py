import os
import random
import string
import sys

# ========== CONSTANTS ==========
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
PLAYERS = 2  # can be up to 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# ========== BOARD FUNCTIONS ==========

def create_board(rows, columns):
    """Create and return a board with the given number of rows and columns, initialized to spaces."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board, columns):
    """Clear the screen and display the board."""
    os.system('clear')
    # Print column headers (A, B, ...)
    col_headers = "  "
    for c in range(columns):
        col_headers += f"{string.ascii_uppercase[c]}   "
    print(col_headers.rstrip())
    print('+' + '---+' * columns)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * columns)

def column_index_from_letter(letter):
    """Return numerical index of a column, given its letter (A, B, ...)."""
    return string.ascii_uppercase.find(letter.upper())

def is_column_valid(col_input, columns):
    """Checks if the input column is valid (single letter, in range, not empty)."""
    if len(col_input) != 1:
        return False
    if col_input not in string.ascii_uppercase[:columns]:
        return False
    return True

def is_column_full(board, col_index):
    """Checks if a column is full."""
    return all(board[row][col_index] != ' ' for row in range(ROWS))

def place_checker(board, col_index, checker):
    """Place a checker into the correct row in the given column. Returns the row index where placed or None."""
    for row in reversed(range(ROWS)):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return row
    return None  # If column is full

def board_full(board):
    """Determine if the board is completely full."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

# ========== WIN CHECKING ==========

def check_direction(board, row, col, delta_row, delta_col, checker):
    """Check in one direction (delta_row, delta_col) for 4 consecutive checkers."""
    count = 0
    r, c = row, col
    for _ in range(4):
        if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
        else:
            break
        r += delta_row
        c += delta_col
    return count == 4

def check_win(board, last_row, last_col, checker):
    """Given last move, check for a win (4 in a row)."""
    directions = [ (0,1), (1,0), (1,1), (1,-1) ]  # horizontal, vertical, two diagonals
    for dr, dc in directions:
        count = 1
        # Look forwards
        r, c = last_row + dr, last_col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Look backwards
        r, c = last_row - dr, last_col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

# ========== GAME LOOP ==========

def main():
    # 1. Initialize board
    if COLUMNS > MAX_COLUMNS:
        print(f"Error: Max columns supported is {MAX_COLUMNS}")
        sys.exit(1)
    if PLAYERS < 2 or PLAYERS > 5:
        print("Error: The number of players must be between 2 and 5.")
        sys.exit(1)

    board = create_board(ROWS, COLUMNS)
    checkers = CHECKERS[:PLAYERS]
    player_names = [f'Player {ch}' for ch in checkers]
    # Randomly select starting player
    current_player = random.randint(0, PLAYERS - 1)

    print_board(board, COLUMNS)
    print(f"{player_names[current_player]} ({checkers[current_player]}) starts!\nPress enter to begin.")
    input()

    # 2. Game loop
    while True:
        print_board(board, COLUMNS)
        checker = checkers[current_player]
        name = player_names[current_player]
        turn_taken = False
        while not turn_taken:
            col_input = input(f"{name} ({checker}), please enter a column: ").strip().upper()
            if not is_column_valid(col_input, COLUMNS):
                print("Invalid column. Please enter a valid letter corresponding to a column.")
                continue
            col_idx = column_index_from_letter(col_input)
            if is_column_full(board, col_idx):
                print("Column is full. You lose your turn!")
                break  # Skip turn as per assignment
            row_idx = place_checker(board, col_idx, checker)
            turn_taken = True
            # Check for win
            if check_win(board, row_idx, col_idx, checker):
                print_board(board, COLUMNS)
                print(f"{name} won!")
                return
            # Check for draw
            if board_full(board):
                print_board(board, COLUMNS)
                print("The game is a draw!")
                return
        current_player = (current_player + 1) % PLAYERS

if __name__ == '__main__':
    main()
