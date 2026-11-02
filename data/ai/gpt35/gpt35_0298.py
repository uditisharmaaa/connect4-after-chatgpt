import os
import random

# Constants: Board dimensions and players
ROWS = 6           # Number of rows
COLUMNS = 7        # Number of columns (max 26)
PLAYERS = 2        # Number of players (2 to 5)
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checkers for players in order
WIN_LENGTH = 4     # Number of consecutive checkers needed to win

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board(rows, columns):
    """Create and return an empty board initialized with spaces."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the Connect 4 board with column labels."""
    clear_screen()

    # Print column labels A...G (or more if columns > 7)
    labels = '  ' + '   '.join(chr(ord('A') + i) for i in range(len(board[0])))
    print(labels)
    # Print board rows with borders
    for row in board:
        print("+---" * len(row) + '+')
        print('|' + '|'.join(f" {cell} " for cell in row) + '|')
    print("+---" * len(board[0]) + '+')

def is_valid_column(col_char, columns):
    """Check if the input column character is valid for the board."""
    if len(col_char) != 1:
        return False
    col_num = ord(col_char) - ord('A')
    return 0 <= col_num < columns

def get_column_index(col_char):
    """Convert a column letter to zero-based column index."""
    return ord(col_char) - ord('A')

def place_checker(board, col_index, checker):
    """
    Place the checker into the column if possible.
    The checker falls to the lowest empty cell in that column.

    Returns:
        True if placed successfully,
        False if the column is full (and player loses turn).
    """
    for row in reversed(range(len(board))):  # from bottom row upwards
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    return False  # Column full

def check_line(board, start_row, start_col, delta_row, delta_col, checker):
    """
    Check one direction for 4 consecutive checkers for given player.
    Returns True if 4 in a row found starting from (start_row, start_col)
    going in direction (delta_row, delta_col), else False.
    """
    count = 0
    row, col = start_row, start_col
    rows, cols = len(board), len(board[0])
    while 0 <= row < rows and 0 <= col < cols and board[row][col] == checker:
        count += 1
        if count == WIN_LENGTH:
            return True
        row += delta_row
        col += delta_col
    return False

def check_win(board, checker):
    """Check board for a win condition for the given checker."""
    rows, cols = len(board), len(board[0])

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            # Check all 4 directions from current cell:
            # horizontal (0,1), vertical (1,0), diagonal down-right (1,1), diagonal up-right (-1,1)
            if (check_line(board, r, c, 0, 1, checker) or
                check_line(board, r, c, 1, 0, checker) or
                check_line(board, r, c, 1, 1, checker) or
                check_line(board, r, c, -1, 1, checker)):
                return True
    return False

def check_draw(board):
    """Check if the board is full (draw)."""
    # If any cell in top row is empty, not draw yet
    return all(cell != ' ' for cell in board[0])

def get_valid_input(current_player):
    """
    Prompt the player for a column input.
    Validate input until correct or column full (lose turn).
    Returns the column character if valid or None if column full.
    """
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        if not is_valid_column(user_input, COLUMNS):
            print("Invalid input. Please enter an uppercase letter corresponding to a column.")
            continue
        col_idx = get_column_index(user_input)
        # Check if column full by verifying top row cell
        # If full, player loses the turn (return None)
        if board[0][col_idx] != ' ':
            # According to spec, turn is lost immediately
            print(f"Column {user_input} is full. You lose your turn.")
            return None
        return user_input

# Initialize board and select random starting player
board = create_board(ROWS, COLUMNS)
player_indices = list(range(PLAYERS))
current_player_index = random.choice(player_indices)

print_board(board)

while True:
    checker = CHECKERS[current_player_index]
    user_col = get_valid_input(checker)
    # If user_col is None, player lost turn (column full)
    if user_col is not None:
        col_index = get_column_index(user_col)
        placed = place_checker(board, col_index, checker)
        # place_checker should always succeed here because we check full beforehand
        # But if not, just continue without switching player, to be safe
        if not placed:
            print(f"Unexpected error: Could not place checker in column {user_col}. Turn lost.")
        print_board(board)

        # Check for a win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break
    else:
        # player loses turn due to full column, show unchanged board
        # No board change so no re-print here (as per spec)
        pass

    # Move to next player
    current_player_index = (current_player_index + 1) % PLAYERS
