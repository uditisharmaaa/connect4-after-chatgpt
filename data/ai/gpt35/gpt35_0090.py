import os
import random

# Constants for board dimensions and players
ROWS = 6                   # Number of rows on the board
COLUMNS = 7                # Number of columns on the board
NUM_PLAYERS = 2            # Number of players (between 2 and 5)
WIN_COUNT = 4              # Number of checkers in a row needed to win

# Player checkers in order
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# Validate constant constraints
assert 2 <= NUM_PLAYERS <= 5, "NUM_PLAYERS must be between 2 and 5"
assert COLUMNS <= 26, "Maximum columns allowed is 26"


def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')


def create_board():
    """Initialize the game board with whitespaces."""
    # Board is a list of rows, each row is a list of strings (cells)
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]


def print_board(board):
    """Print the board with column letters and grid lines."""
    clear_screen()
    # Print column labels (A, B, C, ...)
    column_labels = [chr(ord('A') + i) for i in range(COLUMNS)]
    print('  ' + '   '.join(column_labels))
    
    # Print each row with separators
    horizontal_line = '+' + ('---+' * COLUMNS)
    for row in board:
        print(horizontal_line)
        row_str = '|'
        for cell in row:
            row_str += ' ' + cell + ' |'
        print(row_str)
    print(horizontal_line)


def column_to_index(column_letter):
    """
    Convert a column letter (A-G) to a board index (0-6).
    Returns the index or -1 if invalid.
    """
    if len(column_letter) != 1:
        return -1
    column_letter = column_letter.upper()
    index = ord(column_letter) - ord('A')
    if 0 <= index < COLUMNS:
        return index
    else:
        return -1


def is_valid_column(board, col_index):
    """
    Check if there is space in the column to place a checker.
    If the top row is empty, column is not full.
    """
    return board[0][col_index] == ' '


def place_checker(board, col_index, checker):
    """
    Place a checker in the given column.
    The checker falls to the lowest available spot.
    Returns True if placed, False if column full.
    """
    # Start from bottom row and move upwards
    for row in range(ROWS-1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    # Column full
    return False


def check_line(line, checker):
    """
    Check if a consecutive sequence of length WIN_COUNT with the given checker exists in the line.
    line: list of cells (strings)
    checker: single character string representing player checker
    """
    count = 0
    for cell in line:
        if cell == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
    return False


def check_win(board, checker):
    """Check if the player with 'checker' has won the game."""

    # Horizontal check
    for row in range(ROWS):
        if check_line(board[row], checker):
            return True

    # Vertical check
    for col in range(COLUMNS):
        column_cells = [board[row][col] for row in range(ROWS)]
        if check_line(column_cells, checker):
            return True

    # Diagonal check (down-right direction)
    for row in range(ROWS - WIN_COUNT + 1):
        for col in range(COLUMNS - WIN_COUNT + 1):
            diagonal = [board[row + i][col + i] for i in range(WIN_COUNT)]
            if all(cell == checker for cell in diagonal):
                return True

    # Diagonal check (up-right direction)
    for row in range(WIN_COUNT - 1, ROWS):
        for col in range(COLUMNS - WIN_COUNT + 1):
            diagonal = [board[row - i][col + i] for i in range(WIN_COUNT)]
            if all(cell == checker for cell in diagonal):
                return True

    return False


def board_full(board):
    """Check if the board is full (no empty spaces in top row)."""
    # If any top-row cell is empty, board is not full
    return all(cell != ' ' for cell in board[0])


def get_player_input(player_checker):
    """
    Prompt the player to enter a column letter, validate input.
    Returns column index if valid, or None if turn is lost due to full column.
    """
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(user_input) != 1 or not ('A' <= user_input <= chr(ord('A') + COLUMNS - 1)):
            print(f"Invalid input '{user_input}'. Please enter a column letter between A and {chr(ord('A') + COLUMNS - 1)}.")
            continue

        col_index = column_to_index(user_input)
        if col_index == -1:
            print(f"Invalid column '{user_input}'. Please select a valid column.")
            continue

        # If column is full, player loses turn
        if not is_valid_column(board, col_index):
            print(f"Column {user_input} is full. You lose your turn.")
            return None

        return col_index


# Main game code
board = create_board()

# Select random starting player index
current_player_index = random.randint(0, NUM_PLAYERS - 1)

print_board(board)

while True:
    player_checker = CHECKERS[current_player_index]

    col = get_player_input(player_checker)

    # If col is None, player loses turn (column full)
    if col is not None:
        placed = place_checker(board, col, player_checker)
        # placed should always be True here, since we checked validity earlier

    print_board(board)

    # Check for win only if player placed a checker this turn
    if col is not None and check_win(board, player_checker):
        print(f"Player {player_checker} won!")
        break

    # Check for draw if board full
    if board_full(board):
        print("The game is a draw.")
        break

    # Move to next player
    current_player_index = (current_player_index + 1) % NUM_PLAYERS
