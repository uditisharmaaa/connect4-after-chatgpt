import os
import random
import string

# ======================== CONSTANTS ===============================

ROWS = 6                     # number of rows
COLUMNS = 7                  # number of columns (max: 26)
NUM_PLAYERS = 2              # number of players (between 2 and 5)
CONNECT = 4                  # number in a row to win
CHECKERS = ["X", "O", "V", "H", "M"]  # allowed up to 5 players

assert NUM_PLAYERS >= 2 and NUM_PLAYERS <= 5, "Players between 2 and 5"
assert COLUMNS >= 1 and COLUMNS <= 26, "Columns between 1 and 26"

PLAYER_SYMBOLS = CHECKERS[:NUM_PLAYERS]

# ======================== BOARD FUNCTIONS =========================

def create_board():
    """Initialize the board with empty spaces."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the board with columns labeled A, B, C, ... G"""
    os.system('clear')  # Clear screen before printing
    header = "  " + "   ".join(string.ascii_uppercase[:COLUMNS])
    sep = "+" + ("---+" * COLUMNS)
    print(header)
    for row in board:
        print(sep)
        print("| " + " | ".join(row) + " |")
    print(sep)

# =================== INPUT & VALIDATION ==========================

def get_valid_column(board, current_player):
    """Prompt user until a valid column is entered. 
    Returns integer index of the column (0-based)."""
    while True:
        col = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if len(col) != 1 or col not in string.ascii_uppercase[:COLUMNS]:
            print(f"Invalid input. Enter a letter from A to {string.ascii_uppercase[COLUMNS-1]}.")
            continue
        col_idx = string.ascii_uppercase.index(col)
        # check if column is full
        if board[0][col_idx] != " ":
            print("Column is full! You lose your turn.")
            return None  # lose turn
        return col_idx

# =================== GAME LOGIC ==================================

def place_checker(board, col_idx, symbol):
    """
    Place the checker in the given column at the lowest available row.
    Returns the row index where the checker was placed.
    """
    for row in reversed(range(ROWS)):
        if board[row][col_idx] == " ":
            board[row][col_idx] = symbol
            return row
    return None  # should not happen, as we check for full column earlier

def check_direction(board, row, col, symbol, d_row, d_col):
    """Count consecutive checkers of symbol in (d_row, d_col) direction."""
    count = 0
    r, c = row, col
    while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == symbol:
        count += 1
        r += d_row
        c += d_col
    return count

def check_win(board, row, col, symbol):
    """
    Check all directions from (row, col) for a winning sequence.
    Return True if the player wins, else False.
    """
    directions = [  # pairs of opposite directions
        [(0, 1), (0, -1)],    # horizontal
        [(1, 0), (-1, 0)],    # vertical
        [(1, 1), (-1, -1)],   # diagonal down-right & up-left
        [(1, -1), (-1, 1)]    # diagonal down-left & up-right
    ]
    for dir_pair in directions:
        total = 1  # count the checker just placed
        for d_row, d_col in dir_pair:
            r, c = row + d_row, col + d_col
            total += check_direction(board, r, c, symbol, d_row, d_col)
        if total >= CONNECT:
            return True
    return False

def check_draw(board):
    """Return True if the board is full and no winner."""
    return all(cell != " " for cell in board[0])

# =================== MAIN GAME LOOP ==============================

def main():
    board = create_board()
    current = random.randint(0, NUM_PLAYERS-1)  # randomly select starting player
    print_board(board)
    print(f"Player {PLAYER_SYMBOLS[current]} starts!")
    while True:
        symbol = PLAYER_SYMBOLS[current]
        col_idx = get_valid_column(board, symbol)
        if col_idx is None:  # turn is lost due to full column
            # Move to next player
            current = (current + 1) % NUM_PLAYERS
            continue
        row_idx = place_checker(board, col_idx, symbol)
        print_board(board)
        # Check for win after every move
        if check_win(board, row_idx, col_idx, symbol):
            print(f"Player {symbol} won!")
            break
        if check_draw(board):
            print("It's a draw!")
            break
        # Switch to next player
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
