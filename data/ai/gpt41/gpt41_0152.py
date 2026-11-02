import os
import random
import sys
import string

# --- Constants ---
ROWS = 6
COLS = 7
NUM_PLAYERS = 2  # Change to between 2 and 5 if needed
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# --- Board Initialization ---
def init_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

# --- Board Printing ---
def print_board(board, cols):
    os.system('clear')
    # Print column headers (A, B, ... up to COLS)
    header_letters = [chr(ord('A') + i) for i in range(cols)]
    print('  ' + '   '.join(header_letters))
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(f' {c} ' for c in row) + '|')
        print('+' + '---+' * cols)

# --- Input Validation ---
def is_valid_column(input_str, cols):
    return len(input_str) == 1 and input_str in string.ascii_uppercase[:cols]

# --- Find Row to Place Checker ---
def get_next_open_row(board, col):
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            return row
    return None

# --- Place Checker ---
def place_checker(board, row, col, checker):
    board[row][col] = checker

# --- Check for a Win ---
def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])
    # Horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True
    # Vertical
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True
    # Diagonal (down-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
    # Diagonal (up-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True
    return False

# --- Check for a Draw ---
def check_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True

# --- Main Game Loop ---
def connect4():
    # Sanity checks
    if COLS > 26 or COLS < 4 or ROWS < 4:
        print("Board dimensions must be at least 4x4 and at most 26 columns.")
        sys.exit(1)
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Number of players must be between 2 and 5.")
        sys.exit(1)
    board = init_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    # Randomize first player
    current_player = random.randint(0, NUM_PLAYERS - 1)

    print_board(board, COLS)
    print(f"Player {players[current_player]} starts!")

    game_over = False

    while not game_over:
        checker = players[current_player]
        valid_input = False
        col_index = -1

        # Input Loop
        while not valid_input:
            print_board(board, COLS)
            inp = input(f"Player {checker}, please enter a column: ").strip().upper()
            if not is_valid_column(inp, COLS):
                print("Invalid input. Please enter a valid column letter.")
                continue
            col_index = ord(inp) - ord('A')
            next_row = get_next_open_row(board, col_index)
            if next_row is None:
                print("Column is full. You lose your turn.")
                valid_input = True  # Still valid, but player loses turn
                col_index = None
            else:
                valid_input = True

        if col_index is not None:
            place_checker(board, next_row, col_index, checker)
            print_board(board, COLS)
            if check_win(board, checker):
                print(f"Player {checker} won!")
                game_over = True
                continue
            elif check_draw(board):
                print("The game is a draw!")
                game_over = True
                continue

        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    connect4()
