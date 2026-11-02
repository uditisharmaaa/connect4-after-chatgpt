import os
import random
import string

# ==== CONSTANTS (Changeable for testing, assignment requires 6x7 and 2 players on submission) ====
ROWS = 6                # number of rows
COLUMNS = 7             # number of columns (<= 26)
PLAYER_COUNT = 2        # number of players (2 to 5)
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # player checker symbols, select count as needed

# ==== GLOBALS ====
BOARD = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]  # 2D list representing the board
COLUMN_LABELS = list(string.ascii_uppercase[:COLUMNS])         # e.g. ['A', ..., 'G']

# ==== FUNCTIONS ====

def clear_screen():
    """Clears the terminal screen for readability"""
    os.system('clear')

def print_board():
    """Prints the current state of the board in the required format."""
    # Print column labels
    print("  " + "   ".join(COLUMN_LABELS))
    print("+" + "---+" * COLUMNS)
    for row in BOARD:
        row_str = "| " + " | ".join(row) + " |"
        print(row_str)
        print("+" + "---+" * COLUMNS)

def initialize_board():
    """Initializes the BOARD to all whitespaces."""
    for r in range(ROWS):
        for c in range(COLUMNS):
            BOARD[r][c] = " "

def get_column_index(col_letter):
    """Returns index of column given column label letter (returns None if invalid)."""
    col_letter = col_letter.upper()
    if col_letter in COLUMN_LABELS:
        return COLUMN_LABELS.index(col_letter)
    return None

def is_column_full(col_index):
    """Checks if a given column index is full."""
    return BOARD[0][col_index] != " "

def place_checker(col_index, checker):
    """
    Places a checker in the lowest available spot in the specified column.
    Returns True if successful, False if the column is full.
    """
    for row in range(ROWS-1, -1, -1):
        if BOARD[row][col_index] == " ":
            BOARD[row][col_index] = checker
            return row  # Return the row where the checker landed
    return -1  # Column Full

def valid_column_input(user_input):
    """Validate input: is a single letter, in available columns, and not full."""
    if len(user_input) != 1 or not user_input.isalpha():
        return False
    col_index = get_column_index(user_input)
    if col_index is None:
        return False
    if is_column_full(col_index):
        return False
    return True

def check_win(row, col, checker):
    """Checks if placing 'checker' at (row, col) wins the game for the checker."""
    return (check_direction(row, col, checker, 0, 1)   # horizontal
            or check_direction(row, col, checker, 1, 0)    # vertical
            or check_direction(row, col, checker, 1, 1)    # diagonal down-right
            or check_direction(row, col, checker, 1, -1))  # diagonal down-left

def check_direction(row, col, checker, drow, dcol):
    """
    Checks if there are 4 in a row for checker starting at (row, col) in direction (drow, dcol).
    Returns True if four in a row.
    """
    count = 1  # The checker just placed
    # Check one way
    r, c = row + drow, col + dcol
    while 0 <= r < ROWS and 0 <= c < COLUMNS and BOARD[r][c] == checker:
        count += 1
        r += drow
        c += dcol
    # Check the other way
    r, c = row - drow, col - dcol
    while 0 <= r < ROWS and 0 <= c < COLUMNS and BOARD[r][c] == checker:
        count += 1
        r -= drow
        c -= dcol
    return count >= 4

def is_draw():
    """Returns True if the board is full and no winner."""
    for col in range(COLUMNS):
        if BOARD[0][col] == " ":
            return False
    return True

def get_valid_move(player_checker):
    """
    Prompts the current player for a valid column input.
    Keeps asking until valid input.
    Returns the valid column index.
    """
    while True:
        col_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input. Please enter a single column letter (e.g., A).")
            continue
        col_index = get_column_index(col_input)
        if col_index is None:
            print("Invalid input. Column does not exist.")
            continue
        if is_column_full(col_index):
            print("Column is full. You lose your turn.")
            return None  # Losing the turn, as per assignment
        return col_index

def select_first_player(player_count):
    """Randomly selects and returns the index of the first player."""
    return random.randint(0, player_count - 1)

# ==== MAIN GAME FUNCTION ====

def main():
    initialize_board()
    current_players = CHECKERS[:PLAYER_COUNT]
    turn = select_first_player(PLAYER_COUNT)

    while True:
        clear_screen()
        print_board()

        player_checker = current_players[turn]
        col_index = None
        # Get move - if column is full, player loses the turn automatically (only on full col)
        while col_index is None:
            col_index = get_valid_move(player_checker)
            if col_index is None:  # lose turn if column full on selection
                break

        if col_index is not None:
            # Place the checker (guaranteed column is not full)
            row_index = place_checker(col_index, player_checker)
            clear_screen()
            print_board()

            # Check Win
            if check_win(row_index, col_index, player_checker):
                print(f"Player {player_checker} won!")
                break

            # Check Draw
            if is_draw():
                print("Game ended in a draw!")
                break

        # Move to next turn
        turn = (turn + 1) % PLAYER_COUNT

if __name__ == "__main__":
    main()
