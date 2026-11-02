import os
import random
import string
import sys

# ===================== CONSTANTS =====================
ROWS = 6
COLS = 7                 # <= 26
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2          # For assignment, set to 2

EMPTY = " "

# ===================== BOARD FUNCTIONS =====================
def create_board(rows=ROWS, cols=COLS):
    """Create a ROWS x COLS board initialized with EMPTY."""
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Clear screen and print the Connect 4 board with column letters."""
    os.system('clear' if os.name != 'nt' else 'cls')
    col_labels = "  " + "   ".join(string.ascii_uppercase[:len(board[0])])
    print(col_labels)
    print('+' + '---+' * len(board[0]))
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * len(board[0]))

# ===================== GAME LOGIC =====================
def get_valid_columns(board):
    """Return a set of column labels (letters) that are valid (not full)."""
    valid = set()
    for ci in range(len(board[0])):
        if board[0][ci] == EMPTY:
            valid.add(string.ascii_uppercase[ci])
    return valid

def column_full(board, col_idx):
    """Return True if the given column is full."""
    return board[0][col_idx] != EMPTY

def place_checker(board, col_idx, symbol):
    """
    Place checker in given column.
    Returns False if column is full, else row_index where placed.
    """
    for row in reversed(range(len(board))):
        if board[row][col_idx] == EMPTY:
            board[row][col_idx] = symbol
            return row
    return False

def check_win(board, row, col, symbol):
    """Return True if player with `symbol` has 4 in a row, starting from last placed (row, col)."""
    return (check_direction(board, row, col, symbol, 0, 1)   # Horizontal
            or check_direction(board, row, col, symbol, 1, 0)  # Vertical
            or check_direction(board, row, col, symbol, 1, 1)  # Diagonal /
            or check_direction(board, row, col, symbol, 1, -1)) # Diagonal \

def check_direction(board, row, col, symbol, dr, dc):
    """Check one direction (and its opposite), count consecutive same symbols."""
    count = 1
    # Forward direction
    r, c = row+dr, col+dc
    while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == symbol:
        count += 1
        r += dr
        c += dc
    # Backward direction
    r, c = row-dr, col-dc
    while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == symbol:
        count += 1
        r -= dr
        c -= dc
    return count >= 4

def is_draw(board):
    """Return True if the board is full."""
    return all(cell != EMPTY for cell in board[0])

def validate_input(user_input, valid_cols):
    """Return column index if valid, else None."""
    if len(user_input) != 1 or user_input not in string.ascii_uppercase:
        return None
    if user_input not in valid_cols:
        return None
    return string.ascii_uppercase.index(user_input)

# ===================== MAIN GAME LOOP =====================
def main():
    board = create_board()
    num_players = NUM_PLAYERS
    player_symbols = PLAYER_SYMBOLS[:num_players]

    # Randomly select first player
    current = random.randint(0, num_players - 1)

    print_board(board)
    print(f"Player {player_symbols[current]} starts!\nPress ENTER to begin.")
    input()

    while True:
        print_board(board)
        current_symbol = player_symbols[current]
        valid_cols = get_valid_columns(board)
        if not valid_cols:
            print("The game is a draw!")
            break

        print(f"Player {current_symbol}, please enter a column: ", end='')
        user_input = input().strip().upper()

        col_idx = validate_input(user_input, valid_cols)
        if col_idx is None:
            print("Invalid column. Please enter a valid column letter corresponding to a non-full column.")
            input("Press ENTER to try again...")
            continue

        row_idx = place_checker(board, col_idx, current_symbol)
        if row_idx is False:
            print("Column is full. You lose your turn.")
            current = (current + 1) % num_players  # Skip turn
            input("Press ENTER to continue...")
            continue

        if check_win(board, row_idx, col_idx, current_symbol):
            print_board(board)
            print(f"Player {current_symbol} won!")
            break
        elif is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        else:
            # Next player's turn
            current = (current + 1) % num_players

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        os.system('clear' if os.name != 'nt' else 'cls')
        sys.exit(0)
