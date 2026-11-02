import os
import random
import string
import sys

# =================== CONSTANTS ===================
NUM_ROWS = 6                # Default: 6 rows
NUM_COLS = 7                # Default: 7 columns
NUM_PLAYERS = 2             # Default: 2 players (max 5, min 2)
WINNING_LENGTH = 4          # Number of checkers needed to win

MAX_COLS = 26               # Maximum number of columns (A-Z)
PLAYER_CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Adjust checkers array based on number of players
CHECKERS = PLAYER_CHECKERS[:NUM_PLAYERS]

# =================== FUNCTIONS ===================

def clear_screen():
    """Clears the terminal screen (works for Linux/macOS)."""
    os.system('clear')

def create_board(rows, cols):
    """Creates and returns a 2D list (rows x cols) initialized with spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the Connect 4 board with column labels."""
    cols = len(board[0])
    # Column labels (A, B, C, ...)
    col_labels = [string.ascii_uppercase[i] for i in range(cols)]
    print('  ' + '   '.join(col_labels))
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)

def select_random_player(player_count):
    """Returns a random player index (0-based)."""
    return random.randint(0, player_count - 1)

def get_valid_column(board, player_checker):
    """Prompts the user for a valid column letter and returns the selected column index."""
    cols = len(board[0])
    col_labels = [string.ascii_uppercase[i] for i in range(cols)]
    while True:
        try:
            user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
            # Check input is a single uppercase letter in the allowed range
            if len(user_input) != 1 or user_input not in col_labels:
                print(f"Invalid input. Please enter a letter from A to {col_labels[-1]}.")
                continue
            col = col_labels.index(user_input)
            # Check if column is not full
            if board[0][col] != ' ':
                print("Column is full. You lose your turn!")
                return None  # Lose the turn if column is full
            return col
        except (ValueError, IndexError):
            print(f"Invalid input. Please enter a single letter from A to {col_labels[-1]}.")

def place_checker(board, col, checker):
    """Places a checker at the lowest available row in the specified column."""
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return

def check_win(board, checker):
    """Checks if the given checker has 4 in a row anywhere on the board."""
    rows = len(board)
    cols = len(board[0])
    length = WINNING_LENGTH

    # Check horizontal
    for r in range(rows):
        for c in range(cols - length + 1):
            if all(board[r][c+i] == checker for i in range(length)):
                return True

    # Check vertical
    for c in range(cols):
        for r in range(rows - length + 1):
            if all(board[r+i][c] == checker for i in range(length)):
                return True

    # Check diagonal (down-right)
    for r in range(rows - length + 1):
        for c in range(cols - length + 1):
            if all(board[r+i][c+i] == checker for i in range(length)):
                return True

    # Check diagonal (up-right)
    for r in range(length - 1, rows):
        for c in range(cols - length + 1):
            if all(board[r-i][c+i] == checker for i in range(length)):
                return True

    return False

def check_draw(board):
    """Checks if the board is full (draw)."""
    return all(cell != ' ' for cell in board[0])  # Top row full means board full

def main():
    # Sanity checks for number of players and columns
    if NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Number of players must be between 2 and 5.")
        sys.exit(1)
    if NUM_COLS > MAX_COLS:
        print(f"Maximum number of columns is {MAX_COLS}.")
        sys.exit(1)

    # Game initialization
    board = create_board(NUM_ROWS, NUM_COLS)
    current_player = select_random_player(NUM_PLAYERS)
    game_over = False

    clear_screen()
    print_board(board)

    while not game_over:
        checker = CHECKERS[current_player]

        # Get player input
        col = get_valid_column(board, checker)
        if col is None:
            # If column is full and player loses turn:
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        # Place checker
        place_checker(board, col, checker)

        # Print updated board
        clear_screen()
        print_board(board)

        # Win check
        if check_win(board, checker):
            print(f"Player {checker} won!")
            game_over = True
            continue

        # Draw check
        if check_draw(board):
            print("The game is a draw!")
            game_over = True
            continue

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
