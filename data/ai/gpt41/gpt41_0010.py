import os
import random
import string
import sys

# ------------------------------ #
#          CONSTANTS             #
# ------------------------------ #

ROWS = 6                  # Number of rows on the board
COLUMNS = 7               # Number of columns on the board (max 26)
N_PLAYERS = 2             # Number of players (2-5 allowed)
PLAYER_MARKERS = ['X', 'O', 'V', 'H', 'M']  # Markers available for up to 5 players

# Number required in a row to win
WIN_COUNT = 4

# ------------------------------ #
#       UTILITY FUNCTIONS        #
# ------------------------------ #

def clear_screen():
    """
    Clears the terminal screen.
    """
    os.system('clear')

def create_board(rows, cols):
    """
    Creates the Connect 4 board as a 2D list initialized to ' ' (space).

    Args:
        rows (int): Number of rows.
        cols (int): Number of columns.

    Returns:
        list of list: The empty game board.
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """
    Prints the board to the screen in the required Connect 4 style.

    Args:
        board (list of list): The game board to print.
    """
    cols = len(board[0])
    # Print column headers (A, B, C, ...)
    column_headers = '  ' + '   '.join(string.ascii_uppercase[:cols])
    print(column_headers)
    # Print top border
    print('+' + '---+' * cols)
    # Print rows
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)

def get_valid_columns(board):
    """
    Returns the list of valid column labels for columns that are not full.

    Args:
        board (list of list): The current board.

    Returns:
        list of str: Valid column letters where checkers can be dropped.
    """
    cols = len(board[0])
    valid = []
    for c in range(cols):
        if board[0][c] == ' ':
            valid.append(string.ascii_uppercase[c])
    return valid

def get_column_index(col_letter, cols):
    """
    Converts a column letter to an index. Returns -1 if invalid.

    Args:
        col_letter (str): Column letter (A, B, ...).
        cols (int): Total columns on the board.

    Returns:
        int: Column index, or -1 if invalid.
    """
    col_letter = col_letter.upper()
    if len(col_letter) == 1 and col_letter in string.ascii_uppercase[:cols]:
        return string.ascii_uppercase.index(col_letter)
    else:
        return -1

def is_full(board):
    """
    Returns whether the board is completely full (no moves possible).

    Args:
        board (list of list): The current board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    return all(cell != ' ' for cell in board[0])

def place_checker(board, column_idx, marker):
    """
    Places a marker in the lowest available row in the given column.

    Args:
        board (list of list): The board.
        column_idx (int): The column index to drop the checker into.
        marker (str): The player's marker.

    Returns:
        bool: True if placement successful, False (if the column is full).
    """
    for row in reversed(range(len(board))):
        if board[row][column_idx] == ' ':
            board[row][column_idx] = marker
            return True, row, column_idx
    return False, None, None

def check_winner(board, marker, last_row, last_col):
    """
    Checks if placing a checker at (last_row, last_col) wins for marker.

    Args:
        board (list of list): The board.
        marker (str): The player's marker.
        last_row (int): Row index of last placed checker.
        last_col (int): Column index of last placed checker.

    Returns:
        bool: True if the marker has 4 in a row, otherwise False.
    """

    def count_in_direction(delta_row, delta_col):
        cnt = 0
        r, c = last_row + delta_row, last_col + delta_col
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == marker:
            cnt += 1
            r += delta_row
            c += delta_col
        return cnt

    # Check all four directions: horizontal, vertical, two diagonals
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)] # E, S, SE, SW
    for dr, dc in directions:
        count = 1  # Include the checker we just placed
        count += count_in_direction(dr, dc)
        count += count_in_direction(-dr, -dc)
        if count >= WIN_COUNT:
            return True
    return False

def get_player_input(player_marker, valid_columns):
    """
    Prompts the player for a valid column and validates input.

    Args:
        player_marker (str): Current player's marker.
        valid_columns (list of str): Valid column labels.

    Returns:
        str: Validated column letter.
    """
    while True:
        user_input = input(f"Player {player_marker}, please enter a column: ").strip().upper()
        if (len(user_input) == 1
            and user_input in valid_columns):
            return user_input
        else:
            print(f"Invalid input. Valid columns are: {', '.join(valid_columns)}")

# ------------------------------ #
#          MAIN GAME LOOP        #
# ------------------------------ #

def main():
    # Setup the game
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_MARKERS[:N_PLAYERS]

    # Randomly select who starts
    current_player = random.randint(0, N_PLAYERS - 1)

    # Print initial board
    clear_screen()
    print_board(board)

    # Game loop
    turns = 0
    while True:
        # Gather valid columns (unfilled)
        valid_columns = get_valid_columns(board)

        # If board is full before this turn, it's a draw (shouldn't happen, but guard)
        if not valid_columns:
            print("It's a draw! No more moves possible.")
            break

        active_marker = players[current_player]
        print(f"Player {active_marker}'s turn.")

        col_letter = get_player_input(active_marker, valid_columns)
        col_idx = get_column_index(col_letter, COLUMNS)

        # Place the checker
        placed, row, col = place_checker(board, col_idx, active_marker)

        turns += 1  # We count every attempted turn, whether valid or not

        clear_screen()
        print_board(board)

        if not placed:
            print(f"Column {col_letter} is already full! Player {active_marker} loses this turn.")
            # Move to next player anyway:
            current_player = (current_player + 1) % N_PLAYERS
            continue

        # Check for win condition
        if check_winner(board, active_marker, row, col):
            print(f"Player {active_marker} won!")
            break

        # Check for draw AFTER a valid move
        if is_full(board):
            print("It's a draw! No more moves possible.")
            break

        # Move to next player's turn
        current_player = (current_player + 1) % N_PLAYERS

if __name__ == '__main__':
    main()
