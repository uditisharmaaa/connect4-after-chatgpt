import os
import random
import string

# ---------- CONSTANTS ----------
ROWS = 6                  # Default number of rows (height)
COLUMNS = 7               # Default number of columns (width)
MAX_COLUMNS = 26          # Do not allow more than 26 (A-Z)
NUM_PLAYERS = 2           # Set number of players (2-5)

CHECKERS = ['X', 'O', 'V', 'H', 'M']
PLAYER_CHECKERS = CHECKERS[:NUM_PLAYERS]
WIN_LENGTH = 4            # Number of checkers in a row needed to win

# ---------- FUNCTIONS ----------

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    """Return a new game board (list of lists)"""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the Connect 4 board to the terminal."""
    cols = len(board[0])
    # Print column headers (A, B, C, ...)
    print('  ' + '   '.join(string.ascii_uppercase[:cols]))
    print('+' + '---+' * cols)
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+' + '---+' * cols)

def get_valid_columns(board):
    """Return a list of column indices that are NOT full."""
    valid_cols = []
    for col in range(len(board[0])):
        if board[0][col] == ' ':
            valid_cols.append(col)
    return valid_cols

def get_column_index(col_input, cols):
    """Validate and return the index of the column from input character."""
    if len(col_input) != 1 or col_input not in string.ascii_uppercase[:cols]:
        return None
    return string.ascii_uppercase.index(col_input)

def place_checker(board, col, checker):
    """
    Place the checker in the chosen column.
    Returns True if placed, False if column is full
    """
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False    # Column is full

def is_board_full(board):
    """Check if the board is full."""
    for col in range(len(board[0])):
        if board[0][col] == ' ':
            return False
    return True

def check_win(board, checker):
    """Check for a win condition for the given checker."""
    rows, cols = len(board), len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            # Horizontal
            if c <= cols - WIN_LENGTH and all(board[r][c + i] == checker for i in range(WIN_LENGTH)):
                return True
            # Vertical
            if r <= rows - WIN_LENGTH and all(board[r + i][c] == checker for i in range(WIN_LENGTH)):
                return True
            # Diagonal down-right
            if r <= rows - WIN_LENGTH and c <= cols - WIN_LENGTH and all(board[r + i][c + i] == checker for i in range(WIN_LENGTH)):
                return True
            # Diagonal up-right
            if r >= WIN_LENGTH - 1 and c <= cols - WIN_LENGTH and all(board[r - i][c + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False

def player_turn(board, player_num, checker):
    """Handle a single player's turn."""
    cols = len(board[0])
    valid_cols = get_valid_columns(board)
    while True:
        col_input = input(f"Player {checker}, please enter a column: ").strip().upper()
        col_index = get_column_index(col_input, cols)
        if col_index is None:
            print("Invalid input! Please enter a valid column letter.")
            continue
        if col_index not in valid_cols:
            if board[0][col_index] != ' ':
                print("Column is full! You lose your turn.")
                return False   # Lose turn if column full
            else:
                print("Invalid column! Try again.")
            continue
        placed = place_checker(board, col_index, checker)
        if not placed:
            print("Column is full! You lose your turn.")
            return False      # Lose turn if column full (redundant, but for clarity)
        break
    return True

def main():
    # Initialize board and first player
    rows, cols = ROWS, COLUMNS
    if cols > MAX_COLUMNS:
        print(f"Column count cannot exceed {MAX_COLUMNS}")
        return
    board = create_board(rows, cols)
    first_player = random.randint(0, NUM_PLAYERS - 1)
    current_player = first_player

    # Show initial board
    clear_screen()
    print_board(board)
    print(f"Player {PLAYER_CHECKERS[current_player]} will start!")
    
    # Game loop
    winner = None
    while True:
        checker = PLAYER_CHECKERS[current_player]
        # Print board before asking for move
        clear_screen()
        print_board(board)

        succeeded = player_turn(board, current_player, checker)
        # If move wasn't taken due to full column, skip win/draw check and lose turn
        if not succeeded:
            # Next player's turn
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        # Check for victory
        if check_win(board, checker):
            clear_screen()
            print_board(board)
            print(f"Player {checker} won!")
            break
        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break
        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
