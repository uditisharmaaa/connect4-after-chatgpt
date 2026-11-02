import os
import random
import string

# ===========================#
#         CONSTANTS          #
# ===========================#
NUM_ROWS = 6
NUM_COLS = 7
MAX_COLS = 26
NUM_PLAYERS = 2      # Change this to 2..5 for more players
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

assert 2 <= NUM_PLAYERS <= 5, "Player count out of range"
assert NUM_COLS <= MAX_COLS, "Too many columns"

# ===========================#
#         FUNCTIONS          #
# ===========================#

def clear_screen():
    os.system('clear')

def create_board(rows=NUM_ROWS, cols=NUM_COLS):
    """Create a new game board initialized with whitespaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the current board to the terminal in the expected format."""
    rows = len(board)
    cols = len(board[0])
    col_labels = list(string.ascii_uppercase[:cols])
    
    # Print column headers
    print('  ' + '   '.join(col_labels))
    print('+' + '---+' * cols)
    
    # Print each board row
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)

def get_column_index(col_char, cols=NUM_COLS):
    """Given a column letter, return its 0-based index. Return -1 for invalid input."""
    col_labels = list(string.ascii_uppercase[:cols])
    return col_labels.index(col_char) if col_char in col_labels else -1

def is_column_full(board, col):
    """Check if a column is full."""
    return all(board[row][col] != ' ' for row in range(len(board)))

def place_checker(board, col, symbol):
    """
    Place the checker in the lowest empty cell in the given column.
    Returns the row index where the checker lands, or -1 if the column is full.
    """
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row
    return -1

def check_win(board, last_row, last_col, symbol):
    """Checks for a win condition after the most recent move."""
    directions = [
        (0, 1),    # Horizontal
        (1, 0),    # Vertical
        (1, 1),    # Down-right diagonal
        (1, -1)    # Down-left diagonal
    ]
    
    for dr, dc in directions:
        count = 1  # The last move itself
        # Check one direction
        r, c = last_row + dr, last_col + dc
        while in_bounds(board, r, c) and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        # Check the opposite direction
        r, c = last_row - dr, last_col - dc
        while in_bounds(board, r, c) and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def in_bounds(board, row, col):
    return 0 <= row < len(board) and 0 <= col < len(board[0])

def board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def get_valid_column_from_player(board, player_symbol):
    """Prompt the player for a valid column input."""
    cols = len(board[0])
    col_labels = list(string.ascii_uppercase[:cols])
    while True:
        col_input = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
        if len(col_input) != 1:
            print("Invalid input. Please enter a single letter corresponding to the columns.")
            continue
        if col_input not in col_labels:
            print(f"Invalid input. Please enter one of the columns: {', '.join(col_labels)}")
            continue
        col_index = get_column_index(col_input, cols)
        if is_column_full(board, col_index):
            print("That column is full. You lose your turn!")
            return None  # Invalid move, lose turn
        return col_index

def main():
    board = create_board(NUM_ROWS, NUM_COLS)
    player_symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    turns = 0

    # Initial board print
    clear_screen()
    print_board(board)

    while True:
        player_symbol = player_symbols[current_player_idx]
        col = get_valid_column_from_player(board, player_symbol)
        if col is None:  # Column was full, skip this player's turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            clear_screen()
            print_board(board)
            continue

        # Place the checker
        row = place_checker(board, col, player_symbol)
        turns += 1

        clear_screen()
        print_board(board)

        if check_win(board, row, col, player_symbol):
            print(f"Player {player_symbol} won!")
            break

        if board_full(board):
            print("It's a draw! The board is full.")
            break

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

# Only run the game if this script is being run directly
if __name__ == "__main__":
    main()
