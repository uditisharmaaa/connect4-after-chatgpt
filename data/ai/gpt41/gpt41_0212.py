import os
import random
import string
import sys

# ----------- CONSTANTS -----------
ROWS = 6
COLUMNS = 7
PLAYER_COUNT = 2  # Can be between 2 and 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Supported player tokens

# ----------- FUNCTIONS -----------

def clear_screen():
    os.system('clear')  # Use 'cls' for Windows, 'clear' for Unix/Linux/Mac

def create_board(rows, columns):
    """Creates an empty board."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Prints the board in the required format."""
    column_labels = [string.ascii_uppercase[i] for i in range(len(board[0]))]
    print('  ' + '   '.join(column_labels))
    print('+' + '---+' * len(board[0]))
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * len(board[0]))

def get_next_open_row(board, col):
    """Finds the next available row in a column (from bottom up). Returns None if full."""
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            return row
    return None

def is_valid_column(board, col):
    """Checks if a column is within range and not full."""
    if 0 <= col < len(board[0]):
        return board[0][col] == ' '
    return False

def drop_checker(board, row, col, checker):
    """Places the checker in the given position."""
    board[row][col] = checker

def input_column(board, player_checker):
    """Asks the player for a column. Handles input validation."""
    valid_columns = [string.ascii_uppercase[i] for i in range(len(board[0]))]
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(inp) != 1 or inp not in valid_columns:
            print(f"Invalid input. Please enter a letter in {', '.join(valid_columns)}.")
            continue
        col = valid_columns.index(inp)
        if not is_valid_column(board, col):
            print("This column is full. You lose your turn.")
            return None  # Important: Lose turn if column is full
        return col

def check_for_win(board, checker):
    """Checks if current checker has 4 in a row anywhere."""
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

    # Diagonal (/)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    # Diagonal (\)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    return False

def board_is_full(board):
    return all(cell != ' ' for row in board for cell in row)

def random_first_player(num_players):
    return random.randint(0, num_players - 1)

def main():
    # Sanity checks on constants
    if not (2 <= PLAYER_COUNT <= 5):
        print("PLAYER_COUNT must be between 2 and 5.")
        sys.exit(1)
    if not (1 <= COLUMNS <= 26):
        print("COLUMNS must be between 1 and 26.")
        sys.exit(1)
    if ROWS < 1:
        print("ROWS must be at least 1.")
        sys.exit(1)

    # Setup
    board = create_board(ROWS, COLUMNS)
    player_checkers = CHECKERS[:PLAYER_COUNT]
    current_player_index = random_first_player(PLAYER_COUNT)

    clear_screen()
    print_board(board)

    while True:
        player_checker = player_checkers[current_player_index]
        col = input_column(board, player_checker)
        clear_screen()
        if col is not None:
            row = get_next_open_row(board, col)
            drop_checker(board, row, col, player_checker)
            print_board(board)

            if check_for_win(board, player_checker):
                print(f"Player {player_checker} won!")
                break
            if board_is_full(board):
                print("The game is a draw!")
                break
        else:
            print_board(board)

        # Move to next player (even if move was invalid due to full column)
        current_player_index = (current_player_index + 1) % PLAYER_COUNT

if __name__ == "__main__":
    main()
