import os
import random
import string

# Constants
NUM_ROWS = 6
NUM_COLS = 7                 # can be any value <= 26 (A-Z columns)
NUM_PLAYERS = 2              # can be any value 2 - 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']       # Max 5 players' checkers

# Calculate column labels (A, B, C, ...)
COL_LABELS = list(string.ascii_uppercase[:NUM_COLS])

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Creates and returns a board initialized with spaces."""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Prints the board to the terminal, including column headers."""
    # Print column headers
    print("  ", end='')
    for col in COL_LABELS:
        print(f" {col}  ", end='')
    print()
    # Print separator
    print("+" + "---+" * NUM_COLS)
    # Print each row
    for row in board:
        print("|", end='')
        for cell in row:
            print(f" {cell} |", end='')
        print()
        print("+" + "---+" * NUM_COLS)

def get_next_open_row(board, col):
    """
    Returns the lowest open row in a given column.
    If the column is full, returns None.
    """
    for row in reversed(range(NUM_ROWS)):
        if board[row][col] == ' ':
            return row
    return None

def is_board_full(board):
    """Returns True if the board is full, False otherwise."""
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def valid_column_input(input_str):
    """Checks if the input is a valid column letter for the board."""
    if len(input_str) != 1:
        return False
    if input_str not in COL_LABELS:
        return False
    return True

def check_winner(board, checker):
    """
    Checks if the player with 'checker' has won the game.
    Win if 4 in a row - horizontally, vertically, or diagonally.
    """
    # Horizontal check
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row][col + k] == checker for k in range(4)):
                return True

    # Vertical check
    for col in range(NUM_COLS):
        for row in range(NUM_ROWS - 3):
            if all(board[row + k][col] == checker for k in range(4)):
                return True

    # Diagonal "/"
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLS - 3):
            if all(board[row - k][col + k] == checker for k in range(4)):
                return True

    # Diagonal "\"
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLS - 3):
            if all(board[row + k][col + k] == checker for k in range(4)):
                return True

    return False

def main():
    # Game Setup
    board = create_board()
    active_checkers = CHECKERS[:NUM_PLAYERS]
    players = list(range(NUM_PLAYERS))
    # Randomly select who starts
    current_player_idx = random.choice(players)

    clear_screen()
    print_board(board)
    
    winner = None

    while True:
        checker = active_checkers[current_player_idx]
        print(f"Player {checker}, please enter a column:")

        while True:
            move = input().strip().upper()

            if not valid_column_input(move):
                print(f"Invalid input. Please enter a column (A-{COL_LABELS[-1]}):")
                continue

            col_idx = COL_LABELS.index(move)
            row_idx = get_next_open_row(board, col_idx)
            if row_idx is None:
                print("This column is full. You lose your turn.")
                row_idx = None
                break # Lose turn
            else:
                board[row_idx][col_idx] = checker
                break

        clear_screen()
        print_board(board)

        # Only check for win if player got to move this round
        if row_idx is not None:
            if check_winner(board, checker):
                print(f"Player {checker} won!")
                winner = checker
                break

        if is_board_full(board):
            print("The game is a draw!")
            break

        # Next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
