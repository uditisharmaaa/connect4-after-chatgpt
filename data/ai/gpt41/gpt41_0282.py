import os
import random
import string

# --- CONSTANTS ---
ROWS = 6            # Number of rows in the board
COLUMNS = 7         # Number of columns in the board (max 26 for letter labels)
NUM_PLAYERS = 2     # Number of players (from 2 to 5)

PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Max 5 players

# Get the symbols for active players
ACTIVE_SYMBOLS = PLAYER_SYMBOLS[:NUM_PLAYERS]

# --- FUNCTIONS ---

def initialize_board():
    """Creates and returns a game board initialized with spaces."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """
    Clear the screen and print the current state of the board with col labels.
    """
    os.system('clear')
    # Print column letters
    header = '  ' + '   '.join(string.ascii_uppercase[:COLUMNS])
    print(header)
    # Print separator
    print('+' + '---+' * COLUMNS)
    # Print board rows
    for row in board:
        print('|' + '|'.join(' {} '.format(cell) for cell in row) + '|')
        print('+' + '---+' * COLUMNS)

def get_valid_column(board):
    """
    Prompt user for a valid column input (A-G by default).
    Returns column index (int).
    """
    while True:
        col_input = input("Please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in string.ascii_uppercase[:COLUMNS]:
            print(f"Invalid input. Enter a letter from A to {string.ascii_uppercase[COLUMNS - 1]}.")
            continue
        col_idx = ord(col_input) - ord('A')
        # Check if the column is full
        if board[0][col_idx] != ' ':
            print("This column is full! Turn lost.")
            return None  # lose the turn
        return col_idx

def drop_checker(board, col, symbol):
    """
    Place the player's checker in the lowest available row of the column.
    Returns (row_index, col_index) tuple of where the checker landed.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return (row, col)
    return None  # Should never happen if checked before

def check_line_for_win(board, start_row, start_col, delta_row, delta_col, symbol):
    """
    Check if 4 consecutive checkers for symbol are lined up starting from (start_row, start_col)
    in direction (delta_row, delta_col).
    """
    for i in range(4):
        row = start_row + i * delta_row
        col = start_col + i * delta_col
        if row < 0 or row >= ROWS or col < 0 or col >= COLUMNS:
            return False
        if board[row][col] != symbol:
            return False
    return True

def check_for_win(board, symbol):
    """
    Check the entire board for a win for the given symbol.
    """
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] != symbol:
                continue
            # Check horizontal right
            if check_line_for_win(board, row, col, 0, 1, symbol):
                return True
            # Check vertical down
            if check_line_for_win(board, row, col, 1, 0, symbol):
                return True
            # Check diagonal down-right
            if check_line_for_win(board, row, col, 1, 1, symbol):
                return True
            # Check diagonal up-right
            if check_line_for_win(board, row, col, -1, 1, symbol):
                return True
    return False

def check_for_draw(board):
    """
    Return True if all cells are filled (draw), else False.
    """
    return all(cell != ' ' for row in board for cell in row)

def main():
    # Initialize game
    board = initialize_board()
    # Randomly select first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)
    print(f"Player {ACTIVE_SYMBOLS[current_player]} starts!")

    while True:
        symbol = ACTIVE_SYMBOLS[current_player]
        print(f"Player {symbol}, ", end='')
        col_idx = get_valid_column(board)
        if col_idx is None:
            # Turn lost due to full column
            current_player = (current_player + 1) % NUM_PLAYERS
            print_board(board)
            continue

        # Place checker
        row_idx, _ = drop_checker(board, col_idx, symbol)
        print_board(board)
        # Check for win
        if check_for_win(board, symbol):
            print(f"Player {symbol} won!")
            break
        # Check for draw
        if check_for_draw(board):
            print("It's a draw!")
            break
        # Next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
