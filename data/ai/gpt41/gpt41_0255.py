import random
import os
import sys
import string

# === CONSTANTS ===
NUM_ROWS = 6
NUM_COLS = 7
CHECKERS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2                   # Set for assignment, 2 players
PLAYER_CHECKERS = CHECKERS[:NUM_PLAYERS]
MAX_COLS = 26                     # For possible expansion (A-Z)
WIN_LENGTH = 4

# === HELPER FUNCTIONS ===

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')


def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    cols = len(board[0])
    header = '  ' + '   '.join(string.ascii_uppercase[:cols])
    sep = '+' + ('---+' * cols)
    print(header)
    print(sep)
    for row in board:
        print('|' + '|'.join(' {} '.format(cell) for cell in row) + '|')
        print(sep)


def get_valid_columns(board):
    """Return a list of column indices (ints) that are not full."""
    valid_cols = []
    for col in range(len(board[0])):
        if board[0][col] == ' ':
            valid_cols.append(col)
    return valid_cols


def column_to_index(column_letter):
    """Convert column letter (A, B, ...) to column index (0, 1, ...)."""
    column_letter = column_letter.upper()
    if column_letter in string.ascii_uppercase:
        return ord(column_letter) - ord('A')
    return None


def is_valid_input(inp, board):
    """Checks for valid input column letter that is not full."""
    if len(inp) != 1 or inp not in string.ascii_uppercase[:len(board[0])]:
        return False
    col_idx = column_to_index(inp)
    if col_idx is None or col_idx < 0 or col_idx >= len(board[0]):
        return False
    # Check if column is full
    if board[0][col_idx] != ' ':
        return False
    return True


def drop_checker(board, col_idx, checker):
    """Places a checker in the lowest unoccupied row in the column."""
    for row in reversed(range(len(board))):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return row, col_idx
    return None  # Should not happen if input is valid


def is_board_full(board):
    return all(cell != ' ' for cell in board[0])


def check_winner(board, checker):
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            # Horizontal win
            if c + WIN_LENGTH <= cols and all(board[r][c+i] == checker for i in range(WIN_LENGTH)):
                return True
            # Vertical win
            if r + WIN_LENGTH <= rows and all(board[r+i][c] == checker for i in range(WIN_LENGTH)):
                return True
            # Diagonal \ win
            if (r + WIN_LENGTH <= rows and c + WIN_LENGTH <= cols and
                all(board[r+i][c+i] == checker for i in range(WIN_LENGTH))):
                return True
            # Diagonal / win
            if (r + WIN_LENGTH <= rows and c - WIN_LENGTH + 1 >= 0 and
                all(board[r+i][c-i] == checker for i in range(WIN_LENGTH))):
                return True
    return False


# === MAIN GAME LOOP ===

def main():
    random.seed()

    board = create_board(NUM_ROWS, NUM_COLS)
    player_indices = list(range(NUM_PLAYERS))
    # Randomly select who starts
    current_player_idx = random.choice(player_indices)
    player_symbols = PLAYER_CHECKERS

    clear_screen()
    print_board(board)

    # Main game loop
    while True:
        checker = player_symbols[current_player_idx]
        print(f"Player {checker}, please enter a column:")
        # Input Loop & Validation
        while True:
            user_input = input().strip().upper()
            if len(user_input) == 0:
                print("Please enter a column letter (A-{0}):".format(string.ascii_uppercase[NUM_COLS-1]))
                continue
            if user_input not in string.ascii_uppercase[:NUM_COLS]:
                print("Invalid column! Please enter one of {0}".format(', '.join(string.ascii_uppercase[:NUM_COLS])))
                continue
            col_idx = column_to_index(user_input)
            if col_idx is None:
                print("Invalid input! Please enter a correct column letter (A-{0}).".format(string.ascii_uppercase[NUM_COLS-1]))
                continue
            if board[0][col_idx] != ' ':
                print("Column is full! You lose your turn.")
                break # Lose turn, so exit input loop
            else:
                # Place checker
                drop_checker(board, col_idx, checker)
                break

        clear_screen()
        print_board(board)

        # Check for a win
        if check_winner(board, checker):
            print(f"Player {checker} won!")
            break

        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break

        # Next player
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
