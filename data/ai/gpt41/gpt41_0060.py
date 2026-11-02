import os
import random
import string
import sys

# ====== CONSTANTS ======
NUM_ROWS = 6
NUM_COLS = 7
MAX_COLS = 26   # For possible different dimensions, max 26 columns (A-Z)
NUM_PLAYERS = 2 # 2 players enabled for submission (set 2-5 as needed)
CHECKERS = ["X", "O", "V", "H", "M"]  # Order matters, indexed by player number
WIN_COUNT = 4  # Number of checkers in a row to win

# ====== FUNCTIONS ======

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    """Create a board with the specified dimensions initialized with spaces."""
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Print the board in user-friendly format."""
    rows = len(board)
    cols = len(board[0])

    # Column header: A B C ...
    col_labels = [string.ascii_uppercase[i] for i in range(cols)]
    print('  ' + '   '.join(col_labels))
    print('+' + ('---+'*cols))

    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + ('---+'*cols))

def get_valid_columns(board):
    """Return list of indices of columns that are not full."""
    cols = len(board[0])
    valid = []
    for c in range(cols):
        if board[0][c] == ' ':  # Topmost row is empty
            valid.append(c)
    return valid

def input_column(board, player_checker):
    """Prompt the current player for a valid column input."""
    cols = len(board[0])
    col_labels = [string.ascii_uppercase[i] for i in range(cols)]
    valid_cols = get_valid_columns(board)
    valid_labels = [col_labels[c] for c in valid_cols]

    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(user_input) != 1:
            print("Invalid input. Enter a single column letter.")
            continue
        if user_input not in col_labels:
            print("Invalid column label. Please use: " + ", ".join(col_labels))
            continue
        col_index = col_labels.index(user_input)
        if col_index not in valid_cols:
            print("Column is full. Turn will be lost.")
            return None  # Turn lost
        return col_index

def place_checker(board, col, checker):
    """
    Place the checker in the given column.
    Return the row where checker is placed, or None if the column is full.
    """
    rows = len(board)
    for row in reversed(range(rows)):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return None  # Should not happen as we check if column is valid before

def board_full(board):
    """Return True if the board is full, else False."""
    for cell in board[0]:
        if cell == ' ':
            return False
    return True

def check_win(board, checker):
    """
    Return True if the given checker has four in a row.
    Check horizontally, vertically, and both diagonals.
    """
    rows = len(board)
    cols = len(board[0])

    # Horizontal
    for r in range(rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r][c + i] == checker for i in range(WIN_COUNT)):
                return True

    # Vertical
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols):
            if all(board[r + i][c] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal: top-left to bottom-right
    for r in range(rows - WIN_COUNT + 1):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r + i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    # Diagonal: bottom-left to top-right
    for r in range(WIN_COUNT - 1, rows):
        for c in range(cols - WIN_COUNT + 1):
            if all(board[r - i][c + i] == checker for i in range(WIN_COUNT)):
                return True

    return False

def main():
    # Game setup
    board = create_board(NUM_ROWS, NUM_COLS)
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    current = random.randint(0, NUM_PLAYERS - 1)

    clear_screen()
    print("Welcome to Connect 4!\n")
    print_board(board)
    print(f"Player {players[current]} starts!\n")

    # Game loop
    moves = 0
    while True:
        player_checker = players[current]
        col_index = input_column(board, player_checker)

        clear_screen()
        if col_index is not None:
            row_index = place_checker(board, col_index, player_checker)
            moves += 1

            print_board(board)

            if check_win(board, player_checker):
                print(f"Player {player_checker} won!")
                break

            if board_full(board):
                print("Game is a draw!")
                break
        else:
            print_board(board)
            print("Turn lost due to full column.")  # Clarify why turn is lost

            if board_full(board):
                print("Game is a draw!")
                break

        # Next player's turn
        current = (current + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
